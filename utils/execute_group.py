import os
import subprocess
import argparse
import tqdm

#set up the argparser
parser = argparse.ArgumentParser()
parser.add_argument("path",help='path to the .sch program to execute')
parser.add_argument('-n','--execution-count',required=False,default=100,type=int,help='number of times to execute the program')
parser.add_argument('-p','-path-to-mp',required=False,default='./')
parser.add_argument('-H','--host',required=False,default='HOSTS')
parser.add_argument('-E', required=False, default=None)
args = parser.parse_args()

if os.path.exists(args.p):
    pathToMP = args.p
else:
    raise FileNotFoundError('MP-SPDZ protocol not found!')

protocols = ['soho','hemi','temi','semi','semi2k','mascot','mama','spdz2k']

for protocol in protocols:
    if os.path.exists(args.path):
        pathToProgram = args.path
    else:
        raise FileNotFoundError('Path to .sch file is wrong!')

    try:
        execution_time_list = []
        communication_rounds = []
        global_data = []
        for i in tqdm.tqdm(range(args.execution_count),desc=f'{protocol}:'):
            output = subprocess.getstatusoutput(f'{pathToMP} -l -H {args.host} -E {protocol} {pathToProgram}')
            try:
                index = str(output[1]).find('Time =')
                string = output[1][index+6:index+14].strip()
                #make sure no chars slip in at the end
                num_length = 0
                for char in string:
                    if char.isalpha():
                        break
                    else:
                        num_length+=1
                execution_time_list.append(float(string[0:num_length]))

                index = str(output[1]).find('Global data sent =')
                string = output[1][index+18:index+26].strip()
                #make sure no chars slip in at the end
                num_length = 0
                for char in string:
                    if char.isalpha():
                        break
                    else:
                        num_length+=1
                global_data.append(float(string[0:num_length]))

                index = str(output[1]).find('~')
                string = output[1][index+1:index+5].strip()
                #make sure no chars slip in at the end
                num_length = 0
                for char in string:
                    if char.isalpha():
                        break
                    else:
                        num_length+=1
                communication_rounds.append(float(string[0:num_length]))
            except ValueError as e:
                print(output)
    except KeyboardInterrupt:
        ## pass to allow for neat cleanup
        pass

    with open(protocol+'_time.csv','w') as file:
        for time in execution_time_list:
            file.write(f'{time}, ')


    with open(protocol+'_rounds.csv','w') as file:
        for time in communication_rounds:
            file.write(f'{time}, ')


    with open(protocol+'_data.csv','w') as file:
        for time in global_data:
            file.write(f'{time}, ')
