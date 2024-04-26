import os
import subprocess
import argparse
import tqdm

#set up the argparser
parser = argparse.ArgumentParser()
parser.add_argument("path",help='path to the .sch program to execute')
parser.add_argument('-n','--execution-count',required=False,default=100,type=int,help='number of times to execute the program')
parser.add_argument('-p','-path-to-mp',required=False,default='./')
parser.add_argument('-E', required=False, default=None)
args = parser.parse_args()

if os.path.exists(args.p):
    pathToMP = args.p
else:
    raise FileNotFoundError('MP-SPDZ protocol not found!')


if os.path.exists(args.path):
    pathToProgram = args.path
else:
    raise FileNotFoundError('Path to .sch file is wrong!')

try:
    execution_time_list = []
    for i in tqdm.tqdm(range(args.execution_count)):
        if args.E != None:
            output = subprocess.getstatusoutput(f'{pathToMP} '+f'-E {args.E} 'f'{pathToProgram}')
        else:
            output = subprocess.getstatusoutput(f'{pathToMP} '+f'{pathToProgram}')

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
except KeyboardInterrupt:
    ## pass to allow for neat cleanup
    pass

if args.E != None:
    protocol = args.E
else:
    protocol = os.path.split(pathToMP)[1]

with open(protocol+'.csv','w') as file:
    for time in execution_time_list:
        file.write(f'{time}, ')