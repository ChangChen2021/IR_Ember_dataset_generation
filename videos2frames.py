from fileinput import filename
import os
import math
from tempfile import NamedTemporaryFile
import cv2
from glob import glob
from itertools import cycle
from coordination_dict import coordination_dict

# crop a 64*64 window
# let user decide which area to crop
def crop_frame(frame, x, y):
    size = 32
    cropped_frame = frame[y - size: y + size, x - size: x + size]
    return cropped_frame

def save_frame(video_path, save_dir, x, y):
    cap = cv2.VideoCapture(video_path)
    frameRate = cap.get(5) # frame rate
    # idx = 0
    num = 32
    pool = cycle(list(range(0, num)))
    # rectangle the place
    success,image = cap.read()
    while success:
        color =  (0, 255, 0)
        orignal_image = image
        result_image = cv2.rectangle(orignal_image, (x-32, y-32), (x+32, y+32), color, 2)
        cv2.imwrite(f"{save_dir}/{name}" + "_" + f"{x:03d}" + f"{y:03d}.jpg", result_image)     # save frame as JPEG file      
        break

    while True:
        frameNum = cap.get(1) # current frame number
        ret, frame = cap.read()
        if ret == False:
            cap.release()
            break
        # how many (5) frames in second
        ratio = frameNum % math.floor(frameRate)
        ratio_list = [0, 5, 10, 15, 20, 25]

        if (ratio in ratio_list):
            itr = next(pool)
            cropped_frame = crop_frame(frame, x, y)
            # ! it is the naming problem !
            # check if the directory exist
            folderName = f"{name +'_'}" + f"{x:04d}" + f"{y:04d}"
            # + f"{idx:06d}"
            folder_dir = save_dir + "/" + folderName
            if(os.path.exists(folder_dir) == False):
                os.mkdir(folder_dir)
            fileName = f"{folder_dir}/{folderName}" + "_" + f"{itr:02d}.jpg"
            print(fileName)
            cv2.imwrite(fileName, cropped_frame)
            if (itr == 31):
                # idx = idx + 1
                break

if __name__ == "__main__":
    # all videos under the same directory
    video_paths = glob('**/*.mp4')
    
    for path in video_paths:
        print(path)
        # all videos
        # use the dates to name the files
        # ! below two lines are redundent! 
        save_dir = path.split(".")[0]
        print(save_dir)
        name = os.path.basename(save_dir)
        
        # # get the x, y coordinate
        # x_axis = input("Enter x axis value: ")
        # y_axis = input("Enter y axis value: ")
        x_axis = coordination_dict[name]['x']
        y_axis = coordination_dict[name]['y']
        
        for x,y in zip(x_axis, y_axis):
            if ((y + 32 < 480) and (y - 32 > 0) and (x + 32 < 720) and (x - 32 > 0)):
                # check if the directory exist
                if(os.path.exists(save_dir) == False):
                    os.mkdir(save_dir)
                save_frame(path, save_dir, x, y)

        