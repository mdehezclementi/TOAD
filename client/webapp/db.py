import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from . import crypto_utils as cu


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
    
    table = [
        ['0','0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d','0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1'], 
        ['1','0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1','0xFFcf8FDEE72ac11b5c542428B35EEF5769C409f0'], 
        ['2','0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c','0x22d491Bde2303f2f43325b2108D26f1eAbA1e32b'], 
        ['3','0x646f1ce2fdad0e6deeeb5c7e8e5543bdde65e86029e2fd9fc169899c440a7913','0xE11BA2b4D45Eaed5996Cd0823791E0C93114882d'],
        ['4','0xadd53f9a7e588d003326d1cbf9e4a43c061aadd9bc938c843a79e7b4fd2ad743','0xd03ea8624C8C5987235048901fB614fDcA89b117'], 
        ['5','0x395df67f0c2d2d9fe1ad08d1bc8b6627011959b79c53d7dd6a3536a33ab8a4fd','0x95cED938F7991cd0dFcb48F0a06a40FA1aF46EBC'], 
        ['6','0xe485d098507f54e7733a205420dfddbe58db035fa577fc294ebd14db90767a52','0x3E5e9111Ae8eB78Fe1CC3bb8915d5D461F3Ef9A9'],
        ['7','0xa453611d9419d0e56f499079478fd72c37b251a94bfde4d19872c44cf65386e3','0x28a8746e75304c0780E011BEd21C72cD78cd535E'], 
        ['8','0x829e924fdf021ba3dbbc4225edfece9aca04b929d6e75613329ca6f1d31c0bb4','0xACa94ef8bD5ffEE41947b4585a84BdA5a3d3DA6E'], 
        ['9','0xb0057716d5917badaf911b193b12b910811c1497b5bada8d7711f758981c3773','0x1dF62f291b2E969fB0849d99D9Ce41e2F137006e'],
        # ['10','0x77c5495fbb039eed474fc940f29955ed0531693cc9212911efd35dff0373153f','0x610Bb1573d1046FCb8A70Bbbd395754cD57C2b60'],
        # ['11','0xd99b5b29e6da2528bf458b26237a6cf8655a3e3276c1cdc0de1f98cefee81c01','0x855FA758c77D68a04990E992aA4dcdeF899F654A'],
        # ['12','0x9b9c613a36396172eab2d34d72331c8ca83a358781883a535d2941f66db07b24','0xfA2435Eacf10Ca62ae6787ba2fB044f8733Ee843'],
        # ['13','0x0874049f95d55fb76916262dc70571701b5c4cc5900c0691af75f1a8a52c8268','0x64E078A8Aa15A41B85890265648e965De686bAE6'],
        # ['14','0x21d7212f3b4e5332fd465877b64926e3532653e2798a11255a46f533852dfe46','0x2F560290FEF1B3Ada194b6aA9c40aa71f8e95598'],
        # ['15','0x47b65307d0d654fd4f786b908c04af8fface7710fc998b37d219de19c39ee58c','0xf408f04F9b7691f7174FA2bb73ad6d45fD5d3CBe'],
        # ['16','0x66109972a14d82dbdb6894e61f74708f26128814b3359b64f8b66565679f7299','0x66FC63C2572bF3ADD0Fe5d44b97c2E614E35e9a3'],
        # ['17','0x2eac15546def97adc6d69ca6e28eec831189baa2533e7910755d15403a0749e8','0xF0D5BC18421fa04D0a2A2ef540ba5A9f04014BE3'],
        # ['18','0x2e114163041d2fb8d45f9251db259a68ee6bdbfd6d10fe1ae87c5c4bcd6ba491','0x325A621DeA613BCFb5B1A69a7aCED0ea4AfBD73A'],
        # ['19','0xae9a2e131e9b359b198fa280de53ddbe2247730b881faae7af08e567e58915bd','0x3fD652C93dFA333979ad762Cf581Df89BaBa6795'],
        
    ]

    for e in table:
        db.execute(
                'INSERT INTO user (username, private_key, account_address) VALUES (?, ?, ?)',
                (e[0], e[1], e[2])
            )
        pk_x, pk_y = cu.compute_public_key(e[1])
        db.execute(
                "INSERT INTO eth_public_key (account_address, pk_x, pk_y) VALUES (?,?,?)",
                [e[2], hex(pk_x), hex(pk_y)]
        )
        db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')



def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

