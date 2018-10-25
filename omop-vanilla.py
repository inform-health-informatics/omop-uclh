from utils.utils import gen_connection_string
import psycopg2

# - [ ] @TODO: (2018-10-23) set these up as environment variables
connection_dict = {'user': 'uclh',
                   'host': 'localhost',
                   'port': 55432,
                   'password': 'uclh',
                   'database': 'OMOPUCLH'
                   }

DSN = gen_connection_string(connection_dict, engine='psycopg2')

def clean_start():
    """Drop all existing tables and data"""
    # https://stackoverflow.com/questions/3327312/drop-all-tables-in-postgresql
    SQL = """
    DO $$ DECLARE
    r RECORD;
    BEGIN
        -- if the schema you operate on is not "current", you will want to
        -- replace current_schema() in query with 'schematodeletetablesfrom'
        -- *and* update the generate 'DROP...' accordingly.
        FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = current_schema()) LOOP
            EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
        END LOOP;
    END $$;
    """
    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as curs:
            rp = curs.execute(SQL)

clean_start()

# - [ ] @TODO: (2018-10-25) convert to git submodule or pull specific commit
# The order is important
CDM_files_path = 'CommonDataModel/PostgreSQL/'
CDM_files_names = [
'OMOP CDM postgresql ddl.txt',
'OMOP CDM postgresql indexes.txt',
'OMOP CDM postgresql constraints.txt',
]

for file_name in CDM_files_names:
    fp = CDM_files_path + file_name
    with open(fp, 'r') as f:
        SQL = f.read()
        with psycopg2.connect(DSN) as conn:
            with conn.cursor() as curs:
                rp = curs.execute(SQL)





