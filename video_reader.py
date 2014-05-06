import cv2
import os

def parse_video_into_frames(file_name, maxCount=float("inf")):
    vidcap = cv2.VideoCapture(file_name)
    folder_name = file_name.split(".")[0]
    # if the folder does not exist, make it
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    success, image = vidcap.read()
    count = 0
    while (success) and (count < maxCount):
        success, image = vidcap.read()
        cv2.imwrite(folder_name + ("/frame%d.jpg" % count), image)
        if cv2.waitKey(10) == 27:
            break
        count += 1
    print "success"

parse_video_into_frames('redwine.mp4')
