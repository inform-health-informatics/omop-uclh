# reload(utils.utils)
import re
from utils.utils import gen_connection_string, build_from_vocab_csv, clean_start
import psycopg2

# - [ ] @TODO: (2018-10-23) set these up as environment variables
connection_dict = {'user': 'uclh',
                   'host': 'localhost',
                   'port': 55432,
                   'password': 'uclh',
                   'database': 'OMOPUCLH'
                   }
DSN = gen_connection_string(connection_dict, engine='psycopg2')
force = True

if force:
    clean_start(DSN, force)

# - [ ] @TODO: (2018-10-25) convert to git submodule or pull specific commit
# The order is important
CDM_files_path = 'CommonDataModel/PostgreSQL/'
CDM_files_names = """
OMOP CDM postgresql ddl.txt
OMOP CDM postgresql indexes.txt
OMOP CDM postgresql constraints.txt
""".splitlines()[1:]

VOCAB_files_path = 'vocab/'
VOCAB_file_names = """
CONCEPT.csv
CONCEPT_ANCESTOR.csv
CONCEPT_CLASS.csv
CONCEPT_RELATIONSHIP.csv
CONCEPT_SYNONYM.csv
DOMAIN.csv
DRUG_STRENGTH.csv
RELATIONSHIP.csv
VOCABULARY.csv
""".splitlines()[1:]  # drop empty first line from docstring


# Create tables and populate with vocab BEFORE applying indices and constraints
# =============================================================================
# Create empty tables
file_name = CDM_files_names[0]
fp = CDM_files_path + file_name
with open(fp, 'r') as f:
    SQL = f.read()
    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as curs:
            rp = curs.execute(SQL)

# Load vocab
for file_name in VOCAB_file_names:
    fp = VOCAB_files_path + file_name
    vocab_table = file_name[:-4]  # drop '.csv'
    print('--- Loading {} into {}'.format(fp, vocab_table))
    try:
        build_from_vocab_csv(DSN, vocab_table.lower(), fp, force)
    except psycopg2.DataError as e:
        print('!!! FAILED loading {} into {}, {}'.format(fp, vocab_table, e))


# - [ ] @TODO: (2018-10-25) fails for drug_strength
# build_from_vocab_csv(DSN, 'drug_strength', 'vocab/DRUG_STRENGTH.csv', force)

# Create indices and constraints (remaining 2 files)
# Do this line by line to manage memory and disk space better?
def extract_SQL_from_file(fp):
    reSQL = re.compile(r'^\w.*;')
    with open(fp, 'r') as f:
        lines = f.read()
    return [i for i in lines.splitlines() if re.match(reSQL, i)]


def execute_SQL(DSN, SQL):
    print('--- Executing: {} '.format(SQL))
    with psycopg2.connect(DSN) as conn:
        with conn.cursor() as curs:
            try:
                curs.execute(SQL)
            except psycopg2.ProgrammingError as e:
                print('!!! ProgrammingError executing: {}, {}'.format(SQL, e))
            except psycopg2.OperationalError as e:
                print('!!! OperationalError executing: {}, {}'.format(SQL, e))
            except psycopg2.IntegrityError as e:
                print('!!! IntegrityError executing: {}, {}'.format(SQL, e))


for file_name in CDM_files_names[1:]:
    fp = CDM_files_path + file_name
    SQLs = extract_SQL_from_file(fp)
    [execute_SQL(DSN, SQL) for SQL in SQLs]
