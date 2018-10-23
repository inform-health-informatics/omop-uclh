# TODO Connects to a data base using SQLalchemy
from sqlalchemy import create_engine


def gen_connection_string(d):
    """Generates a SQLAlchemy connection string from a dictionary"""
    # e.g.
    # engine = create_engine('postgresql+psycopg2://steve@localhost:5432/omop')
    # TODO @later permit other interfaces
    d['port'] = str(d['port'])
    # - [ ] @TODO: (2018-10-23) fix for when there is no password (SSH tunnel)
    if 'password' in d.keys():
        if len(d['password']):
    connection_string = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
        **d)
    return connection_string


# - [ ] @TODO: (2018-10-23) set these up as environment variables
connection_dict = {    'user': 'postgres',
    'host': 'localhost',
    'port': 6543,
    'password': 'postgres',
    'database': 'TEST_SM'
}

connection_string = gen_connection_string(connection_dict)
connection_string

engine = create_engine(connection_string)
conn = engine.connect()

# - [ ] @TODO: (2018-10-23)  Confirms that the data base does not already ontain the tables in question

import sqlalchemy as sa
sa.inspect(engine).get_table_names()
from sqlalchemy import MetaData
metadata = MetaData(conn, schema='TEST_SM')
metadata.tables

# Deletes the existing tables with a FORCE option

# Creates a table following a specification stored in a configuration file
# based on the OMOPCDM ddl
