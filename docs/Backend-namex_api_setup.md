# Backend namex/api setup

1. Follow instructions from namex/docs/developer.md first

2. Install PyCharm

3. Create new project in PyCharm	
	- open PyCharm
	- File > New Project (select api folder from within your local namex)

4. Set project interpreter/venv in PyCharm
	- File > default settings > Project Interpreter
		```
		- press wheel beside project interpreter drop down field > add
		- select location as new empty folder within api (name folder venv)
		- select base interpreter as python 3.6
		- press okay
		```

5. Install requirments in "requirements.txt"
	- a banner should have appeared in your project window after setting up your venv asking you to install these
	- click install

6. Change "config.py"
	```
	- change "from dotenv import load_dotenv" to "from dotenv import load_dotenv, find_dotenv"
	- change "load_dotenv()" to "load_dotenv(find_dotenv())"
	```

7. Create postgres database named "namex"

8. Get .env file from developer
	```
	- change username/password to your username/password in postgres
	- place .env in api folder (make sure it is named ".env")
	```

9. Get "client_secrets.dev.json" file from developer
	- place in "client_secrets" folder

10. Run wsgi in PyCharm
	- select wsgi.py
	- select wsgi dropdown at top righthand corner of window > edit configurations
	- select '+' at top left corner > Flask Server
		```
		- name configuration
		- select script path
		- target = path to wsgi
		- Python Interpreter = Python 3.6 (venv)
		```

11. Create database tables
	- open terminal in PyCharm (view > tool widndows > terminal)
		```sh
		python manage.py db upgrade
		```
	- list tables in postgres namex database (make sure tables were created)

12. Run api
	- open terminal in PyCharm
		```sh
		source .env (not needed if direnv working)
		python config.py
		flask run
		```
