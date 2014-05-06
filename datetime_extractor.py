from os import listdir
from os.path import isfile, join
import re
import datetime
from dateutil import parser

def get_gps_text_files():
    mypath = "."
    onlyfiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]
    pattern = re.compile("2014")
    onlyfiles = [ f for f in onlyfiles if pattern.match(f)]
    return onlyfiles

def read_gps_text_file(filename):
    f = open(filename, 'r')
    line = f.readline()
    line = f.readline()
    result = []
    while line != '':
        line = str(line).strip().split(',')
        date_object = parser.parse(line[0])
        # remove noises
        if (date_object.year == 2014):
            result.append((date_object, float(line[1]), float(line[2])))
        line = f.readline()
    return result

def get_all_gps_data():
    files = get_gps_text_files()
    gps_data = []
    for gps_file in files:
        gps_data.extend(read_gps_text_file(gps_file))
    return gps_data

def get_deltas():
    gps_data = get_all_gps_data()
    for i in range(len(gps_data) - 1):
        delta =  gps_data[i+1][0] - gps_data[i][0]
        print gps_data[i+1], gps_data[i]

def get_video_datetime(filename):
    pass


# print get_all_gps_data()