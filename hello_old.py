from flask import Flask, request, session, url_for, render_template, g, flash, redirect
import os, functools
import db

def create_app():
	# Configurations
	application = Flask(__name__)
	application.config.from_mapping(
		SECRET_KEY='dev',
		DATABASE='instance/randres.sqlite',
	)
	application.debug=True
	
	import generate
	application.register_blueprint(generate.bp)

	def login_required(view):
	    @functools.wraps(view)
	    def wrapped_view(**kwargs):
	        if g.user is None:
	            return redirect(url_for('login'))

	        return view(**kwargs)

	    return wrapped_view

	db.init_app(application)

	# Landing page
	@application.route('/')
	def index():
		if g.user is None:
			return render_template('base.html')
		else:
		    dbase = db.get_db()
		    jobs = dbase.execute(
		        'SELECT id, firm, city, state, street, zipcode, link, created'
		        ' FROM job ORDER BY id DESC'
		    ).fetchall()
		    return render_template('job_list.html', jobs=jobs)

	# Job creation
	@application.route('/create_job', methods=('GET', 'POST'))
	@login_required
	def create_job():
	    if request.method == 'POST':
	        firm = request.form['firm']
	        city = request.form['city']
	        state = request.form['state']
	        street = request.form['street']
	        zipcode = request.form['zipcode']
	        link = request.form['link']
	        error = None

	        if None in [firm, city, state, street, zipcode, link]:
	            error = 'All fields are required.'
	        if error is not None:
	            flash(error)
	        else:
	            dbase = db.get_db()
	            dbase.execute(
	                'INSERT INTO job (firm, city, state, street, zipcode, link, user_id)'
	                ' VALUES (?, ?, ?, ?, ?, ?, ?)',
	                (firm, city, state, street, zipcode, link, g.user['id'])
	            )
	            dbase.commit()
	            return redirect(url_for('index'))

	    return render_template('create_job.html')


	@application.route('/app_list', methods=('GET', 'POST'))
	def app_list():
		if g.user is None:
			return render_template('base.html')
		else:
		    dbase = db.get_db()
		    job = request.args.get("job_id")
		    firm = request.args.get("firm")
		    apps = dbase.execute(
		        'SELECT id, firstname, lastname, created'
		        ' FROM app WHERE job_id = {} ORDER BY id DESC'.format(job)
		    ).fetchall()
		    return render_template('app_list.html', apps=apps, job_id=job, firm=firm)

	@application.route('/register', methods=('GET', 'POST'))
	def register():
	    if request.method == 'POST':
	        username = request.form['username']
	        dbase = db.get_db()
	        error = None

	        if not username:
	            error = 'Username is required.'
	        elif dbase.execute(
	            'SELECT id FROM user WHERE username = ?', (username,)
	        ).fetchone() is not None:
	            error = 'User {} is already registered.'.format(username)

	        if error is None:
	            dbase.execute(
	                'INSERT INTO user (username) VALUES (?)', (username,)
	            )
	            dbase.commit()
	            return redirect(url_for('login'))

	        flash(error)

	    return render_template('register.html')

	@application.route('/login', methods=('GET', 'POST'))
	def login():
	    if request.method == 'POST':
	        username = request.form['username']
	        dbase = db.get_db()
	        error = None
	        user = dbase.execute(
	            'SELECT * FROM user WHERE username = ?', (username,)
	        ).fetchone()

	        if user is None:
	            error = 'Username does not exist.'

	        if error is None:
	            session.clear()
	            session['user_id'] = user['id']
	            return redirect(url_for('index'))

	        flash(error)

	    return render_template('login.html')    

	@application.route('/logout')
	def logout():
	    session.clear()
	    return redirect(url_for('index'))

	@application.before_request
	def load_logged_in_user():
	    user_id = session.get('user_id')

	    if user_id is None:
	        g.user = None
	    else:
	        g.user = db.get_db().execute(
	            'SELECT * FROM user WHERE id = ?', (user_id,)
	        ).fetchone()	    

	return application

# Make the app
app = create_app()

if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.debug = True
    app.run()