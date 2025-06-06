# import streamlit as st
# import pandas as pd
# from sqlalchemy import create_engine, text
# from sqlalchemy.orm import sessionmaker
# from meta_ai_api import MetaAI
# import pymysql

# # db_url = "mysql+pymysql://root:Sritesh@1234@localhost:3306/student_db"

# db_url = pymysql.connect(
#     host='localhost',
#     port=3306,
#     user='root',
#     password='your_password',
#     database='student_db'
# )

# # Function to execute SQL queries
# def execute_query(query, params=None):
#     engine = create_engine(db_url)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     try:
#         result = session.execute(text(query), params)
#         session.commit()
#         columns = result.keys()
#         rows = result.fetchall()
#         return pd.DataFrame(rows, columns=columns)
#     except Exception as e:
#         session.rollback()
#         st.error(f"An error occurred: {e}")
#         return None
#     finally:
#         session.close()

# # Function to fetch table names
# def get_table_names():
#     engine = create_engine(db_url)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     try:
#         result = session.execute(text("SHOW TABLES"))
#         tables = [row[0] for row in result]
#         return tables
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         return []
#     finally:
#         session.close()

# # Function to fetch schema description of a table
# def get_table_schema(table_name):
#     engine = create_engine(db_url)
#     Session = sessionmaker(bind=engine)
#     session = Session()

#     try:
#         result = session.execute(text(f"DESCRIBE {table_name}"))
#         schema = ', '.join([f"{row[0]} {row[1]}" for row in result])
#         return schema
#     except Exception as e:
#         st.error(f"An error occurred: {e}")
#         return ""
#     finally:
#         session.close()

# # Function to interact with MetaAI
# def metaAi(schema_description, user_question):
#     ai = MetaAI()
    
#     prompt = f'I have the following database schema: "{schema_description}" Based on this schema, please generate an SQL query for the following user question: "{user_question}" Provide only the SQL query without any additional text and formatting. And if invalid question is provided then return "INVALID STATEMENT" '
#     response = ai.prompt(message=prompt)
#     print(response)
    
#     return response['message']

# # Streamlit UI
# def main():
#     st.title("QueryGenAI")

#     tables = get_table_names()
#     if not tables:
#         st.error("No tables found in the database.")
#         return

#     chosen_table = st.selectbox("Choose a table", tables)

#     if chosen_table:
#         schema = get_table_schema(chosen_table)
#         schema = str(chosen_table) + ":(" + str(schema) + ")"

#         ques = st.text_input("Please Ask Question:")
#         if st.button("Generate Query"):
#             query = metaAi(schema, ques)
#             if query == "INVALID STATEMENT":
#                 st.error("Ask a valid question.")
#             else:
#                 result_df = execute_query(query)
#                 if result_df is not None and not result_df.empty:
#                     st.write("Results:")
#                     st.dataframe(result_df)
#                 else:
#                     st.write("No results found or an error occurred.")

# if __name__ == "__main__":
#     main()



import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from meta_ai_api import MetaAI
import pymysql
import urllib.parse
from urllib.parse import quote_plus

# Define the connection URL
# db_url = "mysql+pymysql://root:" + quote_plus("your password") + "@localhost:3306/querygenai_db"
db_url = "mysql+pymysql://root:" + quote_plus("your_password") + "@host.docker.internal:3306/querygenai_db"


print(db_url)

# Function to execute SQL queries
def execute_query(query, params=None):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(text(query), params)
        session.commit()
        columns = result.keys()
        rows = result.fetchall()
        return pd.DataFrame(rows, columns=columns)
    except Exception as e:
        session.rollback()
        st.error(f"An error occurred: {e}")
        return None
    finally:
        session.close()

# Function to fetch table names
def get_table_names():
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        return tables
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return []
    finally:
        session.close()

# Function to fetch schema description of a table
def get_table_schema(table_name):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        result = session.execute(text(f"DESCRIBE {table_name}"))
        schema = ', '.join([f"{row[0]} {row[1]}" for row in result])
        return schema
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""
    finally:
        session.close()

# Function to interact with MetaAI
def metaAi(schema_description, user_question):
    ai = MetaAI()
    
    prompt = f'I have the following database schema: "{schema_description}" Based on this schema, please generate an SQL query for the following user question: "{user_question}" Provide only the SQL query without any additional text and formatting. And if an invalid question is provided then return "INVALID STATEMENT".'
    response = ai.prompt(message=prompt)
    print(response['message'])
    return response['message']

# Streamlit UI
def main():
    st.title("QueryGenAI")

    tables = get_table_names()
    if not tables:
        st.error("No tables found in the database.")
        return

    chosen_table = st.selectbox("Choose a table", tables)

    if chosen_table:
        schema = get_table_schema(chosen_table)
        schema = str(chosen_table) + ":(" + str(schema) + ")"

        ques = st.text_input("Please Ask Question:")
        if st.button("Generate Query"):
            query = metaAi(schema, ques)
            if query == "INVALID STATEMENT":
                st.error("Ask a valid question.")
            else:
                result_df = execute_query(query)
                if result_df is not None and not result_df.empty:
                    st.write("Results:")
                    st.dataframe(result_df)
                else:
                    st.write("No results found or an error occurred.")

if __name__ == "__main__":
    main()



# docker build -t querygenai-app .       
# >>
# [+] Building 91.2s (10/10) FINISHED                                                                                docker:desktop-linux
#  => [internal] load build definition from Dockerfile                                                                               0.0s
#  => => transferring dockerfile: 264B                                                                                               0.0s 
#  => [internal] load metadata for docker.io/library/python:3.10                                                                     2.3s 
#  => [internal] load .dockerignore                                                                                                  0.0s
#  => => transferring context: 2B                                                                                                    0.0s 
#  => [1/5] FROM docker.io/library/python:3.10@sha256:678140eccfe77504f9681aea8bd881e0a9dc7422cf7808b6ed73e16458308227               0.0s 
#  => [internal] load build context                                                                                                  2.4s 
#  => => transferring context: 12.49MB                                                                                               2.3s 
#  => CACHED [2/5] WORKDIR /app                                                                                                      0.0s
#  => [3/5] COPY . /app                                                                                                              8.4s 
#  => [4/5] RUN pip install --upgrade pip                                                                                            6.6s
#  => [5/5] RUN pip install -r requirements.txt                                                                                     68.3s
#  => exporting to image                                                                                                             3.0s
#  => => exporting layers                                                                                                            3.0s 
#  => => writing image sha256:4dabec6617b0332d3d02b1b28463a4cb5e6ab336e189a775794dbf57b2e6dc2b                                       0.0s 
#  => => naming to docker.io/library/querygenai-app                                                                                  0.0s 

# What's next:
#     View a summary of image vulnerabilities and recommendations → docker scout quickview 
# (.venv) PS C:\Users\SRITESH BISI\Desktop\query gen ai> docker run -p 8501:8501 querygenai-app
# >>

# Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.


#   You can now view your Streamlit app in your browser.

#   URL: http://0.0.0.0:8501

# mysql+pymysql://root:Sritesh%401234@localhost:3306/querygenai_db
#   Stopping...
# (.venv) PS C:\Users\SRITESH BISI\Desktop\query gen ai> docker build -t querygenai-app .      
# >> 
# [+] Building 75.6s (10/10) FINISHED                                                                                docker:desktop-linux
#  => [internal] load build definition from Dockerfile                                                                               0.0s
#  => => transferring dockerfile: 264B                                                                                               0.0s 
#  => [internal] load metadata for docker.io/library/python:3.10                                                                     3.5s 
#  => [internal] load .dockerignore                                                                                                  0.0s
#  => => transferring context: 2B                                                                                                    0.0s 
#  => [internal] load build context                                                                                                  1.0s 
#  => => transferring context: 1.17MB                                                                                                1.0s 
#  => [1/5] FROM docker.io/library/python:3.10@sha256:678140eccfe77504f9681aea8bd881e0a9dc7422cf7808b6ed73e16458308227               0.0s 
#  => CACHED [2/5] WORKDIR /app                                                                                                      0.0s
#  => [3/5] COPY . /app                                                                                                              5.9s 
#  => [4/5] RUN pip install --upgrade pip                                                                                            5.4s
#  => [5/5] RUN pip install -r requirements.txt                                                                                     56.9s
#  => exporting to image                                                                                                             2.6s
#  => => exporting layers                                                                                                            2.6s 
#  => => writing image sha256:b60cacee2e665a1b9caeb69cffe629e0894329a772f22cab120971b41f911b0b                                       0.0s 
#  => => naming to docker.io/library/querygenai-app                                                                                  0.0s 

# What's next:
#     View a summary of image vulnerabilities and recommendations → docker scout quickview 
# (.venv) PS C:\Users\SRITESH BISI\Desktop\query gen ai> docker run -p 8501:8501 querygenai-app
# >> 

# Collecting usage statistics. To deactivate, set browser.gatherUsageStats to false.


#   You can now view your Streamlit app in your browser.

#   URL: http://0.0.0.0:8501 
