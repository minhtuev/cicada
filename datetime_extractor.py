from os import listdir
from os.path import isfile, join
import re
import datetime
from dateutil import parser
import string

def get_files_from_directory(path, pattern):
    onlyfiles = [ f for f in listdir(path) if isfile(join(path,f)) and pattern.match(f)]
    return onlyfiles
    
def get_gps_text_files():
    pattern = re.compile("2014[0-9]*.txt")
    textfiles = get_files_from_directory(".", pattern)
    return textfiles

def get_video_files():
    pattern = re.compile("2014[0-9\_]*.avi")
    videofiles = get_files_from_directory(".", pattern)
    return videofiles

def read_gps_text_file(filename):
    f = open(filename, 'r')
    line = f.readline()
    line = f.readline()
    result = []
    while line != '':
        line = str(line).strip().split(',')
        date_object = parser.parse(line[0])
        date_object -= datetime.timedelta(hours = 4)
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
    filename = filename.split(".")[0]
    filename = filename.split("_")
    filename = string.join(filename[:len(filename) - 1], "-")
    date_object = parser.parse(filename)
    return date_object

print get_gps_text_files()
video_files = get_video_files()
print video_files
print get_video_datetime(video_files[0])
# print get_all_gps_data()