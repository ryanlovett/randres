from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import pandas as pd
import numpy as np
from db import get_db
from db import get_addy
from db import get_schlname, get_schladdress
from db import get_job_hist
from db import get_existing_names
from demos import get_name
from jobs import get_jobs
bp = Blueprint('generate', __name__, url_prefix='/generate')

# from twilio.rest import Client
# account_sid = 'AC81792c0f6bf476fc9e2ecb83ea8e12d5'
# with open('randres/static/tokens.txt') as tf:
#     auth_token = tf.readline().strip('\n')
# client = Client(account_sid, auth_token)

# numbers = client.available_phone_numbers("US").local.list(in_region="NY", sms_enabled=True, voice_enabled=True)
# phone_number = numbers[0].phone_number


# # voicemail twimlet
# vmail = "http://twimlets.com/voicemail?Email=randresmaster%40gmail.com&Message=The%20person%20you%20have%20called%20is%20currently%20unavailable.%20Please%20leave%20a%20message%20at%20the%20tone.&Transcribe=true&"
# client.incoming_phone_numbers.list()[0].update(voice_url=vmail)

# client.incoming_phone_numbers

# client.incoming_phone_numberscreate(
#     phone_number='',
#     voice_method='GET',
#     voice_url=vmail)

# country = client.pricing.phone_numbers.countries("US").fetch()
# for p in country.phone_number_prices:
#     print("{} {}".format(p['number_type'], p['current_price']))

# voicemail success
# https://handler.twilio.com/twiml/EH4c343ddce2764170a30f30a06b83f9dd

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == "GET":
        job_id = request.args.get("job_id")
        firm = request.args.get("firm")
        return render_template('generate/create.html', job_id=job_id, firm=firm)

    if request.method == 'POST':
        job_id = request.form['job_id']
        race = request.form['race']
        gender = request.form['gender']
        firm = request.args.get("firm")

        # Allow for randomized race / gender
        if race == "Random":
            race = np.random.choice(['Black','White'],1)[0]
        
        if gender == "Random":
            gender = np.random.choice(['Male','Female'],1)[0]
              
        db = get_db()
        curs = db.cursor()
        error = None

        if not job_id:
            error = 'Job id is required.'

        if error is not None:
            flash(error)

        # Generate name based on data
        existing_names = get_existing_names(job_id)
        firstname, lastname, email = get_name(race,gender,existing_names)

        # Generate contact information
        phone = 4562311231

        # Generate social
        socials = db.execute('SELECT ssn from SSNS' 
                    ' ORDER BY RANDOM()'
                    ' LIMIT 1').fetchone()
        social = [s for s in socials][0]

        # Pull all addresses for state where job is located
        job_state, job_zip = db.execute('SELECT state, zipcode FROM job WHERE id = ?',
                (job_id,) ).fetchone()

        potential_addys = db.execute(
            'SELECT id, numb, street, city, region, zip'
            ' FROM addy WHERE region = ?', (job_state,) )
        potential_addys = pd.DataFrame(potential_addys.fetchall())

        # Sample addresses within 1k of jobzip
        close_addys = potential_addys.loc[np.abs(potential_addys[5] - job_zip) <= 1000]
        if close_addys.shape[0] <= 1000:
            close_addys = potential_addys

        # Address
        addy_id = close_addys.sample(1).values[0,0]

        # Pull all the schools from the state
        potential_schls = db.execute(
            'SELECT id, name, state, zip'
            ' FROM schl WHERE state = ?', (job_state,) )
        potential_schls = pd.DataFrame(potential_schls.fetchall())

        # Sample schools within 1k of jobzip
        close_schls = potential_schls.loc[np.abs(potential_schls[3] - job_zip) <= 1000]
        if close_schls.shape[0] <= 1000:
            close_schls = potential_schls

        # Actual schl
        schl_id = close_schls.sample(1).values[0,0]

        # Age -- get random date between 1980 and 2000
        dob = "{}/{}/{}".format(np.random.choice(range(1,13),1)[0],
                        np.random.choice(range(1,28),1)[0],
                        np.random.choice(range(1980,2000),1)[0])
        grad_year = pd.to_datetime(dob, format="%m/%d/%Y").year + 18             # Year you turn 18

        # Put into its table
        job_hist = get_jobs(firm, close_addys, dob) 

        # Other stuff
        pin = 5494
        over16 = True
        can_prove = True

        # Generate employment history (optional)
        # legal_work = True
        # responsibilities = 
        # reason_for_leaving = 

        # # References (optional, only years_known requires)
        # personal_or_professional = 
        # ref_first, ref_last, phone, years_known, street, city, state, zipcode

        # # Generate education history

        # # Misc
        # relatives = False # if yes, who
        # referal = False # if yes, who
        # how_hear = 'KFC Website'

        # # Behavior (not required)
        how_many_jobs = len(job_hist)
        ever_terminated = 0
        # explian = ""

        # Generate availability
        hours = 40
        available_all_week = 1
        notice = 'Less than two weeks'
        import datetime
        start_date = (datetime.date.today() + datetime.timedelta(1*365/12)).isoformat()

        # # Physical
        # can_lift_50 = True
        # can_spend_time_on_feet = True
        # specialized_training = ""
        # willing_to_look_ok = True
        # has_transport = True

        # Redirect
        details = (g.user['id'], job_id, firstname, lastname, gender, race, dob, phone, email,
                addy_id, hours, ever_terminated, available_all_week, notice, start_date, schl_id, grad_year, social)
        curs.execute(
            'INSERT INTO app (user_id, job_id, firstname, lastname, gender, race, dob, phone, email,'
            ' addy_id, hours, ever_terminated, available_all_week, notice, start_date, schl_id, grad_year, social)'
            ' VALUES ({})'.format(", ".join(["?" for k in details])),
            details
        )
        lastrow = curs.lastrowid                
        db.commit()

        # Insert job history
        for old_job in job_hist:
            db.execute(
                'INSERT INTO work_hist (app_id, employer, position, addy_id, supervisor, start, end)'
                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
                (lastrow,) + old_job
            )
        db.commit()
 
        # Dictionary with full details
        full_details = {
                'contact': [firstname, lastname, phone, "{}+{}@gmail.com".format(email,lastrow), get_addy(addy_id)],
                'demos': [gender, race, dob],
                'job_hist': get_job_hist(lastrow),
                'avail': [hours, available_all_week, notice, start_date],
                'schl': [get_schlname(schl_id), get_schladdress(schl_id), grad_year],
                'id':lastrow,
                'job_id':job_id,
                'firm':firm,
                'social': str(social),
        }
        return render_template('generate/show_app.html', details=full_details)

@bp.route('/delete', methods=('POST','GET'))
def delete():
    job = request.args.get("job_id")
    firm = request.args.get("firm") 

    if request.method == 'POST':
        id = request.args.get("id") 
        db = get_db()
        db.execute('DELETE FROM app WHERE id = ?', (id,))
        db.commit()
    return redirect(url_for('app_list', job_id=job, firm=firm))

@bp.route('/show_details', methods=('GET',))
def show_details():
    app_id = request.args.get('app_id')
    db = get_db()

    details = db.execute(
    'SELECT user_id, job_id, firstname, lastname, gender, race, dob, phone, email,'
            ' addy_id, hours, ever_terminated, available_all_week, notice, start_date,'
            ' schl_id, grad_year, social'
    ' FROM app WHERE id = {}'.format(app_id)
    ).fetchone()
    user_id, job_id, firstname, lastname, gender, race, dob, phone, email, addy_id, hours, ever_terminated, available_all_week, notice, start_date, schl_id, grad_year, social = details

    firm = db.execute('SELECT firm FROM job WHERE id = {}'.format(job_id)).fetchone()
    firm = "".join([x for x in firm])

    full_details = {
        'contact': [firstname, lastname, phone, "{}+{}@gmail.com".format(email,app_id), get_addy(addy_id)],
        'demos': [gender, race, dob],
        'job_hist': get_job_hist(app_id),
        'avail': [hours, available_all_week, notice, start_date],
        'schl': [get_schlname(schl_id), get_schladdress(schl_id), grad_year],
        'id':app_id,
        'job_id':job_id,
        'firm':firm,
        'social': str(social),       
        }
    print(full_details)
    return render_template('generate/show_app.html', details=full_details)




    # return render_template('generate/create.html', details=details)


        # elif db.execute(
        #     'SELECT id FROM user WHERE username = ?', (username,)
        # ).fetchone() is not None:
        #     error = 'User {} is already registered.'.format(username)

        # if error is None:
        #     db.execute(
        #         'INSERT INTO user (username, password) VALUES (?, ?)',
        #         (username, generate_password_hash(password))
        #     )
        #     db.commit()
        #     return redirect(url_for('auth.login'))

        # flash(error)

