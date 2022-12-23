# Flask RestX Api Boilerplate
Version Flask 2.0  
  
&nbsp;  

This is a boilerplate for any flask_restx application.  


### What's included?  
    - app
    - requirements.txt
    - manage.py

### What's not included?
    - Migrations
    - Database
    - Development environment (Read README)


### **_Prerequisites_**
>**Git**  

    - sudo apt install git  

>**Python3**  

    - sudo apt install python3  

>**Virtualenv**  

    - sudo apt install python3-virtualenv  

>**Pip**  

    - sudo apt install python3-pip  

>**python-as-python3**  

    - sudo apt install python-as-python3

>**python-dotenv**

    - pip install python-dotenv

>**flask-run**

    - bash
            $ export FLASK_APP=hello
            $ flask run
            * Running on http://127.0.0.1:5000/
    
    - powershell
            > $env:FLASK_APP = "hello"
            > flask run
            * Running on http://127.0.0.1:5000/
    
    - cmd  
            > set FLASK_APP=hello
            > flask run
            * Running on http://127.0.0.1:5000/

>**db-init**

    - flask db init

>**db-migrate**

    - flask db migrate

>**db-upgrade**

    - flask db upgrade
    
>**db-stam head updated (allembic update)
  
    - flask db stamp head


### _How to get started_?  
- Clone the repository using **git clone https://github.com/Cybertronian123/Api_Boilerplate.git**
- Make a new folder using  **mkdir \<foldername\>**
- Cd into the folder that you cloned **cd Api_Boilerplate/**
- Run the setup file **python3 setup.py**
- At the __Name of your Project:__ input box, type the **\<foldername\>** that you created
- Cd into the folder **cd \<foldername\>**
- Create the virtual environment: **virtualenv env**
- Activate the environment: **source env/bin/activate**
- Install the requirements: **pip install -r requirements.txt**
- Set FLASK_APP: 
    - bash
            $ export FLASK_APP=hello
    
    - powercell
            > $env:FLASK_APP = "hello"
    
    - cmd
            > set FLASK_APP=hello
    
- Initialise the database: **flask db init**
- Migrate the database: **flask db migrate --message 'inital migration'**
- Apply the migrations: **flask db upgrade**
- Run: **flask run**

