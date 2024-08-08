import os, shutil, errno, subprocess
from time import sleep


POWERSHELL_PATH = "powershell.exe"


def setup_project():
    '''
    Sets Up the Flask_RestX-Boilerplate for a new project:

    Required Parameters: Project Name
    '''
    print('''
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
                                                                                                                                        
    \n\n\n''')
    print("Welcome to Flask-RestX-Boilerplate Setup:")
    print("Please name your project: >")
    project_name  = input()

    src = os.path.dirname(os.path.abspath('setup.py')) + "/app"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/app" 

    error_oc = False

    try:
        shutil.copytree(src, dest)
    except OSError as err:
    
        # error caused if the source was not a directory
        if err.errno == errno.ENOTDIR:
            shutil.copy2(src, dest)
        else:
            print("Error: % s" % err)
            error_oc = True
    try:
        print("Making Git Repository")
        sleep(2)
        src =  os.path.dirname(os.path.abspath('setup.py')) + "/.gitignore"
        dest =  os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/.gitignore" 
        shutil.copy2(src, dest)
        print("Copying WSGI Application")
        sleep(2)
        src =  os.path.dirname(os.path.abspath('setup.py')) + "/manage.py"
        dest =  os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/wsgi.py" 

        print("Copying Requirements")
        sleep(2)
        shutil.copy2(src, dest)
        src = os.path.dirname(os.path.abspath('setup.py')) + "/requirements.txt"
        dest = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/requirements.txt"
        shutil.copy2(src, dest)

        print("Copying Environment Files")
        sleep(2)
        src = os.path.dirname(os.path.abspath('setup.py')) + "/.env.example"
        dest = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/.env"
        shutil.copy2(src, dest)


        print("Setup Install Script. Please run install.ps1 post setup if it doesn't automatically run.")
        sleep(3)
        src = src = os.path.dirname(os.path.abspath('setup.py')) + "/install.ps1"
        dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/install.ps1" 
        shutil.copy2(src, dest)

        fp = open('filename', 'w')
        fp.write(f'{project_name}')
        fp.close()

        print("Temporarily copying Project Name")
        sleep(2)
        src = os.path.dirname(os.path.abspath('setup.py')) + "/filename"
        dest = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/filename"
        shutil.copy2(src, dest) 

        print("Copying startup script (run.ps1). Please run post install.ps1 if it doesn't automatically run.")
        sleep(2)

        src = os.path.dirname(os.path.abspath('setup.py')) + "/run.ps1"
        dest = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/run.ps1"
        shutil.copy2(src, dest)
    except OSError as err:
        print("Error: % s" % err)
        error_oc = True


    if error_oc:
        print("Some error ocurred! Project might be broken!")
    else:
        print(f"All good! Project created in: ../{project_name}/")

    return project_name, error_oc



def run_ps_script(script_path, *params):
    try:
        commandline_options = [POWERSHELL_PATH, '-ExecutionPolicy', 'unrestricted', script_path]
        for param in params:
            commandline_options.append("'" + param + "'")

        process_result = subprocess.run(commandline_options, stdout = subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        print("Script Execution Status: \n")
        print(process_result.returncode)
        print(process_result.stdout)
        print(process_result.stderr)

        if process_result.returncode == 0:
            Message = "Success"
        else:
            Message = "Fail"

        return Message, None
    except Exception as e:
        return "Fail", e
    


def __init__(self, **kwargs):
    try:
        project_name, setup_status = setup_project()

        if setup_status == False:

            print("Running Install Script... Please Wait!")
            install_script_list = os.path.dirname(os.path.abspath('setup.py')).split("\\")[0:len(os.path.dirname(os.path.abspath('setup.py')).split("\\"))-1]
            install_loc = ""
            for item in install_script_list:
                install_loc += str(item)+"\\\\"

            install_loc+=str(project_name)+"install.ps1"

            install_status, install_error = run_ps_script(install_loc)

            if install_status == "Success":
                print("\n__________________________________________________________\nInstall Script Successfully Completed!\n__________________________________________________________\n")
                print("Running Post-Install Test Script.... Please Wait!")
                run_script_list = os.path.dirname(os.path.abspath('setup.py')).split("\\")[0:len(os.path.dirname(os.path.abspath('setup.py')).split("\\"))-1]
                run_loc = ""
                for item in run_script_list:
                    run_loc += str(item)+"\\\\"

                run_loc+=str(project_name)+"run.ps1"

                run_status, run_error = run_ps_script(run_loc)

                if run_status == "Success":
                    print("\n__________________________________________________________\nPost Install has been successfully completed! You can run your project now!\n__________________________________________________________\n")
                else:
                    print("\n__________________________________________________________\nPost Install has failed! You can't run your project! Please troubleshoot!\n__________________________________________________________\n")

            else:
                print("\n__________________________________________________________\nInstall Script Failed! Aborting! \n Error: "+ install_error +"\n__________________________________________________________\n")   

        else:
            print("\n__________________________________________________________\nProject Setup Failed!\n__________________________________________________________\n")

    except Exception as e:
        print(f"\n__________________________________________________________\nSystem Error: \n{e}\n__________________________________________________________\n")









