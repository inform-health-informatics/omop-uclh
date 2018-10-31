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
patients = [fake.fake_it(seed=i) for i in range(5)]
fields_person = """
    person_id
    gender_concept_id
    year_of_birth
    race_concept_id
    ethnicity_concept_id""".split()
persons = [{k: v for k, v in i.patient.__dict__.items() if k in fields_person}
           for i in patients]
ins = t_person.insert()
result = connection.execute(ins, persons)
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
