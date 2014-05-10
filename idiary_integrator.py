import requests
import base64
import json
import pprint
from dateutil import parser
from datetime_extractor import get_video_files, get_all_gps_data
from video_extractor import process_video

def encode_image(image_path):
    """This function reads an image file as binary and encodes it as a b64 string"""
    # read binary
    f = open(image_path, 'rb')
    rawImage = f.read()
    f.close()
    encoded = base64.encodestring(rawImage)
    return encoded

def parse_frame_results(folder_name):
    results = []
    f = open(folder_name + "/results.txt", 'r')
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        tokens = line.split(",")
        frame_num = int(tokens[0])
        dt = parser.parse(tokens[1])
        lat = float(tokens[2])
        lon = float(tokens[3])
        results.append((frame_num, dt, lat, lon))
    f.close()
    return results

def dump_to_html(content, filename = "response.html"):
    f = open(filename, 'w')
    f.write(content)
    f.close()

def integrate_video_frames(folder_name, frame_results, username = "Mikhail"):
    """This function takes the path to the generated folder and the frame results
    and send to the server"""
    # url = "http://127.0.0.1:8000/lab/image/"
    url = "http://128.31.33.218/lab/image/"
    for (frame_num, dt, lat, lon) in frame_results:
        filename = folder_name + "/" + ("/frame%d.jpg" % frame_num)
        rawString = encode_image(filename)        
        timestamp = str(dt)
        tag = "Mikhail video batch 1"
        extension = "jpg"
        data = {"rawImage":rawString,\
                "latitude": lat,\
                "longitude":lon,\
                "timestamp":timestamp,\
                "tag":tag,\
                "extension":extension,\
                "username":username,\
                }
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, data = json.dumps(data), headers = headers)
        print r.status_code
        if r.status_code == 500:
            dump_to_html(r.content)

def process_all_video_files(id = 0):
    filenames = get_video_files()
    pprint.pprint(filenames)
    gps_data = get_all_gps_data()
    for index, filename in enumerate(filenames):
        if index >= id:
            print "Extracting frames for", filename
            process_video(filename, gps_data, seconds_delta = 1)
    print "done"

process_all_video_files(1)
# folder_name = filename.split(".")[0]      
#results = parse_frame_results(folder_name)
#integrate_video_frames(folder_name, results)