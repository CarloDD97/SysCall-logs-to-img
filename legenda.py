#!/usr/bin/env python3

import sys, os, io

DIR_PATH = "C:/Users/Carlo/Documents/VisualStudioCode/Progetto Python system-calls/all"
DIR_PATH2 = "C:/Users/Carlo/Documents/VisualStudioCode/Progetto Python system-calls/samples_trust"
PROJ_PATH = "C:/Users/Carlo/Documents/VisualStudioCode/Progetto Python system-calls"
START_COL = 28 #colonna da cui inizia la stringa della syscall
SYS_CALL_TABLE = [[],[]]
PEZZA = ['0','0','0','0','0','0','0']

def sys_call_list(sys_call):
    exist = False
    for call in SYS_CALL_TABLE[0]:
        if sys_call == call:
            exist = True
            break

    if not exist:
        SYS_CALL_TABLE[0].append(sys_call)

def syscall_extract(string):
    j = 0
    sys_call = ""
    for char in string[START_COL:]:
        if string[START_COL+j] == "(" or string[START_COL+j] == "<":
            break
        sys_call += char
        j += 1
    return sys_call

def lines_reader(lines):
    for line in lines:
        try:
            if line == '\n' or line[START_COL] ==  "<" or line[START_COL] == "-":
                continue            
            if line[START_COL] == "+":
                #print ('found +' + string)
                break
        except IndexError:
            #print('lol')
            continue              
                   
        '''prendo la porzione di stringa che mi interessa'''            
        sys_call = syscall_extract(line)
        if len(sys_call) < 3: 
            continue
        sys_call_list(sys_call)     


def logs_files():
    i = 0
    for file in os.listdir(DIR_PATH2):
        if i >=5: #limite di 5 file (di prova)
            break
        yield file
        i+=1  
    
    

def file_reader(files):
    '''loop per i file'''
    for file in files:       

        file_p = DIR_PATH2 + '/' + file
        #print(file_p)
        
        file_reader = open(file_p, 'r')
        lines = file_reader.readlines()
        lines_reader(lines)

def bit_string_compression(string, n, e):
    compressed_string = ""
    i = n
    len_s = len(string)
    #print(str(n) + ' ' + str(len_s))
    #print(string[i-n+e:i])
    
    while (i <= len_s):        
        #print(str(i-e+1) + '-- ' + str(i-1))        
        for char in string[i-n+e:i]:
            compressed_string += char        
        i += n   
    return compressed_string

def split_bit_str(string):
    split_strings = []
    n  = 8
    for index in range(n, len(string)+1, n):
        decimal_str = str((int(string[index - n : index], 2)))
        split_strings.append(decimal_str)
    return split_strings

def str_to_rgb(sys_call):
    n = len(sys_call)
    to_remove = n*8-24
    e = int(to_remove /8)
    bit_string = ""
    #bit = "0"
    for i in sys_call:
        bit = "".join("{:8b}".format(ord(i)))
        bit_str = str((int(bit, 10)))
        while len(bit_str) < 8:
            bit_str = '0' + bit_str
                
        bit_string += bit_str

    '''comprimo la stringa in modo univoco'''
    compressed_string = bit_string_compression(bit_string, n, e)
    
    '''la splitto di 8 in 8 bit'''
    split_strings = split_bit_str(compressed_string)

    return split_strings

    #print(compressed_string + ' len: ' + str(len(compressed_string)))
    #print(split_strings)


def color_list():
    i = 0
    for call in SYS_CALL_TABLE[0]:
        #color = hexadecimal_color_syscall(call)
        rgb = str_to_rgb(call)
        SYS_CALL_TABLE[1].append(rgb)
        #print(call + ' :' + rgb[0] + ', '+ rgb[1] + ', '+ rgb[2])
        #print(call + ' ' + ''.join(SYS_CALL_TABLE[1][i][0]) + ", " + ''.join(SYS_CALL_TABLE[1][i][1]) + ", " +''.join(SYS_CALL_TABLE[1][i][2]))
        i+=1

def writer():
    file_p = PROJ_PATH + '/legend.txt'
    f = open(file_p, 'w+')
    i = 0
    for call in SYS_CALL_TABLE[0]:
        string = (call + ' ' + ''.join(SYS_CALL_TABLE[1][i][0]) + ", " + ''.join(SYS_CALL_TABLE[1][i][1]) + ", " +''.join(SYS_CALL_TABLE[1][i][2]))
        print(string)
        f.write(string + "\n" )
        i+=1

    f.close

if __name__ == "__main__":
    '''
    str_to_rgb('write22') 
    '''
    files = list(logs_files())
    file_reader(files)
    SYS_CALL_TABLE[0].sort(reverse=False)
    color_list()
    writer()
    #print(SYS_CALL_TABLE)
    
    