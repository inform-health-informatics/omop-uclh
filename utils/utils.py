# General utilities and helpers
import csv
import psycopg2
from typing import List


def parse_table_ddl(ddl: str, dialect: str ='PostgreSQL') -> List:
    """Parse SQL CREATE TABLE syntax into a list of tuples

    Arguments:
        ddl {str} -- [description]

    Keyword Arguments:
        dialect {str} -- [description] (default: {'PostgreSQL'})
    """
    from collections import namedtuple

    data_types = tuple(
        "INTEGER DATE VARCHAR TIMESTAMP TIME NUMERIC TEXT".lower().split())

    ColumnDefinition = namedtuple('ColumnDefinition', [
        'name',   # column name
        'type',   # data type e.g. INTEGER, VARCHAR etc.
        'null'    # NULL or NOT NULL
    ])

    column_definitions = list()

    for l in ddl.splitlines():
        l = l.split()
        try:
            dtype = l[1].lower()
            assert dtype.startswith(data_types)
            nullable = 'NULL' if l[2].lower() == 'null' else 'NOT NULL'
            column_definitions.append(
                ColumnDefinition(l[0], dtype.upper(), nullable))
        except AssertionError:
            continue
        except IndexError:
            continue

    return column_definitions


def gen_connection_string(d, engine='postgresql'):
    """Generates a SQLAlchemy connection string from a dictionary"""
    # e.g. # engine = create_engine('postgresql+psycopg2://steve@localhost:5432/omop')
    # TODO @later permit other interfaces
    d['port'] = str(d['port'])

    if engine == 'postgresql':
        if d.get('password'):
            return 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(**d)
        else:
            return 'postgresql+psycopg2://{user}@{host}:{port}/{database}'.format(**d)

    elif engine == 'psycopg2':
        if d.get('password'):
            return 'host={host} dbname={database} user={user} password={password} port={port}'.format(**d)
        else:
            return 'host={host} dbname={database} user={user} port={port}'.format(**d)


def build_from_vocab_csv(DSN, vocab_table, vocab_csv, force=False):
    """Given a Table object then populate that table from a CSV file
    using psycopg2 copy_from as a much more efficient bulk insert tool"""

    if force:
        SQL = "TRUNCATE {};".format(vocab_table)
        with psycopg2.connect(DSN) as conn:
            with conn.cursor() as curs:
                rp = curs.execute(SQL)

    with open(vocab_csv, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header row
        with psycopg2.connect(DSN) as conn:
            with conn.cursor() as curs:
                curs.copy_from(f, vocab_table, sep='\t')


def clean_start(DSN, force):
    """Drop all existing tables and data from a schema"""
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
    if force:
        with psycopg2.connect(DSN) as conn:
            with conn.cursor() as curs:
                rp = curs.execute(SQL)
