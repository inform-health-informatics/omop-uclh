
def foo():
    pass

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
