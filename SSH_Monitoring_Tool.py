import paramiko
import os, time, sys
from contextlib import closing
from zipfile import ZipFile, ZIP_DEFLATED
import shutil
import datetime

import csv,codecs,cStringIO,os,psycopg2,urllib2,os,sys,shutil,xlsxwriter,time,ConfigParser,string
from collections import Counter
from string import Template
import re
from fuzzywuzzy import fuzz


import thread, threading
from time import strftime

from functools import wraps




class MyOutput():
    def __init__(self, logfile):
        self.stdout = sys.stdout
        self.log = open(logfile, 'w')
  
    def write(self, text):
        self.stdout.write(text)
        self.log.write(text)
        self.log.flush()
  
    def close(self):
        self.stdout.close()
        self.log.close()


class SSH():
    def __init__(self, host, s_u, s_k):
        self.host=host
        self.s_u=s_u
        self.s_k=s_k

    def CONNECT(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if self.s_k.endswith('.pem'):
                self.client.connect(self.host, username=self.s_u, password='', key_filename=self.s_k)
            else:
                print 'here'
                print self.host
                print self.s_u
                print self.s_k.split('\\')[-1].strip()
                self.client.connect(self.host, username=self.s_u, password=self.s_k.split('\\')[-1].strip())
            return [True,'Connected to the host']
        except Exception, e:
            return [False,str(e)]


    def SSH_COMMAND(self, command):
        print 'SSH --> '+command
        stdin,stdout,stderr=self.client.exec_command(command)
        stdin.close()
        self.output=''
        for line in stdout.read().splitlines():
            self.output+=line+'\n'
        for line in stderr.read().splitlines():
            self.output+='ERROR: '+line+'\n'
        return self.output

    def SSH_COMMAND_ONLY(self, command):
        #print 'SSH --> '+command
        stdin,stdout,stderr=self.client.exec_command(command)
        stdin.close()
        for line in stdout.read().splitlines():
            pass
        for line in stderr.read().splitlines():
            pass


    def UPLOAD_FILE(self, local_abs_path, server_dst_path):
        try:
            file_name=os.path.basename(local_abs_path)
            ftp = self.client.open_sftp()
            if server_dst_path[-1]=='/':
                server_dst_path=server_dst_path+file_name
            else:
                server_dst_path=server_dst_path+'/'+file_name
            #print 'Source: '+local_abs_path+' Destination: '+server_dst_path
            ftp.put(local_abs_path,server_dst_path)
            return [True, file_name+" was sucsesfully uploaded --> PASS"]
        except  Exception, e:
            return [False,str(e)]

    def DOWNLOAD_FILE(self,path,local_dir_path):
        try:
            ftp=self.client.open_sftp()
            local_path=os.path.join(local_dir_path, os.path.basename(path))
            print 'Source: '+path+' Destination: '+local_path
            ftp.get(path, local_path)
            return [True, os.path.basename(path)+" was sucsesfully downloaded --> PASS"]
        except  Exception, e:
            return[False, str(e)]

    def CLOSE(self):
        self.client.close()


def DELETE_LOG_CONTENT(log_file_name):
    f = open(log_file_name, 'w')
    f.write('')

def EXIT(string):
    stam=raw_input(string)
    sys.exit(1)

def CONTINUE (message=''):
    print message
    cont=raw_input('Continue? y/n  ')
    if (cont=='y'):
        print "Your choose is: '"+cont+"' continue execution!"
        print ''
    elif (cont=='n'):
        print "Your choose is: '"+cont+"' execution will be stopped!"
        sys.exit(1)
    else:
        print "No such option: '"+cont+"'"
        CONTINUE ()

def CHOOSE_OPTION_FROM_LIST(list_object, msg):
    print ''
    try:
        if (len(list_object)==0):
            print "Nothing to choose :( "
            print "Execution will stop!"
            time.sleep(5)
            EXIT("**************** FATAL ERROR, CANNOT CONTINUE EXECUTION !!!   ******************")
            sys.exit(1)
        print msg
        counter=1
        for item in list_object:
            print str(counter)+') - '+item
            counter=counter+1
        choosed_option=raw_input("Choose option by entering the suitable number! ")
        while (int(choosed_option)<0 or int(choosed_option)> len(list_object)):
            print "No such option - ", choosed_option
            choosed_option=raw_input("Choose option by entering the suitable number! ")

        print "Chosen option is : '"+list_object[int(choosed_option)-1]+"'"
        return [True,list_object[int(choosed_option)-1]]
    except Exception, e:
        print '*** No such option!!!***', e
        return[False, str(e)]

def GET_OBJECT_ABS_PATH(root_dir_path, object_name):
    for (path, dirs, files) in os.walk(root_dir_path):
        for item in dirs:
            if item==object_name:
                return ['dir',os.path.join(os.path.abspath(path),object_name)]
        for item in files:
            if item==object_name:
                return ['fil',os.path.join(os.path.abspath(path),object_name)]


def ZIPDIR(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)+len(os.sep):] #XXX: relative path
                z.write(absfn, zfn)



def CREATE_EXCEL_SHEETS(file_name,sheet_dict):
    #Create an new Excel file and add a worksheet.
    try:
        workbook = xlsxwriter.Workbook(file_name)
        for d in sheet_dict.keys():
            worksheet = workbook.add_worksheet(d)
            bold = workbook.add_format({'bold': 1})
            nes_lis_data=sheet_dict[d]
            row=0
            for lis in nes_lis_data:
                col=0
                for item in lis:
                    #item=item.decode("utf8")
                    #print item
                    worksheet.write(row, col, str(item).decode('utf8', 'ignore'))
                    col+=1
                row+=1
        workbook.close()
        return True
    except Exception, e:
        print '*** CREATE_EXCEL_SHEETS!!! ***', e



def ADD_LIST_AS_LINE_TO_CSV_FILE(csv_file_name,lis):
    try:
        f = open(csv_file_name, 'ab')
        writer = csv.writer(f)
        writer.writerow(lis)
        f.close()
    except Exception, e:
        print '*** ADD_LIST_AS_LINE_TO_CSV_FILE!!! ***', e

def READ_CSV_AS_NESTED_LIST(file_name):
    try:
        nested=[]
        with open(file_name, 'rb') as f:
            reader = csv.reader(f)
            for row in reader:
                nested.append(row)
        return nested

    except Exception, e:
        print '*** READ_CSV_AS_NESTED_LIST!!! ***', e

def SPEC_PRINT(string_list):
    len_list=[]
    for item in string_list:
        len_list.append(len('### '+item.strip()+' ###'))
    max_len=max(len_list)
    print ''
    print"#"*max_len
    for item in string_list:
        print "### "+item.strip()+" "*(max_len-len("### "+item.strip())-4)+" ###"
    print"#"*max_len+'\n'




########################### MAIN ###################################
#DELETE_LOG_CONTENT('Runtime.log')
#DELETE_LOG_CONTENT('Error.log')
#sys.stdout=MyOutput('Runtime.log')
#sys.stderr=MyOutput('Error.log')


#for server in servers:
#	a=SSH(server[1],server[2],os.path.abspath(server[3]))
#	result=a.CONNECT()
#	if result[0]==False:
#		print result[1]
#		EXIT('Type ENTER to EXIT!!!')
#	else:
#		print a.SSH_COMMAND('hostname')
#		print a.SSH_COMMAND('date')
#		print a.SSH_COMMAND('whoami')
#	a.CLOSE()
#EXIT('Type ENTER to EXIT!!!')


#ps aux --sort rss | grep storm_initializer.py | grep -v grep | awk '{print $13 "," $2 "," $5}'
#ps aux --sort rss | grep storm.id | grep -v grep | awk '{print $20 "," $2 "," $5}'
#ps aux --sort rss | grep backtype.storm.daemon.supervisor | grep -v grep | awk '{print $NF "," $2 "," $5}'


def MONITOR_SERVER(server_name,ip,user,key,delay):
    sample_time=0

    # CPU and MEM
    res_file=server_name+'.csv'
    DELETE_LOG_CONTENT(res_file)
    monitor_data=['Sample_time','Date','CPU','Memory','Disk']
    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,monitor_data)
    #cpu="top -n 2 | grep -i 'cpu(s)' > stam.txt; tail -1 stam.txt | awk '{print $2}' | cut -d '%' -f1"
    cpu="mpstat | grep all | awk '{print 100-$12}'"
    mem="free | grep Mem | awk '{print $3/$2*100}'"
    disk="""df -h / | grep -v system | awk '{print $5}'"""

    # Processes
    res_file_proc=server_name+'_PROCESS.csv'
    DELETE_LOG_CONTENT(res_file_proc)
    proc_data=['Sample_time','Date','ProcessName','PID','MEM']
    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file_proc,proc_data)
    # Workers
    worker_proc_commands=['date',
                   """ps aux --sort rss | grep storm_initializer.py | grep -v grep | awk '{print $13 "," $2 "," $4}'""",
                  """ps aux --sort rss | grep storm.id | grep -v grep | awk '{print $20 "," $2 "," $4}'""",
                  """ps aux --sort rss | grep backtype.storm.daemon.supervisor | grep -v grep | awk '{print $NF "," $2 "," $4}'"""]
    worker_proc_command=''
    for item in worker_proc_commands:
        worker_proc_command+=item+';'
    worker_proc_command.strip(';')
    #Main
    main_proc_commands=['date',
                        """ps aux --sort rss | grep -i java | grep -i storm | grep -v grep | awk '{print $NF "," $2 "," $4}'""",
                        """ps aux --sort rss | grep -i python | grep -v grep | awk '{print $NF "," $2 "," $4}'""",
                        """ps aux --sort rss | grep -i redis | grep -v grep | awk '{print $1 "," $2 "," $4}'"""]
    main_proc_command=''
    for item in main_proc_commands:
        main_proc_command+=item+';'
    main_proc_command.strip(';')



    #SSH Connect
    a=SSH(ip,user,os.path.abspath(key))
    result=a.CONNECT()
    print result
    if result[0]==False:
        #print result[1]
        #EXIT("Couldn't connect to: "+server_name)
        SPEC_PRINT([server_name])
        sys.exit(1)
    else:
        while(1):

            # Monitoring
            time.sleep(delay)
            monitor_command='date'+';'+cpu+';'+mem+';'+disk
            monitor_data=a.SSH_COMMAND(monitor_command).strip().split('\n')
            monitor_data=[sample_time]+monitor_data
            print monitor_data
            ADD_LIST_AS_LINE_TO_CSV_FILE(res_file,monitor_data)

            if 'worker' in server_name.lower():
                # Proccess workers
                proc_data=a.SSH_COMMAND(worker_proc_command)
                proc_data=proc_data.replace('-Dstorm.id=','')
                proc_data=proc_data.strip().split('\n')
                proc_data=[item.split(',') for item in proc_data]
                date=proc_data[0]
                proc_data.remove(date)
                proc_data=[[sample_time]+date+item for item in proc_data]
                for p in proc_data:
                    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file_proc,p)
                print proc_data[0]

            if 'main' in server_name.lower():
                proc_data=a.SSH_COMMAND(main_proc_command)
                if 'error' in str(proc_data).lower():
                    print 'Warning!!!'
                    print str(proc_data)


                proc_data=proc_data.strip().split('\n')
                proc_data=[item.split(',') for item in proc_data]
                date=proc_data[0]
                proc_data.remove(date)
                proc_data=[[sample_time]+date+item for item in proc_data]
                for p in proc_data:
                    ADD_LIST_AS_LINE_TO_CSV_FILE(res_file_proc,p)
                print proc_data[0]
            sample_time+=delay
    a.CLOSE()

#MONITOR_SERVER('Worker_1','54.196.120.205','ubuntu','sockskp.pem',1)
#MONITOR_SERVER('Worker_2','54.204.181.147','ubuntu','sockskp.pem',1)
#MONITOR_SERVER('Main','54.237.139.64','ubuntu','sockskp.pem',1)


#servers=[['Worker_1','54.80.140.167','ubuntu','sockskp.pem',10],
#		 ['Worker_2','54.204.181.147','ubuntu','sockskp.pem',10],
#		 ['Main','54.237.139.64','ubuntu','sockskp.pem',10]]




###################################################### MAin ##########################################################



if __name__ == "__main__":

    for fil in os.listdir('.'):
        if fil.endswith('csv') or fil.endswith('.png'):
            os.remove(fil)


    class myThread(threading.Thread):
        def __init__(self,server_name,ip,user,key,delay):
            self.server_name=server_name
            self.ip=ip
            self.user=user
            self.key=key
            self.delay=delay
            threading.Thread.__init__(self)
        def run(self):
            #try:
            MONITOR_SERVER(self.server_name,self.ip,self.user,self.key,self.delay)
            #except (KeyboardInterrupt, SystemExit):
            #	print '\n! Received keyboard interrupt, quitting threads.\n'



    #servers=[['Worker_1','54.87.217.176','ubuntu','sockskp.pem',10],
    #         ['Worker_2','54.211.128.218','ubuntu','sockskp.pem',10],
    #         ['Worker_3','54.89.117.147','ubuntu','sockskp.pem',10],
    #         ['Worker_4','54.196.174.27','ubuntu','sockskp.pem',10],
    #		 ['Main','174.129.176.42','ubuntu','sockskp.pem',10],
    #		 ]

    #### Start threads ###
    threads=[]
    for server in servers:
        server_name=server[0]
        ip=server[1]
        user=server[2]
        key=server[3]
        delay=server[4]
        threads.append(myThread(server_name,ip,user,key,delay))
    for t in threads:
        print t
        time.sleep(1)
        t.start()


    ### While threads are alive ###
    while 1:
        try:
            time.sleep(3)
            now = datetime.datetime.now()
            now=now.strftime("%Y-%m-%d_%H_%M_%S")
            print "            ***"+now+" Active threads:"+str(len(threads))+" ***"
            thread_len=len(threads)
            for t in threads:
                if not t.isAlive():
                    threads.remove(t)
                    if len(threads)==0:
                        print 'Kirdik, no thread is alive, going to die...'
                        sys.exit(1)
        except KeyboardInterrupt:
            print "Ctrl-c received! Sending kill to threads..."
            for t in threads:
                t.kill_received = True

  





