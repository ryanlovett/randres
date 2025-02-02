DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS app;
DROP TABLE IF EXISTS addy;
DROP TABLE IF EXISTS job;
DROP TABLE IF EXISTS work_hist;
DROP TABLE IF EXISTS schl;
DROP TABLE IF EXISTS ssns;

CREATE TABLE user (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 username TEST UNIQUE NOT NULL
);

CREATE TABLE app (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 user_id INTEGER NOT NULL,
 job_id INTEGER NOT NULL,
 created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
 firstname TEXT NOT NULL,
 lastname TEXT NOT NULL,
 gender TEXT NOT NULL,
 race TEXT NOT NULL,
 dob TEXT NOT NULL,
 phone INTEGER NOT NULL,
 email TEXT NOT NULL,
 addy_id INTEGER NOT NULL,
 hours INTEGER NOT NULL,
 ever_terminated INTEGER NOT NULL,
 available_all_week INTEGER NOT NULL,
 notice TEXT NOT NULL,
 start_date TEXT NOT NULL,
 schl_id INTEGER NOT NULL,
 grad_year INTEGER NOT NULL,
 social INTEGER NOT NULL,
 FOREIGN KEY (user_id) REFERENCES user (id),
 FOREIGN KEY (job_id) REFERENCES job (id),
 FOREIGN KEY (addy_id) REFERENCES addy (id),
 FOREIGN KEY (schl_id) REFERENCES schl (id)
);

CREATE TABLE work_hist (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 app_id INTEGER NOT NULL,
 employer TEXT NOT NULL,
 position TEXT NOT NULL,
 addy_id INTEGER NOT NULL,
 supervisor TEXT NOT NULL,
 start TEXT NOT NULL,
 end TEXT NOT NULL,
 FOREIGN KEY (app_id) REFERENCES app (id),
 FOREIGN KEY (addy_id) REFERENCES addy (id) 
);

CREATE TABLE addy (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 numb INTEGER NOT NULL,
 street TEXT NOT NULL,
 unit TEXT NOT NULL,
 city TEXT NOT NULL,
 region TEXT NOT NULL,
 zip INTEGER NOT NULL
);

CREATE TABLE ssns (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 ssn INTEGER NOT NULL
);

CREATE TABLE schl (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 street TEXT NOT NULL,
 city TEXT NOT NULL,
 state TEXT NOT NULL,
 zip INTEGER NOT NULL
);

CREATE TABLE job (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 firm TEXT NOT NULL,
 city TEXT NOT NULL,
 state TEXT NOT NULL,
 street TEXT NOT NULL,
 zipcode INTEGER NOT NULL,
 link TEXT NOT NULL,
 user_id INTEGER NOT NULL,
 created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, 
 FOREIGN KEY (user_id) REFERENCES user (id) 
);

INSERT INTO user (username) VALUES ("ekrose");
INSERT INTO user (username) VALUES ("pkline");
INSERT INTO user (username) VALUES ("crwalters");

INSERT INTO job (firm, city, state, street, zipcode, link, user_id) VALUES 
	("KFC", "Excelsior Springs", "MO", "1744 West Jesse James Road", 64024,
		"https://jobs.kfc.com/job?id=450fa414-4f72-4f45-b817-a752013adce1", 1);

INSERT INTO job (firm, city, state, street, zipcode, link, user_id) VALUES 
	("Target", "Tucson", "AZ", "3699 e broadway blvd", 85716,
		"https://jobs.target.com/job/tucson/sales-floor-team-member/1118/11428510", 1);	
