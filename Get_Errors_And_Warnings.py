#!/usr/bin/python
import os,sys
from datetime import datetime
def DELETE_LOG_CONTENT(log_file_name):
    f = open(log_file_name, 'w')
    f.write('')
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

#####################################################################
## Env name##
try:
    env_name=sys.argv[2]
except:
    env_name='shachar'

## Grep by time ###
try:
    grep=sys.argv[1]
except:
    #grep=raw_input('Enter date, for example <2014-05-11 10:34:43>: ')
    grep='2015-01-13 10:34:43'

## Output file name ##
try:
    output_file_name=sys.argv[3]
except:
    output_file_name='Exceptions_And_Warnings'+"_"+env_name

## Log path ##
try:
    log_path=sys.argv[4]
except:
    log_path='.'



### Prepare output file ###     
DELETE_LOG_CONTENT(output_file_name)
sys.stdout=MyOutput(output_file_name)
sys.stderr=MyOutput(output_file_name)
logs=[fil for fil in os.listdir(log_path) if fil.endswith('.log')]

### Lines to Grep ###
#keys=['warning','error']
keys=['ERROR']#,'WARN']
total_exception=0

### Find relevant line for search ###
relevant_start_line=None
for log in logs:
    data=open(os.path.join(log_path,log),'r').readlines()
    for line in reversed(data):
        try:
            line_date=line.split(',')[0]
            #start=line_date.find('2016')
            #line_date=line_date[start:]
            line_date=datetime.strptime(line_date,"%Y-%m-%d %H:%M:%S")
            delta=line_date-datetime.strptime(grep,"%Y-%m-%d %H:%M:%S")
            if str(delta).startswith('-')==True:
                relevant_start_line=data.index(line)
                print relevant_start_line
                break
        except:
            pass

    ### Save errors and warnings ### 
    lines_to_save=[]
    if relevant_start_line!=None and env_name!='All':
        line_counter=relevant_start_line
        for line in data[relevant_start_line:]:
            split_line=line.split(',')
            for key in keys:
                if key in line:
                    lines_to_save.append(line_counter)
            line_counter+=1

    for i in lines_to_save:
        try:
            total_exception+=1
            print '\r\n'+'#'*50+' '+log+' '+'#'*50
            print data[i-3].strip().replace('#','\r')
            print data[i-2].strip().replace('#','\r')
            print data[i-1].strip().replace('#','\r')
            print data[i].strip().replace('#','\r')
            print data[i+1].strip().replace('#','\r')
            print data[i+2].strip().replace('#','\r')
            print data[i+3].strip().replace('#','\r')
            print data[i+4].strip().replace('#','\r')
            print data[i+5].strip().replace('#','\r')
            print data[i+6].strip().replace('#','\r')
            print data[i+7].strip().replace('#','\r')
            print data[i+8].strip().replace('#','\r')
            print data[i+9].strip().replace('#','\r')
            print data[i+10].strip().replace('#','\r')
            print data[i+11].strip().replace('#','\r')
            print data[i+12].strip().replace('#','\r')
            print data[i+13].strip().replace('#','\r')
            print data[i+14].strip().replace('#','\r')
            print data[i+15].strip().replace('#','\r')
            print data[i+16].strip().replace('#','\r')
            print data[i+17].strip().replace('#','\r')
            print data[i+18].strip().replace('#','\r')
            print data[i+19].strip().replace('#','\r')
            print data[i+20].strip().replace('#','\r')
            print data[i+21].strip().replace('#','\r')
            print data[i+22].strip().replace('#','\r')
            print data[i+23].strip().replace('#','\r')
            print data[i+24].strip().replace('#','\r')
            print data[i+25].strip().replace('#','\r')
        except:
            pass


SPEC_PRINT(['Total exceptions number:',str(total_exception)])
