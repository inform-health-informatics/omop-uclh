# TODO Connects to a data base using SQLalchemy
from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric,
                        String, DateTime, Date, ForeignKey, Boolean, create_engine)
from utils import gen_connection_string
import psycopg2


class DataAccessLayer:
    conn = None
    engine = None
    conn_string = None
    metadata = MetaData()

    concept = Table('concept', metadata,
                    Column('concept_id', Integer(), nullable=False, primary_key=True),
                    Column('concept_name', String(255), nullable=False),
                    Column('domain_id', String(20), nullable=False),
                    Column('vocabulary_id', String(20), nullable=False),
                    Column('concept_class_id', String(20), nullable=False),
                    Column('standard_concept', String(1), nullable=True),
                    Column('concept_code', String(50), nullable=False),
                    Column('valid_start_date', Date, nullable=False),
                    Column('valid_end_date', Date, nullable=False),
                    Column('invalid_reason', String(1), nullable=True)
                    )

    def db_init(self, conn_string):
        self.engine = create_engine(conn_string or self.conn_string)
        self.metadata.create_all(self.engine)
        self.conn = self.engine.connect()

# - [ ] @TODO: (2018-10-23) set these up as environment variables
connection_dict = {'user': 'postgres',
                   'host': 'localhost',
                   'port': 6543,
                   'password': 'postgres',
                   'database': 'TEST_SM'
                   }

connection_string = gen_connection_string(connection_dict)

dal = DataAccessLayer()
dal.db_init(connection_string)

# - [ ] @TODO: (2018-10-23)  Confirms that the data base does not already ontain the tables in question
# inspect existing tables
inspector = sa.inspect(dal.engine)
inspector.get_table_names()

# delete a table
concept = Table('concept', dal.metadata, autoload=True)
concept.drop(dal.engine, checkfirst=True)
inspector.get_table_names()

# create table
dal.concept.create(dal.engine, checkfirst=True)

# load data into table
# need to use psycopg2 copy_from
import psycopg2
import csv
pysco_conn = psycopg2.connect("host=localhost dbname=TEST_SM user=postgres password=postgres port=6543")
cur = pysco_conn.cursor()

with open('vocab/CONCEPT.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # skip the header row
    cur.copy_from(f, 'concept', sep='\t')

pysco_conn.commit()

# example single insert

dal.concept.insert().values()









# Deletes the existing tables with a FORCE option

# Creates a table following a specification stored in a configuration file
# based on the OMOPCDM ddl
