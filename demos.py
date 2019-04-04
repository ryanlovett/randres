import numpy as np

def get_name(race, gend):
	names = {'White': {
				'Female': ['Allison', 'Anne', 'Carrie', 'Emily', 'Jill', 'Laurie', 'Kristen',
	        	           'Meredith', 'Sarah'],
	       		'Male': ['Brad', 'Brendan', 'Geoffrey', 'Greg', 'Brett', 'Jay', 'Matthew',
	    			     'Neil', 'Todd'],
	       		'Last': ['Stoltzfus', 'Byler', 'Hershberger', 'Troyer', 'Yoder',
	  				     'Burkholder', 'Hostetler', 'Graber', 'Mast', 'Roush'],
					},
			 'Black': {
			 	'Female': ['Aisha', 'Ebony', 'Keisha', 'Kenya', 'Latonya', 'Lakisha',
      					   'Latoya', 'Tamika', 'Tanisha'],
			 	'Male': ['Darnell', 'Hakim', 'Jermaine', 'Kareem', 'Jamal', 'Leroy',
    				     'Rasheed', 'Tremayne', 'Tyrone'],
			 	'Last': ['Smalls', 'Washington', 'Pierre', 'Muhammad', 'Hairston', 'Ruffin',
      					 'Alston', 'Chatman', 'Francois', 'Battle']
			 		}		
			}

	try: 
		return np.random.choice(names[race][gend],1)[0], np.random.choice(names[race]['Last'],1)[0]
		raise ValueError('Race or gender category not valid.')	
	except Exception as e:
		return e 
