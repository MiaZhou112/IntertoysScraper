import psycopg2
from sqlalchemy import create_engine
import pandas as pd

def add_file_in_DB(database_uri, database_table, input_filename):
    engine = create_engine(database_uri)
    with pd.ExcelFile(input_filename) as f:
        df = pd.read_excel(f)
        df.to_sql(name= database_table,con=engine,if_exists='replace',index=False)
    
        


