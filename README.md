                         /$$$$$$$$/$$                     /$$                                  
                        | $$_____/ $$                    | $$                                  
                        | $$     | $$  /$$$$$$   /$$$$$$$| $$   /$$                            
                        | $$$$$  | $$ |____  $$ /$$_____/| $$  /$$/                            
                        | $$__/  | $$  /$$$$$$$|  $$$$$$ | $$$$$$/                             
                        | $$     | $$ /$$__  $$ \____  $$| $$_  $$                             
                        | $$     | $$|  $$$$$$$ /$$$$$$$/| $$ \  $$                            
                        |__/     |__/ \_______/|_______/ |__/  \__/                            
                     /$$$$$$$                       /$$    /$$   /$$                       
                    | $$__  $$                     | $$   | $$  / $$                       
                    | $$  \ $$  /$$$$$$   /$$$$$$$/$$$$$$ |  $$/ $$/                       
                    | $$$$$$$/ /$$__  $$ /$$_____/_  $$_/  \  $$$$/                        
                    | $$__  $$| $$$$$$$$|  $$$$$$  | $$     >$$  $$                        
                    | $$  \ $$| $$_____/ \____  $$ | $$ /$$/$$/\  $$                       
                    | $$  | $$|  $$$$$$$ /$$$$$$$/ |  $$$$/ $$  \ $$                       
                    |__/  |__/ \_______/|_______/   \___/ |__/  |__/                       
     /$$$$$$$            /$$ /$$                              /$$              /$$               
    | $$__  $$          |__/| $$                             | $$             | $$                
    | $$  \ $$  /$$$$$$  /$$| $$  /$$$$$$   /$$$$$$  /$$$$$$ | $$  /$$$$$$   /$$$$$$    /$$$$$$    
    | $$$$$$$  /$$__  $$| $$| $$ /$$__  $$ /$$__  $$/$$__  $$| $$ |____  $$ |_  $$_/   /$$__  $$ 
    | $$__  $$| $$  \ $$| $$| $$| $$$$$$$$| $$  \__/ $$  \ $$| $$  /$$$$$$$   | $$    | $$$$$$$$  
    | $$  \ $$| $$  | $$| $$| $$| $$_____/| $$     | $$  | $$| $$ /$$__  $$   | $$ /$$| $$_____/  
    | $$$$$$$/|  $$$$$$/| $$| $$|  $$$$$$$| $$     | $$$$$$$/| $$|  $$$$$$$   |  $$$$/|  $$$$$$$   
    |_______/  \______/ |__/|__/ \_______/|__/     | $$____/ |__/ \_______/    \___/   \_______/ 
                                                   | $$
                                                   |_$$                                                
# Flask RestX Api Boilerplate
Flask Version: 2.0  
  
&nbsp;  

This is a boilerplate for any flask_restx api based web application backend. This has been developed as a passion project by **anurajcreator** and **Cybertronian123**.  


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
    
>**db-stamp head updated (allembic update)**
  
    - flask db stamp head


### _How to get started_?  
- Clone the repository using **git clone https://github.com/anurajcreator/flask-restx-boilerplate**
- Cd into the folder that you cloned 
    - >**cd flask-restx-boilerplate/**
- Run the setup file by
    - >**python3 setup.py**
    - **Note:**
        - Please run the file using Python version 3.9.10 or below. Requirements and Dependencies used in the project are not compatible with higher versions of python. To run a code with a specific version of python, use VS Code's **"Select Interpreter"** function or edit the **PATH** System Environment Variable to include the preferred version on top of the list and restart your pc(Windows).

- The setup will start to install the required dependencies for the project. This might take up to 5 minutes or more.

- At the __Name your Project:__ input box, type the **\<foldername\>** that you want your project to be in.

- After installation, cd into the folder by
    - > **cd \<foldername\>**

- The environment can be manually activated by:

    - > **.\venv\Scripts\activate.ps1**

- And the app can be run by:

    - > **flask run**

- The database and response encryption private keys will be generated. After testing the app on port 5000, **Ctrl + C** to close the server.

- Set FLASK_APP(When no development env is created!): 
    - bash
            $ export FLASK_APP=hello
    
    - powercell
            > $env:FLASK_APP = "hello"
    
    - cmd
            > set FLASK_APP=hello
    
- Initialise the database: 
    - > **flask db init**
- Migrate the database:
    - >  **flask db migrate --message 'inital migration'**
- Apply the migrations: 
    - > **flask db upgrade**
- Run: 
    - > **flask run**


### _Congratulations

> **If you get the following output upon running:**

    > flask run

    * Environment: development
    * Debug mode: on
    * Debugger is active!
    * Debugger PIN: 101-351-714
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)


Then you've successfully created your application. Thanks for using flask-restx-boilerplate



