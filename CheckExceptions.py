#!/usr/bin/python
import SSH_Monitoring_Tool
import os,time,shutil,ConfigParser,sys
import zipfile
from functools import wraps
def CONVERT_INI_TO_VARIABLES(ini_file_name):
    try:
        config = ConfigParser.ConfigParser()
        config.read(ini_file_name)

        dictionary = {}
        for section in config.sections():
            dictionary[section] = {}
            for option in config.options(section):
                dictionary[section][option] = config.get(section, option)

        sections=config.sections()
        for section in sections:
            data=dictionary[section]
            globals().update(data)
    except Exception, e:
        print '*** CONVERT_INI_TO_VARIABLES!!! ***', e
        SSH_Monitoring_Tool.EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
        sys.exit(1)

        ############################## Main #################################################################
### Get User parameters and convert types where needed ###
CONVERT_INI_TO_VARIABLES('conf.ini')
if upload_script.lower()=='true':
    upload_script=True
ssh_retry=int(ssh_retry)
servers=eval(servers)
modes=['Get ERRORs in NV logs using GREP',
       'Get latest timestamp of vcat.log and Catalina.out logs',
       'Get Catalina ERRORs/WARNINGs using grep']
       #'Get All Errors or Warnings (including rotated logs)','Get last tasks',
       #'Get JAVA exceptions','Get Task Details']
mode=SSH_Monitoring_Tool.CHOOSE_OPTION_FROM_LIST(modes,'Please choose operation mode: ')


# if mode[1]=='Get ERRORs in NV logs':
#     for s in servers:
#         print '-'*90
#         print s
#         #SSH_Monitoring_Tool.SPEC_PRINT([s[0]])
#         ## SSH with retry
#         exit_flag=False
#         while exit_flag!=True:
#             ssh_retry-=1
#             a=SSH_Monitoring_Tool.SSH(s[1],s[2],os.path.abspath(s[3]))
#             is_connected=a.CONNECT()
#             print is_connected
#             if is_connected[0]==True:
#                 exit_flag=True
#             if ssh_retry==0:
#                 exit_flag=True
#         if is_connected[0]:
#             if upload_script==True:
#                 result_dir='Errors_And_Warnings_'+s[0]+'_'+nv_time.replace(' ','_').replace(':','_')
#                 try:
#                     shutil.rmtree(result_dir)
#                 except:
#                     pass
#                 try:
#                     os.mkdir(result_dir)
#                 except Exception, e:
#                     print e
#                     SSH_Monitoring_Tool.EXIT('Type Enter to Exit!')
#
#
#                 #print a.UPLOAD_FILE('Get_Errors_And_Warnings.py',log_path)
#                 print a.UPLOAD_FILE('Get_Errors_And_Warnings.py','/home/'+s[2])
#                 a.SSH_COMMAND('sudo cp Get_Errors_And_Warnings.py '+nv_log_path)
#                 a.SSH_COMMAND('sudo chmod 777 '+nv_log_path+'Get_Errors_And_Warnings.py')
#                 a.SSH_COMMAND('sudo chown root:root '+nv_log_path+'Get_Errors_And_Warnings.py')
#                 com='sudo '+nv_log_path+'Get_Errors_And_Warnings.py '+"'"+nv_time+"'"+' '+env_name+' Exceptions.log '+nv_log_path
#                 print com
#                 out=a.SSH_COMMAND_ONLY(com)
#                 a.SSH_COMMAND('sudo rm '+nv_log_path+'Get_Errors_And_Warnings.py')
#                 print a.SSH_COMMAND('zip Exceptions.log.zip Exceptions.log')
#                 print a.DOWNLOAD_FILE('/home/ubuntu/Exceptions.log.zip',os.path.abspath(result_dir))
#                 a.SSH_COMMAND('sudo rm /home/ubuntu/Exceptions.log')
#                 a.SSH_COMMAND('sudo rm /home/ubuntu/Exceptions.log.zip')
#                 a.CLOSE()
#         else:
#             print SSH_Monitoring_Tool.SPEC_PRINT(["Achtung Achtung !!!","SSH to: "+s[0].lower()+" failed!!!"])
#             SSH_Monitoring_Tool.EXIT('Press Enter to exit!')

if mode[1]=='Get ERRORs in NV logs using GREP':
    result_dirs=[]
    options=['ERROR','WARN']
    option=SSH_Monitoring_Tool.CHOOSE_OPTION_FROM_LIST(options,'Please choose debug level: ')
    if option[1]=='ERROR':
        grep_string=" ERROR "
        result_file='All_Errors.log'
    if option[1]=='WARN':
        grep_string=" WARNING "
        result_file='All_Warnings.log'
 
    timestamp_result_dir='NV_Logs_'+nv_time.replace(' ','_').replace(':','_')+'_'+option[1]
    try:
        shutil.rmtree(timestamp_result_dir)
    except:
        pass
    try:
        os.mkdir(timestamp_result_dir)
    except Exception, e:
        print e
        SSH_Monitoring_Tool.EXIT('Type Enter to Exit!')

 
    for s in servers:
        print '-'*90
        print s
        #SSH_Monitoring_Tool.SPEC_PRINT([s[0]])
        ## SSH with retry
        exit_flag=False
        while exit_flag!=True:
            ssh_retry-=1
            a=SSH_Monitoring_Tool.SSH(s[1],s[2],os.path.abspath(s[3]))
            is_connected=a.CONNECT()
            print is_connected
            if is_connected[0]==True:
                exit_flag=True
            if ssh_retry==0:
                exit_flag=True

        if is_connected[0]:
            if upload_script==True:
                result_dir=option[1]+'_'+s[0]+'_'+nv_time.replace(' ','_').replace(':','_')
                try:
                    shutil.rmtree(result_dir)
                except:
                    pass
                try:
                    os.mkdir(result_dir)
                    result_dirs.append(result_dir)
                except Exception, e:
                    print e
                    SSH_Monitoring_Tool.EXIT('Type Enter to Exit!')
                print a.UPLOAD_FILE('Get_All_Errors_Or_Warnings.py','.')

                print a.SSH_COMMAND('chmod 777 Get_All_Errors_Or_Warnings.py')

                com="sudo python Get_All_Errors_Or_Warnings.py "+"'"+nv_time+"'"+' '+nv_log_path+' '+result_file+' '+grep_string
                print '--> '+com
                print a.SSH_COMMAND(com)
                print a.SSH_COMMAND('zip '+result_file+'.zip'+' '+result_file)
                print a.DOWNLOAD_FILE(result_file+'.zip',os.path.abspath(result_dir))
                with zipfile.ZipFile(os.path.join(os.path.abspath(result_dir),result_file+'.zip'), "r") as z:
                    z.extractall(os.path.abspath(result_dir))
                os.remove(os.path.join(os.path.abspath(result_dir),result_file+'.zip'))
                a.SSH_COMMAND('rm -rf '+result_file+'*')
                a.SSH_COMMAND('rm -rf Get_All_Errors_Or_Warnings.py')
                a.SSH_COMMAND('rm -rf errors.txt')
                a.CLOSE()
        else:
            print SSH_Monitoring_Tool.SPEC_PRINT(["Achtung Achtung !!!","SSH to: "+s[0].lower()+" failed!!!"])
            SSH_Monitoring_Tool.EXIT('Press Enter to exit!')

    for dir in result_dirs:
        shutil.move(dir,timestamp_result_dir)
 

if mode[1]=='Get Catalina ERRORs/WARNINGs using grep':
    result_dirs=[]
    options=['ERROR','WARN']
    option=SSH_Monitoring_Tool.CHOOSE_OPTION_FROM_LIST(options,'Please choose debug level: ')
    if option[1]=='ERROR':
        grep_string=" ERROR "
        result_file='All_Errors.log'
    if option[1]=='WARN':
        grep_string=" WARN "
        result_file='All_Warnings.log'

    timestamp_result_dir='Catalina_'+catalina_time.replace(' ','_').replace(':','_')+'_'+option[1]
    try:
        shutil.rmtree(timestamp_result_dir)
    except:
        pass
    try:
        os.mkdir(timestamp_result_dir)
    except Exception, e:
        print e
        SSH_Monitoring_Tool.EXIT('Type Enter to Exit!')


    for s in servers:
        print '-'*90
        print s
        #SSH_Monitoring_Tool.SPEC_PRINT([s[0]])
        ## SSH with retry
        exit_flag=False
        while exit_flag!=True:
            ssh_retry-=1
            a=SSH_Monitoring_Tool.SSH(s[1],s[2],os.path.abspath(s[3]))
            is_connected=a.CONNECT()
            print is_connected
            if is_connected[0]==True:
                exit_flag=True
            if ssh_retry==0:
                exit_flag=True

        if is_connected[0]:
            if upload_script==True:
                result_dir=option[1]+'_'+s[0]+'_'+catalina_time.replace(' ','_').replace(':','_')
                try:
                    shutil.rmtree(result_dir)
                except:
                    pass
                try:
                    os.mkdir(result_dir)
                    result_dirs.append(result_dir)
                except Exception, e:
                    print e
                    SSH_Monitoring_Tool.EXIT('Type Enter to Exit!')
                print a.UPLOAD_FILE('Get_All_Errors_Or_Warnings_Catalina.py','.')

                print a.SSH_COMMAND('chmod 777 Get_All_Errors_Or_Warnings_Catalina.py')

                com="sudo python Get_All_Errors_Or_Warnings_Catalina.py "+"'"+catalina_time+"'"+' '+catalina_log_path+' '+result_file+' '+grep_string
                print '--> '+com
                print a.SSH_COMMAND(com)
                print a.SSH_COMMAND('zip '+result_file+'.zip'+' '+result_file)
                print a.DOWNLOAD_FILE(result_file+'.zip',os.path.abspath(result_dir))
                with zipfile.ZipFile(os.path.join(os.path.abspath(result_dir),result_file+'.zip'), "r") as z:
                    z.extractall(os.path.abspath(result_dir))
                os.remove(os.path.join(os.path.abspath(result_dir),result_file+'.zip'))
                a.SSH_COMMAND('rm -rf '+result_file+'*')
                a.SSH_COMMAND('rm -rf Get_All_Errors_Or_Warnings_Catalina.py')
                a.SSH_COMMAND('rm -rf errors.txt')
                a.CLOSE()
        else:
            print SSH_Monitoring_Tool.SPEC_PRINT(["Achtung Achtung !!!","SSH to: "+s[0].lower()+" failed!!!"])
            SSH_Monitoring_Tool.EXIT('Press Enter to exit!')

    for dir in result_dirs:
        shutil.move(dir,timestamp_result_dir)






if mode[1]=='Get latest timestamp of vcat.log and Catalina.out logs':
    for s in servers:
        print '-'*90
        print s
        #SSH_Monitoring_Tool.SPEC_PRINT([s[0]])
        ## SSH with retry
        exit_flag=False
        while exit_flag!=True:
            ssh_retry-=1
            a=SSH_Monitoring_Tool.SSH(s[1],s[2],os.path.abspath(s[3]))
            is_connected=a.CONNECT()
            print is_connected
            if is_connected[0]==True:
                exit_flag=True
            if ssh_retry==0:
                exit_flag=True

        if is_connected[0]:
            print 'vcat.log --> '+a.SSH_COMMAND('''tail -1 '''+nv_log_path+'''vcat.log | cut -d ',' -f1''').strip()
            print 'catalina.out --> '+a.SSH_COMMAND('''tail -1 '''+catalina_log_path+'''catalina.out | cut -d '.' -f1''').strip()
            a.CLOSE()
        else:
            print SSH_Monitoring_Tool.SPEC_PRINT(["Achtung Achtung !!!","SSH to: "+s[0].lower()+" failed!!!"])
            SSH_Monitoring_Tool.EXIT('Press Enter to exit!')







