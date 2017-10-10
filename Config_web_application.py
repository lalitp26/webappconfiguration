
import os
import subprocess, shutil
# from github import Github

status_flag = False
folder_name = None
folder_path = None

confi_file = '''
            server {0}
                listen 80;
                server_name {1};
                sendfile on;
                root {2};
                location img/ {0}
                    try_files /app/img/$uri =404;
                {3}
                location / {0}
                    add_header 'Access-Control-Allow-Origin' '*';
                {3}
            {3}'''

print("Plase wait Checking prerequisite...")
current_working_dir = os.getcwd()

try:
    print("Checking for NGINX server")
    subprocess.call(['nginx','-V'])
    status_flag = True
except expression as identifier:
    print("NGINX not install")
    choice = input("Do you want to install [y/n]: ")
    if choice.lower() is 'y':
        print("Please wait...Installing NGINX server...")
        try:
            subprocess.call(['sudo', 'pip', 'install', 'nginx'])    
        except expression as identifier:
            print("Faild to install...")
            status_flag= False
        
    else:
        print("Please wait.... Aborting setup...")
        status_flag = False



while status_flag:
    folder_name = input("Enter Folder Name To Create:- ")

    if not folder_name:
        folder_name ="frappe-web-apps"

    folder_path = os.path.join(os.sep,current_working_dir,folder_name)

    if os.path.exists(folder_path):
        print("Folder already exists would you like to override y/n")
        user_choice = input()

        if user_choice is 'y':
            shutil.rmtree(folder_path)
            os.mkdir(folder_path)
            status_flag = True
            break
        else:
            continue
    else:
        os.mkdir(folder_path)
        break

# print(os.path.join(os.sep,current_working_dir,folder_name))
os.chdir(folder_name)
while status_flag:
    try:
        print("Please wait... Initializing git...")
        subprocess.call(['git','init'])
        print("Done")
        remote_url = input("Enter remote url to add Upstream:- ")
        print("Please wailt.... adding updtream url")
        subprocess.call(['git','remote','add','upstream','https://github.com/medipta/webcode'])
        print("Done")
        print("Please wait.... Pulling master repo...")
        subprocess.call(['git','pull','upstream','master'])
        print("Project created successfully......")
        break
    except expression as identifier:
        print("Somethig went wrong..")
        choice = input("Do you want to initialize again [y/n]: ")
        if choice.lower() is 'y':
            print("Please wait Continuing......")
            continue
        else:
            status_flag = False
            print("For fresh installation run programe again. Thanks...")
            break


print("Creating server configuration file......")
print("Enter server name Ex. lab.medipta.org or lab.medipta.com etc...")
server_name = input()
server_path = "/etc/nginx/conf.d"
config_file_name = folder_name + ".conf"
config_file_path = os.join(folder_path, config_file_name)
destination_config_file_path = os.join(server_path, config_file_name)

from shutil import copyfile
if os.path.exists(server_path):
    file = open(config_file_name,'w')
    file.write(confi_file.format('{', server_name, folder_path, '}'))
    file.close()
    try:
        subprocess.call(['sudo','ln', '-s', config_file_path, destination_config_file_path])
        # copyfile(os.path.join(folder_path,config_file_name), os.path.join(server_path,config_file_name))
        print("########### Done ###########")
        print(" *** Please open file [hosts] present in [/etc/] durectory\nand add 127.0.0.1    server name and save***")

    except expression as identifier:
        print("Unknown error occured.... Aborting setup...")
    
else:
    print("[/etc/nginx/sites-available/] folder is not available")
    print("Please check NGINX install properly..")
    print("Aborting setup...Thanks")

print("Please wait.... Restarting and Reloading nginx server...")
subprocess.call(['sudo','service','nginx','restart'])
subprocess.call(['sudo','service','nginx','reload'])
print("Your web application is ready to use")
print("Open browser and enter in addressbar ",server_name)

# sudo vim /etc/hosts
# sudo service nginx reload
# sudo service nginx restart
