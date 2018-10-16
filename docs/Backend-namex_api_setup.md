# Backend namex/api setup

1. Follow instructions from https://github.com/bcgov/namex/blob/master/docs/developer.md first

2. Install PyCharm
	- download JetBrains Toolbox
	- create acount (if student create free account, otherwise start 30 day free trail)
	- open JetBrains Toolbox and install PyCharm

3. Open new project in PyCharm	
	- open PyCharm
	- File > New Project (select api folder from within your local namex)

4. Set project interpreter/venv in PyCharm
	- **Windows:** File > default settings > Project Interpreter
	- **Mac OS:** Pycharm > Preferences >  Project: docs > Project Interpreter
	- Press wheel beside project interpreter drop down field > add
	- Select location as new empty folder within api (name folder venv)
	- Select base interpreter as python 3.6
		 - If you don't have python 3.6 installed, and you don't want to update the system python, install pyenv:
		        
		        > pip install pyenv
		        > pyenv install 3.6.x
           (e.g. 3.6.6)
          - Add the new interpreter by finding it within the ~/.pyenv directory; 
           Then you will be able to select it in the list.
	- Press okay

5. Install requirements in "requirements.txt"
	- a banner should have appeared in your project window after setting up your venv asking you to install these
	- click install

6. Create postgres database named "namex"

7. Get .env file from developer
	```
	- change username/password to your username/password in postgres
	- place .env in api folder (make sure it is named ".env")
	```

9. Run wsgi in PyCharm
	- select wsgi.py
	- select wsgi dropdown at top righthand corner of window > edit configurations
	- select '+' at top left corner > Flask Server
		```
		- name configuration
		- select script path
		- target = path to wsgi
		- Python Interpreter = Python 3.6 (venv)
		```

10. Create database tables
	- open terminal in PyCharm (view > tool windows > terminal)
		```sh
		python manage.py db upgrade
		```
	- list tables in postgres namex database (make sure tables were created)

11. Run api
	- open terminal in PyCharm
		```sh
		source .env (not needed if direnv working)
		python config.py
		flask run
		```
