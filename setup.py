import os, shutil, errno
from time import sleep



print("Welcome to Boilerplate Setup:")
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
    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/.gitignore"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/.gitignore" 
    shutil.copy2(src, dest)
    print("Copying WSGI Application")
    sleep(2)
    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/manage.py"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/wsgi.py" 

    print("Copying Requirements")
    sleep(2)
    shutil.copy2(src, dest)
    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/requirements.txt"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/requirements.txt"
    shutil.copy2(src, dest)

    print("Copying Environment Files")
    sleep(2)
    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/.env.example"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/.env"
    shutil.copy2(src, dest)


    print("Setup Install Script. Please run install.ps1 post setup")
    sleep(3)
    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/install.ps1"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/install.ps1" 
    shutil.copy2(src, dest)

    fp = open('filename', 'w')
    fp.write(f'{project_name}')
    fp.close()

    print("Temporarily copying Project Name")
    sleep(2)
    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/filename"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/filename"
    shutil.copy2(src, dest) 

    print("Copying startup script (run.ps1)")
    sleep(2)

    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/run.ps1"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/run.ps1"
    shutil.copy2(src, dest)
except OSError as err:
    print("Error: % s" % err)
    error_oc = True


if error_oc:
    print("Some error occured! Project might be broken!")
else:
    print(f"All good! Project created in: ../{project_name}/")








