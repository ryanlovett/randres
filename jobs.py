import numpy as np
import datetime
import pandas as pd

def get_jobs(curr_app, potential_addys, dob):

	# List of potential jobs
	fast_food =  ['McDonalds','KFC','Taco Bell','Pizza Hut','Wendys','Burger King','Subway','Dunkin Donuts']
	pharmacy =  ['Walgreens','CVS']
	retailers = ['Walmart','Target','Home Depot','Lowes','TJ Max','Best Buy']
	coffee = ['Starbucks',]
	delivery = ['FedEx', 'UPS']
	restaurants = ['Olive Garden', 'Cheesecake Factory', 'Dennys']
	car_share = ['Uber and Lyft']
	security = ['Securitas','Allied Univeral']

	# List of positions
	standard_positions = ['Team Member', 'Retail Associate', 'Cashier', 'Stocker', 'Customer Service Associate'] # Works for all but food
	food_positions = ['Crew Member', 'Cashier']
	coffee_positions = ['Barista']
	delivery_positions = ['Package Handler', 'Customer Service Associate', 'Delivery Driver / Courier']

	# Dictionaries for randomization
	jobs = {'fast_food':fast_food, 'pharmacy':pharmacy, 'retailers':retailers, 'coffee':coffee,
			'delivery':delivery, 'restaurants':restaurants, 'car_share':car_share, 'security':security}
	postions = {'fast_food':food_positions, 'coffee':coffee_positions, 'delivery':delivery_positions, 
				'restaurants':food_positions + ['Server'], 'car_share':['Driver'], 'security':['Security Officer']}

	supervisors = [
		'Jason English', 'Deja Benson', 'Maddox Galvan', 'Tiara Hudson', 'German Larsen', 'Averie Noble',
		'Skye Harris', 'Diana Herrera', 'Sammy Webb', 'Joanna Patton', 'Jessie Craig', 'Jeffery Pena',
		'Jamie Blair', 'Rex Warren', 'Makenzie Acevedo', 'Regan Durham', 'Jordin Newton', 'Zaid Harmon',
		'Allyson Kent', 'Cloe Shepard', 'Paisley George', 'Braydon Peck', 'Zachery Thornton', 'Cameron Dickerson',
		'Gaven Fritz','Braedon Montoya','Dorian Hanna','India Weeks','Vance Frey','Eli Fletcher','Laney Sims',
		'Davon Buckley','Amanda Gordon','Aniya Mitchell','Jimena Boyle','Erik Hawkins','Chad Black','Charlee Davila',
		'Deven Harvey','Monica Mccullough','Gustavo Briggs','Alexis Manning','Caleb Roberson','Mitchell Olson'
	]

	today = datetime.datetime.now()
	today_pd = pd.to_datetime("{}-{}-{}".format(today.day,today.month,today.year), format="%d-%m-%Y")
	dob = pd.to_datetime(dob, format="%m/%d/%Y")

	## Generate three yeras of jobs history
	njobs = np.random.choice(list(range(1,4)),1)[0]
	joblist = []
	sup_list = []
	existing_jobs = []
	for k in range(njobs):
		jobcat = np.random.choice(list(jobs.keys()),1)[0]
		job =  np.random.choice([k for k in jobs[jobcat] if k is not curr_app and k not in existing_jobs], 1)[0]
		existing_jobs += [job]
		try:
			pos = np.random.choice(postions[jobcat], 1)[0]
		except:
			pos = np.random.choice(standard_positions, 1)[0]
		addy = potential_addys.sample(1).values[0,0]
		sup = np.random.choice([k for k in supervisors if k not in sup_list], 1)[0]
		sup_list += [sup]
		if k == 0:
			tenure = np.random.choice(range(6,19),1)[0]
			start = "{}/{}".format((today_pd - pd.DateOffset(tenure,'months')).month, (today_pd - pd.DateOffset(tenure,'months')).year)
			end = "Present"
		else:
			tenure += np.random.choice(range(6,19),1)[0]
			if (today_pd - pd.DateOffset(tenure,'months')).dt.year - dob.dt.year <= 18: # Don't do more jobs for young kids
				break
			end = start
			start = "{}/{}".format((today_pd - pd.DateOffset(tenure,'months')).month, (today_pd - pd.DateOffset(tenure,'months')).year)
		joblist += [(job, pos, addy, sup, start, end)]

	return joblist


	# First job is a random choice for the last two years
	fjob = np.random.choice([k for k in potential_firms if k is not curr_app], 1)[0]
	fpos = np.random.choice(positions, 1)[0]
	faddy = potential_addys.sample(1).values[0,0]
	fsup = np.random.choice(supervisors, 1)[0]
	fstart = "{}/{}".format(today.month,today.year-2)
	fend = "Present"

	# Second job
	sjob = np.random.choice([k for k in potential_firms if k is not curr_app], 1)[0]
	spos = np.random.choice(positions, 1)[0]
	saddy = potential_addys.sample(1).values[0,0]
	ssup = np.random.choice([k for k in supervisors if k is not fsup], 1)[0]
	sstart = "{}/{}".format(today.month,today.year-3)
	send = "{}/{}".format(today.month,today.year-2)

	return [(fjob, fpos, faddy, fsup, fstart, fend),
			(sjob, spos, saddy, ssup, sstart, send)]