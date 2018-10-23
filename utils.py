
def gen_connection_string(d):
    """Generates a SQLAlchemy connection string from a dictionary"""
    # e.g. # engine = create_engine('postgresql+psycopg2://steve@localhost:5432/omop')
    # TODO @later permit other interfaces
    d['port'] = str(d['port'])
    # with passwordd
    if 'password' in d.keys():
        if len(d['password']):
            connection_string = 'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'.format(
                **d)
    else:
        # no password
        connection_string = 'postgresql+psycopg2://{user}@{host}:{port}/{database}'.format(
            **d)
    return connection_string


