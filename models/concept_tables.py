from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric,
                        String, DateTime, Date, ForeignKey, Boolean, create_engine)
import psycopg2
import csv
from utils.utils import gen_connection_string


class DataAccessLayer:
    conn = None
    engine = None
    conn_string = None
    metadata = MetaData()

    concept = Table('concept', metadata,
                    Column('concept_id', Integer(),
                           nullable=False, primary_key=True),
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

    vocabulary = Table('vocabulary', metadata,
                       Column('vocabulary_id', String(20), nullable=False),
                       Column('vocabulary_name', String(255), nullable=False),
                       Column('vocabulary_reference',
                              String(255), nullable=False),
                       Column('vocabulary_version',
                              String(255), nullable=False),
                       Column('vocabulary_concept_id',
                              Integer(), nullable=False)
                       )

    def db_init(self, connection_dict):
        self.connection_dict = connection_dict
        if not self.conn_string:
            conn_string = gen_connection_string(
                self.connection_dict, engine='postgresql')
        self.engine = create_engine(conn_string or self.conn_string)
        self.metadata.create_all(self.engine)
        self.conn = self.engine.connect()

    def build_from_vocab_csv(self, vocab_table, vocab_csv, force=False):
        """Given a Table object then populate that table from a CSV file
        using psycopg2 copy_from as a much more efficient bulk insert tool"""

        if vocab_table in self.metadata and force:
            vocab_table.drop(self.engine, checkfirst=True)

        conn_string = gen_connection_string(
            self.connection_dict, engine='psycopg2')
        pysco_conn = psycopg2.connect(conn_string)
        cur = pysco_conn.cursor()

        with open(vocab_csv, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # skip the header row
            cur.copy_from(f, vocab_table.name, sep='\t')

        pysco_conn.commit()
