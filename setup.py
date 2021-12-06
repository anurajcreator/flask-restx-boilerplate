import os, shutil, errno

project_name  = input("Welcome to Boilerplate Setup:\nPlease name your project: >")

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
    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/.gitignore"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/.gitignore" 
    shutil.copy2(src, dest)
    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/manage.py"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/manage.py" 
    shutil.copy2(src, dest)
    src = src = os.path.dirname(os.path.abspath('setup.py')) + "/requirements.txt"
    dest = path = os.path.dirname(os.path.dirname(os.path.abspath('setup.py'))) + f"/{project_name}" + "/requirements.txt"
    shutil.copy2(src, dest)
except OSError as err:
    print("Error: % s" % err)
    error_oc = True

if error_oc:
    print("Some error occured! Project might be broken!")
else:
    print(f"All good! Project created in: ../{project_name}/")








