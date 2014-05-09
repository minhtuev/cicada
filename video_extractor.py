import cv2
import os
import pprint
from datetime_extractor import *

# get the length of the video in seconds
def get_video_length(cam):
    return get_num_frames(cam)/get_frame_rate(cam)

def get_frame_rate(cam):
    return cam.get(cv2.cv.CV_CAP_PROP_FPS)

def get_num_frames(cam):
    return cam.get(7)

def print_video_properties(cam):
    print "Video Properties:"
    print "\t Width: ",cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    print "\t Height: ",cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    print "\t FourCC: ",cam.get(cv2.cv.CV_CAP_PROP_FOURCC)
    print "\t Framerate: ",get_frame_rate(cam)
    print "\t Number of Frames: ",get_num_frames(cam)

def process_video(filename, gps_list):
    cam = cv2.VideoCapture(filename)
    print_video_properties(cam)
    # video length in seconds
    video_length = get_video_length(cam)
    video_datetime = get_video_datetime(filename)

    folder_name = filename.split(".")[0]
    # if the folder does not exist, make it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    print "videolength", video_length
    start_time = video_datetime
    end_time = (video_datetime + datetime.timedelta(seconds = video_length))
    print "video start time:", start_time.time()
    print "video end time:", end_time.time()
    
    frame_num = 1
    frame_time = 0
    frame_rate = get_frame_rate(cam)
    max_frame_num = get_num_frames(cam)

    # iterating through all (datetime, lat, lon) and find the proper time interval
    for (dt, lat, lon) in gps_list:
        if (start_time.time() <= dt.time()) and (dt.time() <= end_time.time()):
            frame_time = start_time + datetime.timedelta(seconds = frame_num*1.0/get_frame_rate(cam))
            # navigating toward the exact time
            while abs((frame_time - dt).seconds) > 1 and frame_num <= max_frame_num:
                success, image = vidcap.read()
                frame_num += 1
                frame_time = start_time + datetime.timedelta(seconds = frame_num*1.0/get_frame_rate(cam))
            # while at the exact time, extrac the frame and save
            while abs((frame_time - dt).seconds) < 1 and frame_num <= max_frame_num:
                cv2.imwrite(folder_name + ("/frame%d.jpg" % frame_num), image)
                success, image = vidcap.read()
                frame_num += 1
                frame_time = start_time + datetime.timedelta(seconds = frame_num*1.0/get_frame_rate(cam))        
    cam.release()

filenames = get_video_files()
gps_data = get_all_gps_data()

process_video(filenames[0], gps_data)