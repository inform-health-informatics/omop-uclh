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

dal.build_from_vocab_csv(dal.concept, 'vocab/CONCEPT.csv')
dal.build_from_vocab_csv(dal.vocabulary, 'vocab/VOCABULARY.csv')
dal.build_from_vocab_csv(dal.domain, 'vocab/domain.csv')
dal.build_from_vocab_csv(dal.concept_class, 'vocab/concept_class.csv')
dal.build_from_vocab_csv(dal.concept_relationship, 'vocab/concept_relationship.csv')
dal.build_from_vocab_csv(dal.relationship, 'vocab/relationship.csv')
dal.build_from_vocab_csv(dal.concept_synonym, 'vocab/concept_synonym.csv')
dal.build_from_vocab_csv(dal.concept_ancestor, 'vocab/concept_ancestor.csv')

# No such table in vocab; deprecated mapping; should be using CONCEPT_RELATIONSHIP
# dal.build_from_vocab_csv(dal.source_to_concept_map, 'vocab/source_to_concept_map.csv' )

# No vocab files
dal.build_from_vocab_csv(dal.cohort_definition, 'vocab/cohort_definition.csv')
dal.build_from_vocab_csv(dal.attribute_definition, 'vocab/attribute_definition.csv')
