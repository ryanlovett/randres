import numpy as np
import datetime

def get_jobs(curr_app, potential_addys):

	potential_firms = ['McDonalds','Target','KFC','Walmart']
	positions = ['Team Member', 'Retail Associate']
	supervisors = ['Hillary Saez', 'Jesse Handle', 'David Walters', 'Supreet Moretti', 'Fred Kline']

	today = datetime.datetime.now()

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