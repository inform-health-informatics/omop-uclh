import sqlalchemy as sa
from models.concept_tables import DataAccessLayer

# - [ ] @TODO: (2018-10-23) set these up as environment variables
connection_dict = {'user': 'postgres',
                   'host': 'localhost',
                   'port': 6543,
                   'password': 'postgres',
                   'database': 'TEST_SM'
                   }


dal = DataAccessLayer()
dal.db_init(connection_dict)

# - [ ] @TODO: (2018-10-23)  Confirms that the data base does not already ontain the tables in question
# inspect existing tables
inspector = sa.inspect(dal.engine)
inspector.get_table_names()

dal.build_from_vocab_csv(dal.concept, 'vocab/CONCEPT.csv' )
dal.build_from_vocab_csv(dal.vocabulary, 'vocab/VOCABULARY.csv' )
