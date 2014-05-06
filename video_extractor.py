import cv2
from datetime_extractor import *

# get the length of the video in seconds
def get_video_length(cam):
    return cam.get(7)/cam.get(cv2.cv.CV_CAP_PROP_FPS)

def process_video(filename, gps_list):
    cam = cv2.VideoCapture(filename)
    print "Video Properties:"
    print "\t Width: ",cam.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    print "\t Height: ",cam.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    print "\t FourCC: ",cam.get(cv2.cv.CV_CAP_PROP_FOURCC)
    print "\t Framerate: ",cam.get(cv2.cv.CV_CAP_PROP_FPS)
    print "\t Number of Frames: ",cam.get(7)
    video_length = get_video_length(cam)
    video_datetime = get_video_datetime(filename)

    print "videolength", video_length
    print video_datetime
    # video_datetime_end = video_datetime + video_length
    # gps_data = get_all_gps_data()
    # frame_num = 0
    # # iterating through all (datetime, lat, lon)
    # for (dt, lat, lon) in gps_data:
    #     if (video_datetime <= dt) and (dt <= video_datetime_end):
    #         print dt

    cam.release()

filenames = get_gps_text_files()
gps_data = get_all_gps_data()

process_video(filenames[0], gps_data)