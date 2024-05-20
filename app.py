import logging
import streamlit as st
from llama_index.core import SQLDatabase, VectorStoreIndex
from llama_index.core.objects import SQLTableNodeMapping, SQLTableSchema, ObjectIndex
from pandas import DataFrame
from sqlalchemy import Connection
from typing import Dict, Any, Iterator
from llama_index.core.llama_pack.base import BaseLlamaPack
import os
import pandas as pd
from llama_index.core.indices.struct_store import NLSQLTableQueryEngine
from extensions import database, ai
from config import config

#os.environ['OPENAI_API_KEY'] = config.openai_api_key


class StreamlitChatPack(BaseLlamaPack):

    def __init__(self, page: str = "Natural Language to SQL Query", run_from_main: bool = False, **kwargs: Any,) -> None:
        self.page = page

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {}

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        # Set page config
        st.set_page_config(page_title=f"{self.page}",
                           layout="centered",
                           initial_sidebar_state="auto",
                           menu_items=None)

        # Initialize the chat messages history
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": f"Hello. Ask me anything related to the database."}]

        # Set title
        st.title(f"{self.page}💬")
        st.info(f"Explore eshop views with this AI-powered app. Pose any question and receive data.", icon="ℹ️",)

        def add_to_message_history(role, content):
            # Add response to message history
            st.session_state["messages"].append({"role": role, "content": str(content)})

        def get_table_data(table_name, conn):
            sql = f"SELECT * FROM {table_name}"
            return execute_query(sql=sql, conn=conn, fetch_all=False)

        def execute_query(sql: str, conn: Connection, fetch_all: bool) -> DataFrame | Iterator[DataFrame]:
            result: Iterator[DataFrame] = pd.read_sql_query(sql=sql.removesuffix(";"), con=conn, chunksize=config.database_fetch_size)

            if not fetch_all:
                for data_frame in result:
                    return data_frame

            return pd.concat(result, ignore_index=True)

        def write_data_into_response(sql: str, conn: Connection) -> None:
            data: DataFrame = execute_query(sql=sql, conn=conn, fetch_all=True if "fetch all data" in prompt.lower() else False)
            if len(data.index) == config.database_fetch_size:
                with st.empty():
                    f"Only {config.database_fetch_size} rows were fetched. If you would like to fetch all rows, append to end of your question \"- fetch all data\""
            with st.empty():
                st.dataframe(data)

        @st.cache_resource
        def load_db():
            db_engine = database.get_engine()
            db_connection = database.get_connection()
            sql_db = SQLDatabase(engine=db_engine)
            return sql_db, db_engine, db_connection

        sql_database, engine, connection = load_db()

        # Sidebar for database schema viewer
        st.sidebar.markdown("## Database Object Viewer")
        table_names = config.app_table_list

        # Sidebar selection for tables
        selected_table = st.sidebar.selectbox("Select a Table", table_names)

        # Display the selected table
        if selected_table:
            df = get_table_data(selected_table, connection)
            st.sidebar.text(f"Data for table '{selected_table}':")
            st.sidebar.dataframe(df)

        # Sidebar Intro
        #st.sidebar.markdown('## App Created By')
        #st.sidebar.markdown("""Ludek""")

        # Initialize the query engine
        if "query_engine" not in st.session_state:
            # Create query engine
            st.session_state["query_engine"] = NLSQLTableQueryEngine(sql_database=sql_database,
                                                                     tables=config.app_table_list,
                                                                     llm=ai.get_llm(),
                                                                     sql_only=True,
                                                                     synthesize_response=False)

        # Display the prior chat messages
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Prompt for user input and save to chat history
        if prompt := st.chat_input("Enter your natural language query about the database"):
            with st.chat_message("user"):
                st.write(prompt)
            add_to_message_history("user", prompt)

        # If last message is not from assistant, generate a new response
        if st.session_state["messages"][-1]["role"] != "assistant":
            with st.spinner():
                with st.chat_message("assistant"):
                    response = st.session_state["query_engine"].query(f"User Question:{prompt}.")
                    sql_query = f"```sql\n{response.metadata['sql_query']}\n```\n**Response:**\n{response.response}\n"

                    response_container = st.empty()
                    response_container.write(sql_query)
                    add_to_message_history("assistant", sql_query)

                    write_data_into_response(sql=response.metadata['sql_query'], conn=connection)


if __name__ == "__main__":
    StreamlitChatPack(run_from_main=True).run()
