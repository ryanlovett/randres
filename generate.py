from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
import pandas as pd
from db import get_db
from db import get_addy
from db import get_job_hist
from demos import get_name
from jobs import get_jobs

bp = Blueprint('generate', __name__, url_prefix='/generate')

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
       
        db = get_db()
        curs = db.cursor()
        error = None

        if not job_id:
            error = 'Job id is required.'

        if error is not None:
            flash(error)

        # Generate name based on data
        firstname, lastname = get_name(race,gender)

        # Generate contact information
        phone = 4562311231
        email = "ekrose+spam@gmail.com"

        # Pull all addresses for state where job is located
        job_state, job_zip = db.execute('SELECT state, zipcode FROM job WHERE id = ?',
        		(job_id,) ).fetchone()

        potential_addys = db.execute(
        	'SELECT id, numb, street, city, region, zip'
        	' FROM addy WHERE region = ?', (job_state,) )
        potential_addys = pd.DataFrame(potential_addys.fetchall())

        # Address
        addy_id = potential_addys.sample(1).values[0,0]

        # Age -- get random date between 1980 and 2000
        dob = "{}/{}/{}".format(np.random.choice(range(1,13),1)[0],
                        np.random.choice(range(1,28),1)[0],
                        np.random.choice(range(1980,2000),1)[0])
        graduation_year = pd.to_datetime(dob, format="%m/%d/%Y").year + 18             # Year you turn 18

        # Put into its table
        job_hist = get_jobs(firm, potential_addys, dob) 

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
        		addy_id, hours, ever_terminated, available_all_week, notice, start_date)
        curs.execute(
            'INSERT INTO app (user_id, job_id, firstname, lastname, gender, race, dob, phone, email,'
        	' addy_id, hours, ever_terminated, available_all_week, notice, start_date)'
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
        		'contact': [firstname, lastname, phone, email, get_addy(addy_id)],
        		'demos': [gender, race, dob],
        		'job_hist': get_job_hist(lastrow),
        		'avail': [hours, available_all_week, notice, start_date]
        }
        return render_template('generate/show_app.html', details=full_details)

@bp.route('/show_details', methods=('GET',))
def show_details():
	app_id = request.args.get('app_id')
	db = get_db()

	details = db.execute(
	'SELECT user_id, job_id, firstname, lastname, gender, race, dob, phone, email,'
        	' addy_id, hours, ever_terminated, available_all_week, notice, start_date'
	' FROM app WHERE id = {}'.format(app_id)
	).fetchone()

	user_id, job_id, firstname, lastname, gender, race, dob, phone, email, addy_id, hours, ever_terminated, available_all_week, notice, start_date = details
	full_details = {
		'contact': [firstname, lastname, phone, email, get_addy(addy_id)],
		'demos': [gender, race, dob],
		'job_hist': get_job_hist(app_id),
        'avail': [hours, available_all_week, notice, start_date]		
		}
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

