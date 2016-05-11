#!/usr/bin/python
import subprocess,time,os,sys
from datetime import datetime
import gzip
from collections import Counter
from string import digits




########################## Parameters #############################
## Grep by time ###
try:
    grep=sys.argv[1]
except:
    grep='2016-04-01 00:42:00'

## Log path ##
try:
    log_path=sys.argv[2]
except:
    log_path='./'
## Result fileh ##
try:
    result_file=sys.argv[3]
except:
    result_file='All_Exceptions.log'
## String for Grep##
try:
    string_for_grep=sys.argv[4]
except:
    string_for_grep=' ERROR '



def DELETE_LOG_CONTENT(log_file_name):
    f = open(log_file_name, 'w')
    f.write('')

def INSERT_TO_LOG(log_file, msg):
    log_file = open(log_file, 'a')
    log_file.write(msg+'\n')
    log_file.close()

def READ_GZ_DATA_LIST(file_path):
    fil=gzip.open(log, 'rb')
    fil_data=fil.readlines()
    fil.close()
    return fil_data

def GET_LOG_END_TIME(log):
    if log.endswith('.gz'):
        log_data=READ_GZ_DATA_LIST(log)
        stop_time=None
        while stop_time==None:
            for line in reversed(log_data):
                if ' 2015-' in line:
                    split_line=line.split(',')
                else :
                    continue
            stop_time=split_line[3][split_line[3].find('2015'):]
    else:
        log_data=READ_FILE_DATA_LIST(log)
        stop_time=None
        while stop_time==None:
            for line in reversed(log_data):
                if ' 2015-' in line:
                    split_line=line.split(',')
                else :
                    continue
            stop_time=split_line[3][split_line[3].find('2015'):]
    return stop_time.strip()

def GET_LOG_END_TIME_FROM_CACHE_FILE(cache_file,log):
    if cache_file not in os.listdir('.') or len(open(cache_file,'r').readlines())==0 or log not in open(cache_file,'r').read():
        stop_time=GET_LOG_END_TIME(log)
        INSERT_TO_LOG(cache_file,log+','+stop_time)
    else:
        cached_data=open(cache_file).readlines()
        for l in cached_data:
            split_line=l.split(',')
            if log==split_line[0].strip():
                stop_time=split_line[1].strip()
                break
    return stop_time

def PRINT_ON_SAME_PLACE(string):
    string=str(string)
    sys.stdout.flush()
    sys.stdout.write(string+'\r')
    sys.stdout.write("\b")

def GET_LINES_INDEXES_GREP(log, string, time_grep):
    time_grep=datetime.strptime(time_grep,"%Y-%m-%d %H:%M:%S")
    indexes=[]
    save_to_file='errors.txt'
    if log.endswith('.gz'):
        os.system("zgrep -n '"+string+"' "+log+" > "+save_to_file)
    else:
        os.system("grep -n '"+string+"' "+log+" > "+save_to_file)
    lines=open(save_to_file,'r').readlines()
    try:
        for line in lines:
            line_index=line.split(':')[0]
            line=line.replace(line_index+':','')
            date=line.split(',')[0]
            date=datetime.strptime(date,"%Y-%m-%d %H:%M:%S")
            if date>time_grep:
                indexes.append(line_index)
    except Exception, e:
        print str(e)
    indexes=[int(i)-1 for i in indexes]
    return indexes

def READ_FILE_DATA_LIST(file_path):
    fil=open(log, 'r')
    fil_data=fil.readlines()
    fil.close()
    return fil_data        

################################### Main ########################################################
start_execution_time=time.time()
DELETE_LOG_CONTENT(result_file)
f=open(result_file,'a')
logs=os.listdir(log_path)
logs=[os.path.join(log_path,fil) for fil in logs if '.log' in fil]
#logs=[os.path.join(log_path,fil) for fil in logs if 'duplicatecontactdatabase' in fil]

all_exceptions_list=[]
printed_indexes=[]
traceback_list=[]

for log in logs:
    exceptions_number=0
    print '-'*100
    print '--> '+log

    log_data=READ_FILE_DATA_LIST(log)
    len_log_data=len(log_data)
    exception_indexes=GET_LINES_INDEXES_GREP(log,string_for_grep,grep)
    for index in exception_indexes:
        try:
            key=log_data[index].split(' ')[4].split(':')[0]
            value=log_data[index][log_data[index].find(' - '):].strip()
            all_exceptions_list.append([key,value,log,index+1])
            exceptions_number+=1
        except:
            continue
        #PRINT_ON_SAME_PLACE(str(index))
        data_to_print=''
        if index not in printed_indexes:
            f.write('\n'+'#'*50+' '+log+' Line number: '+str(index+1)+'#'*50+'\n')
            stop_ind=index+10
            start_ind=index-5
            x=start_ind
            while x<=stop_ind:
                if 0<=x<len_log_data:
                    f.write(str(x+1)+':'+log_data[x])
                    data_to_print+=log_data[x]
                    printed_indexes.append(x)
                    if log_data[x].startswith(' '):
                        stop_ind+=1
                else:
                    f.write('\n')
                x+=1
        if data_to_print.find('Traceback')>0:
            traceback_list.append([key,value,log,index+1])

### Add statistics to the end of result file ###
if len(all_exceptions_list)>0:
    stop_execution_time=time.time()
    print '*'*50+' Statistics '+'*'*50
    f.write('\n'*50)
    f.write('\n'+'*'*122+' Statistics '+'*'*122+'\n')
    #all_exceptions_list_keys=[item[0][0:120] if len(item[0])>120 else item[0][0:-1] for item in all_exceptions_list]
    all_exceptions_list_keys=[item[0] for item in all_exceptions_list]
    all_exceptions_list_set=set(all_exceptions_list_keys)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            	
    for k in all_exceptions_list_set:
        print '-'*400
        f.write('-'*400+'\n')
        counter=all_exceptions_list_keys.count(k)
        print 'Key: "'+k+'" Counter: '+str(counter)
        f.write('Key: "'+k+'" Counter: '+str(counter)+'\n')    
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            	
        len_to_print=30
        printed_values=0
        if all_exceptions_list_keys.count(k)>len_to_print:
            print_data=[]
            for kv in all_exceptions_list:
                if kv[0]==k:
                    value=kv[1]
                    print_data.append(kv[2]+':'+str(kv[3])+':'+value+'\n')
            for d in print_data[0:10]:
                f.write(d)
            f.write('...\n'*3)
            for d in print_data[-11:-1]:
                f.write(d)
        else:
            for kv in all_exceptions_list:
                if kv[0]==k:
                    value=kv[1]
                    f.write(kv[2]+':'+str(kv[3])+':'+value+'\n')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            	
    f.write('-'*400+'\n')                                   		    
    # print "*** Total Traceback number: "+str(len(traceback_list))+' ***'
    # f.write("*** Total Traceback number: "+str(len(traceback_list))+' ***'+'\n')
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            	
    # #traceback_list.append([key,value,log,index+1])
    # f.write('\nKeys\n')
    # keys=[item[0] for item in traceback_list]
    # for s in set(keys):
    #     f.write(str(keys.count(s))+': '+s+'\n')
    #
    # f.write('\nLog Path\n')
    # log=[item[2] for item in traceback_list]
    # for s in set(log):
    #     f.write(str(log.count(s))+': '+s+'\n')
    #
    # f.write('\nPython error\n')
    # pythons=[]
    # values=[val[1] for val in traceback_list]
    # for val in values:
    #     split_val=val.split(' ')
    #     for item in split_val:
    #         if item.find('.py')>0:
    #             python_file_name=item
    #             python_msg=val.split('.py')[1]
    #             python=python_file_name+' '+python_msg
    #             pythons.append(python)
    # for s in set(pythons):
    #     f.write(str(pythons.count(s))+': '+s+'\n')
    #


    #f.write('\nTraceback last line\n')
    #last_lines=[]
    #for t in traceback_list:
    #    print '--------------------------------------'
    #    f.write(str(t)+'\n')
    #values=[val[1] for val in traceback_list]
    #for val in values:
    #    split_val=val.split('\n')
    #    for item in split_val:
    #        if item.startswith(' '):
    #            last_line=item
    #            last_lines.append(last_line)
    #for s in set(last_lines):
    #    f.write(str(last_lines.count(s))+': '+s+'\n')	
    #    	    
                                
                                
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            	
    f.write('-'*400+'\n') 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            	
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            	
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            	
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            	
    print "Total "+string_for_grep+" number: "+str(len(all_exceptions_list))
    f.write("Total "+string_for_grep+" number: "+str(len(all_exceptions_list))+'\n')
    print 'Execution time: '+str(round((stop_execution_time-start_execution_time)/60,2))+'[min]'
    f.write('Execution time: '+str(round((stop_execution_time-start_execution_time)/60,2))+'[min]\n')
    print '#'*len('#'*40+' Statistics '+'#'*40)
    f.write('#'*len('#'*40+' Statistics '+'#'*40)+'\n')
f.close() #Close file anyway
