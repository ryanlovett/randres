import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
import csv, codecs

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

def get_addy(id):
    db = get_db()

    addy = db.execute(
            'SELECT numb, street, city, region, zip'
            ' FROM addy WHERE id = ? ORDER BY id DESC', (id,)
            ).fetchone()
    return  " ".join([str(x) for x in addy])

def get_job_hist(app_id):
    db = get_db()

    hist = db.execute(
            'SELECT employer, position, addy_id, supervisor, start, end'
            ' FROM work_hist WHERE app_id = ? ORDER BY id DESC', (app_id,)
            ).fetchall()
    hist = [list(x) for x in hist]
    for job in hist:
        job[2] = get_addy(job[2])
    return hist

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    import pkg_resources
    resource_package = "randres"  # Could be any module/package name
    addy_list = pkg_resources.resource_filename(resource_package, '/'.join(('assets', 'address_sample.csv')))
    with open(addy_list) as fin: 
        dr = csv.DictReader(fin) 
        for i in dr:
            print(i['number'], i['street'], i['unit'], i['city'], i['region'], i['zipcode']) 
            db.execute("INSERT INTO addy (numb, street, unit, city, region, zip) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (i['number'], i['street'], i['unit'], i['city'], i['region'], i['zipcode']))
        db.commit()

    # Add the school list
    schl_list = pkg_resources.resource_filename(resource_package, '/'.join(('assets', 'schl_sample.csv')))
    with open(schl_list) as fin: 
        dr = csv.DictReader(fin) 
        for i in dr:
            print(i['LSTATE09'], i['SCHNAM09'], i['LZIP09']) 
            db.execute("INSERT INTO schl (name, state, zip) "
                            "VALUES (?, ?, ?)",
                            (i['LSTATE09'], i['SCHNAM09'], i['LZIP09']))
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
