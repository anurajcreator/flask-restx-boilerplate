import os, shutil, errno, subprocess, time, sys, itertools, threading

POWERSHELL_PATH = "powershell.exe"


def project_identity():
    try:
    
        project_name  = input("Please name your project: >")
        project_version = input("Project Version: >")
        project_description = input("Project Description: >")

        return project_name, project_version, project_description
    
    except Exception as e:

        return f"err: {e}", f"err: {e}", f"err: {e}"
        

def environment_setup():
    try:
        master_password = input("Please set the master password for this project: >")

        variables_status = {
            "Database Encryption": False,
            "Response Encryption": False,
            "Mailgun Integration": False,
            "Fast2SMS Integration": False,
            "Database Setup": False,
        }


        print("\n\nPlease go over the following project settings before continuing. Choose a number to configure the feature status.\nPress 6 to Continue(Irreversible)\n__________________________________________________________________________________________________________________")
        while True:
            sys.stdout.write(f"1. Database Encryption: {variables_status['Database Encryption']}\n2. Response Encryption: {variables_status['Response Encryption']}\n3. Mailgun Integration: {variables_status['Mailgun Integration']}\n4. Fast2SMS Integration: {variables_status['Fast2SMS Integration']}\n5. Database Setup: {variables_status['Database Setup']}\n\n6. Continue(Irreversible)\n> ")
            try:
                choice = input()
                if int(choice) not in range(1,7):
                    sys.stdout.flush()
                    sys.stdout.write("Choose an option between 1 and 6.\n")
                    continue
                
                choice = int(choice)
            
            except Exception as e:
                print("\nInput must be a number! Try again.\n")
                continue
            
            if choice == 1:
                sys.stdout.flush()
                sys.stdout.write("This option controls whether the data stored in the database is encrypted using public and private key pairs. (T/F)?")
                
                while True:
                    control = input()
                    if control == 'T':
                        variables_status['Database Encryption'] = True
                        break
                    elif control == 'F':
                        variables_status['Database Encryption'] = False
                        break
                    else:
                        sys.stdout.write("\nPlease Choose a value between T and F")
                        continue

            elif choice == 2:
                sys.stdout.flush()
                sys.stdout.write("This option controls whether the data sent to the client is encrypted using public and private key pairs. (T/F)?")
                
                while True:
                    control = input()
                    if control == 'T':
                        variables_status['Response Encryption'] = True
                        break
                    elif control == 'F':
                        variables_status['Response Encryption'] = False
                        break
                    else:
                        sys.stdout.write("\nPlease Choose a value between T and F")
                        continue

            elif choice == 3:
                sys.stdout.flush()
                sys.stdout.write("This option controls whether the setup will ask for Mailgun Credentials during Install. (T/F)?")
                
                while True:
                    control = input()
                    if control == 'T':
                        variables_status['Mailgun Integration'] = True
                        break
                    elif control == 'F':
                        variables_status['Mailgun Integration'] = False
                        break
                    else:
                        sys.stdout.write("\nPlease Choose a value between T and F")
                        continue

            elif choice == 4:
                sys.stdout.flush()
                sys.stdout.write("This option controls whether the setup will ask for Fast2SMS Credentials during Install. (T/F)?")
                
                while True:
                    control = input()
                    if control == 'T':
                        variables_status['Fast2SMS Integration'] = True
                        break
                    elif control == 'F':
                        variables_status['Fast2SMS Integration'] = False
                        break
                    else:
                        sys.stdout.write("\nPlease Choose a value between T and F")
                        continue

            elif choice == 5:
                sys.stdout.flush()
                sys.stdout.write("This option controls whether the setup will ask for Database Credentials during Install. (T/F)?")
                
                while True:
                    control = input()
                    if control == 'T':
                        variables_status['Database Setup'] = True
                        break
                    elif control == 'F':
                        variables_status['Database Setup'] = False
                        break
                    else:
                        sys.stdout.write("\nPlease Choose a value between T and F")
                        continue
            
            confirm = 'N'
            if choice == 6:

                sys.stdout.write("\n\nPlease confirm the above changes and proceed with Installation: (Y/N)?")
                
                while True:
                    control = input()

                    if control == 'Y':
                        confirm = control
                        break
                    elif control == 'N':
                        confirm = control
                        break
                    else:
                        sys.stdout.write("\nPlease Choose a value between Y and N")
                        continue

            if confirm == 'Y':
                break
            else:
                sys.stdout.flush()
                continue

        

        example_env = os.path.dirname(os.path.abspath('setup.py')) + f"/.env.example"
        project_env = os.path.dirname(os.path.abspath('setup.py')) + f"/.env"
        shutil.copy2(example_env, project_env)

        
        

        

    except Exception as e:
        pass



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
                                                   | $$
                                                   |__/                                                                                     
    \n\n\n''')
    print("Welcome to Flask-RestX-Boilerplate Setup:")
    
    project_name, project_version, project_description  = project_identity()
    # environment_setup()

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
        
        src =  os.path.dirname(os.path.abspath('setup.py')) + "/.gitignore"
        dest =  os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/.gitignore" 
        shutil.copy2(src, dest)
        print("Copying WSGI Application")
        
        src =  os.path.dirname(os.path.abspath('setup.py')) + "/manage.py"
        dest =  os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/wsgi.py" 

        print("Copying Requirements")
        
        shutil.copy2(src, dest)
        src = os.path.dirname(os.path.abspath('setup.py')) + "/requirements.txt"
        dest = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/requirements.txt"
        shutil.copy2(src, dest)



        print("Copying Environment Files")
        
        src = os.path.dirname(os.path.abspath('setup.py')) + "/.env.example"
        dest = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/.env"
        shutil.copy2(src, dest)


        # print("Setup Install Script. Please run install.ps1 post setup if it doesn't automatically run.")
        # 
        # src = src = os.path.dirname(os.path.abspath('setup.py')) + "/install.ps1"
        # dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/install.ps1" 
        # shutil.copy2(src, dest)

        fp = open('temp_file', 'w')
        fp.write(f"..\{project_name}")
        fp.close()

        print("Temporarily copying Project Name")
        
        src = os.path.dirname(os.path.abspath('setup.py')) + "/temp_file"
        dest = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/temp_file"
        shutil.copy2(src, dest) 

        print("Copying startup script (run.ps1). Please run post install.ps1 if it doesn't automatically run.")
        

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

        process_result = subprocess.Popen(commandline_options, stdout = subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        process_result.communicate()
        print("Script Execution Status: \n")
        print(process_result.returncode)
        print(process_result.stdout)
        print(process_result.stderr)

        if process_result.returncode == 0:
            Message = "Success"
        else:
            Message = "Fail"

        return Message, ""
    except Exception as e:
        return "Fail", e
    



done = False
def animate():
    for c in itertools.cycle(["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]):
        global done
        if done:
            break
        sys.stdout.write('\rInstalling ... ' + c+ "  ")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rInstallation Done!     ')


def main():
    try:
        project_name, setup_status = setup_project()

        if setup_status == False:

            print("Running Install Script... Please Wait!")
            time.sleep(2)
            install_loc = os.path.dirname(os.path.abspath('setup.py'))
            

            install_loc+="\\install.ps1"
            t = threading.Thread(target=animate)
            t.start()

            install_status, install_error = run_ps_script(install_loc)

            

            if install_status == "Success":
                print("\n__________________________________________________________\nInstall Script Successfully Completed!\n__________________________________________________________\n")
                global done
                done = True
                t.join()
                print("Running Post-Install Test Script.... Please Wait!")
                os.remove("temp_file")
                run_loc = os.path.dirname(os.path.dirname(os.path.abspath('setup.py')))
                

                run_loc+=f"\\{project_name}\\run.ps1"

                done =  False
                run_status, run_error = run_ps_script(run_loc)

                if run_status == "Success":
                    
                    print("\n__________________________________________________________\nPost Install has been successfully completed! You can run your project now!\n__________________________________________________________\n")
                    # os.remove(run_loc)
                    
                    
                else:
                    print(f"\n__________________________________________________________\nPost Install has failed! You can't run your project! Please troubleshoot!\n{run_error}\n\n__________________________________________________________\n")

            else:
                print("\n__________________________________________________________\nInstall Script Failed! Aborting! \n Error: "+ install_error +"\n__________________________________________________________\n")   

        else:
            print("\n__________________________________________________________\nProject Setup Failed!\n__________________________________________________________\n")

        

    except Exception as e:
        print(f"\n__________________________________________________________\nSystem Error: \n{e}\n__________________________________________________________\n")



if __name__ == "__main__":
    main()





