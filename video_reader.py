import cv2


def parse_video_into_frames(fileName, maxCount=float("inf")):
    vidcap = cv2.VideoCapture(fileName)
    folderName = fileName.split(".")[0]
    print folderName
    success, image = vidcap.read()
    count = 0
    while (success) and (count < maxCount):
        success, image = vidcap.read()
        cv2.imwrite("test1/frame%d.jpg" % count, image)
        if cv2.waitKey(10) == 27:
            break
        count += 1
    print "success"

parse_video_into_frames('pigeon.mp4')
