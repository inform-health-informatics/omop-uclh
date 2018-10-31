"""Fakes data for a single patient each time it is run

According to the data spec requestd by Abi
* AMUAI
    * antimicrobial use after 48h in ICU
    * boolean
* ANCPWBC
    * associated absolute neutrophil count from pre-admission WCC
    * decimal
* BPC
    * biopsy proven cirrhosis
    * boolean
* PHB
    * pre-admission haemoglobin
    * decimal
* LG
    * lowest serum glucose
    * decimal
# - [ ] @BREADCRUMB: (2018-10-30) start by loading in fake lactate data
* HBL
    * highest blood lactate
    * decimal
"""

# - [ ] @TODO: (2018-10-30) # connect to the data base
import sqlalchemy as sa
import psycopg2
from utils.utils import gen_connection_string
import fakers.faker as fake

connection_dict = {'user': 'uclh',
                   'host': 'localhost',
                   'port': 55432,
                   'password': 'uclh',
                   'database': 'OMOPUCLH'
                   }

DSN = gen_connection_string(connection_dict)
metadata = sa.MetaData()
engine = sa.create_engine(DSN)
connection = engine.connect()
# bind the whole database
metadata.reflect(bind=engine)

# Reflect person, visit and measurement tables
t_person = metadata.tables['person']
t_visit = metadata.tables['visit_occurrence']
# Good for subvisits at 'location or service level'; can be sequential or hierarchical
# t_visit_detail = metadata.tables['visit_detail']

# - [ ] @TODO: (2018-10-30) test CRUD operations on example table
# insert a list of dictionaries
patients = [fake.fake_it() for i in range(5)]

# Insert person level data
# ------------------------
fields_person = """
    person_id
    gender_concept_id
    year_of_birth
    race_concept_id
    ethnicity_concept_id""".split()

def insert_many(connection, _patients, _obj, _table, _fields):
    """Insert from patients into table

    Given a list of patient objects then extract person, spell or measurement
    level data and insert into appropriate table

    Arguments:
        connection {[type]} -- database connection
        table {[type]} -- target table object
        _patients {[type]} -- list of patient objects
        _fields {[type]} -- fields to be inserted
    """
    _rows = [{k: v for k, v in getattr(i, _obj).__dict__.items() if k in _fields}
           for i in _patients]
    import pdb; pdb.set_trace()
    ins = _table.insert()
    return connection.execute(ins, _rows)


result = insert_many(connection, patients, 'patient', t_person, fields_person)

# Insert spell (visit_occurence) level data
# -----------------------------------------
fields_visit = """
visit_occurrence_id
person_id
visit_concept_id
visit_start_date
visit_start_datetime
visit_end_date
visit_end_datetime
visit_type_concept_id
""".split()

result = insert_many(connection, patients, , fields_visit)

# - [ ] @TODO: (2018-10-30) # create fake data as pandas dataframe
# - [ ] @TODO: (2018-10-30) # write to database


def main():
    print('>>> Connecting vis DSN: {}'.format(DSN))
    print('>>> Person table columns: {}'.format(t_person.columns.keys()))
    print('>>> Mr Smith: {}'.format(patients[0].patient.__dict__))
    # print('>>> Visit table columns: {}'.format(t_visit.columns.keys()))
    # print('>>> Measurement table columns: {}'.format(t_measurement.columns.keys()))

    print('so far so good')


if __name__ == '__main__':
    main()
