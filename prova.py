#!/usr/bin/env python3

import sys
import os
import io
import binascii
import math
from PIL import Image

MAL_PATH = "C:/Users/Carlo/Documents/VisualStudioCode/Progetto Python system-calls/samples_mal"
TRUST_PATH = "C:/Users/Carlo/Documents/VisualStudioCode/Progetto Python system-calls/samples_trust"
PROJ_PATH = "C:/Users/Carlo/Documents/VisualStudioCode/Progetto Python system-calls"
START_COL = 28  # colonna da cui inizia la stringa della syscall

'''metodo da eliminare'''


def str_to_colorscale(string):
    bit = "0"
    pixel_list = []
    #print(string)
    for i in string[:3]:
        bit = "".join("{:8b}".format(ord(i)))
        pixel_list.append(int(bit, 2))
    pixel = tuple(pixel_list)
    # print(pixel_list)
    return pixel


'''nuovo'''


def split_bit_str(string):
    split_strings = []
    n = 8
    for index in range(n, len(string)+1, n):
        decimal_str = str((int(string[index - n: index], 2)))
        split_strings.append(int(decimal_str))
    return split_strings


def logs_files():
    for file in os.listdir(TRUST_PATH):
        yield file


def img_generator(lines):
    '''conteggio le righe per la dimensione dell'immagine'''
    k = 0
    # print(len(lines))
    for line in lines:
        try:
            if line == '\n' or line[START_COL] == "<" or line[START_COL] == "-":
                continue
            if line[START_COL] == "+":
                #print ('found +' + string)
                break
        except IndexError:
            # print('lol')
            continue
        k += 1
        # print(k)
    # print(k)
    '''genero pixelmap e immagine'''
    dim = int(math.sqrt(k))+1
    img = Image.new('RGB', (dim, dim), 'white')
    pixMap = img.load()
    return img, pixMap, dim


def syscall_extract(string):
    j = 0
    sys_call = ""
    for char in string[START_COL:]:
        if string[START_COL+j] == "(" or string[START_COL+j] == "<" or string[START_COL] == "-":
            break
        sys_call += char
        j += 1
    return sys_call


def fil_image(pixmap, pixel, x, y, dim):

    if x < dim:
        pixmap[x, y] = pixel
        x += 1
    else:
        x = 0
        y += 1
        pixmap[x, y] = pixel
        x += 1

    return x, y, pixmap


'''nuovo'''


def bit_string_compression(string, n, e):
    compressed_string = ""
    i = n
    len_s = len(string)
    #print(str(n) + ' ' + str(len_s))
    # print(string[i-n+e:i])

    while (i <= len_s):
        #print(str(i-e+1) + '-- ' + str(i-1))
        for char in string[i-n+e:i]:
            compressed_string += char
        i += n
    return compressed_string


'''nuovo'''


def str_to_rgb(sys_call):
    n = len(sys_call)
    to_remove = n*8-24
    e = int(to_remove / 8)
    _string = ""
    #bit = "0"
    for i in sys_call:
        bit = "".join("{:8b}".format(ord(i))) 
        bit_str = str((int(bit, 10)))
        while len(bit_str) < 8:
            bit_str = '0' + bit_str

        _string += bit_str

    '''comprimo la stringa in modo univoco'''
    compressed_string = bit_string_compression(_string, n, e)

    '''la splitto di 8 in 8 bit'''
    split_strings = split_bit_str(compressed_string)

    return tuple(split_strings)


def lines_reader(lines, pixMap, dim):
    x, y = 0, 0  # coordinate pixelmap
    '''loop per le righe'''

    for line in lines:
        string = line
        #print(string)

        try:
            if line == '\n' or line[START_COL] == "<" or line[START_COL] == "-":
                continue
            if line[START_COL] == "+":
                #print ('found +' + string)
                break
        except IndexError:
            # print('lol')
            continue

        '''prendo la porzione di stringa che mi interessa'''
        sys_call = syscall_extract(string)
        if len(sys_call) < 3: 
            continue

        '''genero pixel e inserisco nella pixelmap--> fatto male'''
        # single_pixel = str_to_colorscale(sys_call[:3]) #passo solo i primi 3 char della syscall

        '''NUOVO -> genero dalla sys_call i valori RGB'''
        single_pixel = str_to_rgb(sys_call)
        '''costruisco pixMap'''
        if y < dim:
            x, y, pixMap = fil_image(pixMap, single_pixel, x, y, dim)
        else:
            print("erore dimensione immagine")
            break

    return pixMap


def file_reader(files):
    '''loop per i file'''
    for file in files:

        file_p = TRUST_PATH + '/' + file
        print(file_p)

        file_reader = open(file_p, 'r')
        lines = file_reader.readlines()

        '''genero le immagini'''
        img, pixMap, dim = img_generator(lines)
        pixMap = lines_reader(lines, pixMap, dim)

        file_name = file.split(".")
        lenght = len(file_name)
        file_name_final = ""
        for n in file_name[:lenght-2]:
            file_name_final += n + '.'

        img.save(PROJ_PATH + '/' + 'output' + '/' + file_name_final + 'png')


'''scrittura su arff, dato che mi sono dimenticato'''


def fill_arff(files):
    arff_p = PROJ_PATH + '/' + 'legitimate_vs_malware.txt'
    file_writer = open(arff_p, 'w+')
    for file in files:      
        file_name = file.split(".")
        lenght = len(file_name)
        file_name_final = ""
        for n in file_name[:lenght-2]:
            file_name_final += n + '.'
        file_name_final += 'png' + ',TRUSTED'
        # print(file_name_final)
        file_writer.write(file_name_final + '\n')
    file_writer.close


def read_file(file_p):
    file_reader = open(file_p, 'r')
    lines = file_reader.readlines()

    for line in lines:
        try:
            if line == '\n' or line[START_COL] == "<" or line[START_COL] == "-":
                continue
            if line[START_COL] == "+":
                #print ('found +' + string)
                break
        except IndexError:
            # print('lol')
            continue

    img, pixMap, dim = img_generator(lines)
    pixMap = lines_reader(lines, pixMap, dim)


if __name__ == "__main__":
  
    files = list(logs_files())
    #file_reader(files)
    fill_arff(files)
    
