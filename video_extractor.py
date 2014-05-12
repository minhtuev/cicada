import cv2
import os
import datetime
import string
from datetime_extractor import get_video_datetime

# get the length of the video in seconds
def get_video_length(cam):
    """ Return the length of the video cam = cv2.VideoCapture"""
    return get_num_frames(cam)/get_frame_rate(cam)

def get_frame_rate(cam):
    """ Return the frame rate of the video cam = cv2.VideoCapture"""
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

def process_video(filename, gps_list, seconds_delta = 1, folder_name = None):
    cam = cv2.VideoCapture(filename)
    print_video_properties(cam)
    # video length in seconds
    video_length = get_video_length(cam)
    video_datetime = get_video_datetime(filename)

    # if the folder name is not supplied, we use the file name
    if folder_name is None:
        folder_name = filename.split(".")[0]

    # if the folder does not exist, make it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    print "videolength:", video_length
    start_time = video_datetime
    end_time = (video_datetime + datetime.timedelta(seconds = video_length))
    print "video start time:", start_time.time()
    print "video end time:", end_time.time()
    
    success, image = cam.read()            
    frame_num = 1
    frame_time = 0
    max_frame_num = get_num_frames(cam)
    results = []
    frame_count = 0
    # iterating through all (datetime, lat, lon) and find the proper time interval
    for (dt, lat, lon) in gps_list:
        if (start_time.time() <= dt.time()) and (dt.time() <= end_time.time()):
            frame_time = start_time + datetime.timedelta(seconds = frame_num*1.0/get_frame_rate(cam))
            print "Extracting frames for" , dt, ", at coordinates:", lat, lon 
 
            # navigating toward the exact time
            while abs((frame_time - dt).seconds) > seconds_delta and frame_num <= max_frame_num:
                success, image = cam.read()
                frame_num += 1
                frame_time = start_time + datetime.timedelta(seconds = frame_num*1.0/get_frame_rate(cam))
 
            # while at the exact time, extrac the frame and save
            while abs((frame_time - dt).seconds) < seconds_delta and frame_num <= max_frame_num:
                results.append((frame_num, dt, lat, lon))
                cv2.imwrite(folder_name + ("/frame%d.jpg" % frame_num), image)
                success, image = cam.read()
                frame_count += 1
                frame_num += 1
                frame_time = start_time + datetime.timedelta(seconds = frame_num*1.0/get_frame_rate(cam))
    cam.release()
    print "Number of frames extracted:", frame_count

    # write the summary to a file:
    f = open(folder_name + "/results.txt", 'w')
    for (frame_num, dt, lat, lon) in results:
        line = string.join([str(frame_num), str(dt), str(lat), str(lon)], ",") + "\n"
        f.write(line)
    f.close()

    return results