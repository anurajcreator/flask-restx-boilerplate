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
        - Please run the file using Python version 3.9.10 or below. Requirements and Dependencies used in the project are not compatible with higher versions of python. To run a code with a specific version of python, use VS Code's **"Select Interpreter"** function.

- The setup will start to install the required dependencies for the project. This might take up to 5 minutes or more.

- At the __Name your Project:__ input box, type the **\<foldername\>** that you want your project to be in.

- After installation, cd into the folder by
    - > **cd \<foldername\>**
- Run the file: **run.ps1** by:
    - > **./run.ps1**
    - The files for linux systems will be coming soon.
    - In case of an error like this:
    - > **File C:\Users\<Username>\<App Name>\run.ps1 cannot be loaded because the execution of scripts is disabled on this system. Please see "get-help about_signing" for more details.**
    - Run Powershell as an administrator and execute the following command:
    - > **set-executionpolicy remotesigned**

- Alternatively, the environment can be manually activated by:

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

