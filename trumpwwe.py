import cv2
import sys
import imageio
import os
import string
import random

#time to clean this up for server use
def getTracker(frame, bbox):
    tracker = cv2.Tracker_create("MEDIANFLOW")
    tracker.init(frame, bbox)
    return tracker

def main():
    #args = get_args()
    id = sys.argv[1]
	
    # alternative algorithms
    # BOOSTING, KCF, TLD, MEDIANFLOW or GOTURN
    #MEDIANFLOW seems to be the fastest and most accurate for occlusions of dude's face
    tracker = cv2.Tracker_create("MEDIANFLOW")
    # Read video
    # video = cv2.VideoCapture("vid1.mp4")

    # Exit if video not opened.
    # if not video.isOpened():
    #     print("Could not open video")
    #     sys.exit()

    # Read first frame.
    # ok, frame = video.read()
    # if not ok:
    #     print('Cannot read video file')
    #     sys.exit()
    
    imageLoc = "./uploads/" + id + ".jpg"
    my_img = cv2.imread(imageLoc)
    # print('image upload')

    # what it starts tracking, from the first frame
    #dude's face
    frame = cv2.imread('./frames/frame_000.jpg')
    

    bbox = (175, 80, 60, 60)
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    readj_points = {116: (284,176, 50, 50),  148: (285, 199, 30,30)}

    kargs =  {"duration" : .09}
    frame_count = 0
    with imageio.get_writer('./public/gifs/'+id +'.gif', mode='I', **kargs) as writer:
        for filename in sorted(os.listdir("./frames"))[1:]:
            frame = cv2.imread("./frames/" + filename)
            
            #readjust the tracker 
            if frame_count in readj_points:
                tracker = getTracker(frame, readj_points[frame_count])

            #update tracker object
            ok, bbox = tracker.update(frame)

            # tracker there
            if ok:
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                #put in my stuff (resize image then put it in ROI
                assuranceSize = 40
                resized_image = cv2.resize(my_img, (int(bbox[2]+ assuranceSize), int(bbox[3] + assuranceSize)))
                y_coord = int(bbox[1])
                x_coord = int(bbox[0])

                frame[y_coord:y_coord+resized_image.shape[0], x_coord: x_coord + resized_image.shape[1]] = resized_image

            #compress the image
            frame = cv2.resize(frame, (420, 200))
            #write it to the gif 
            if (frame_count % 3 == 1):
                writer.append_data(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            


            frame_count += 1

    print(id)
    #now we generate gif


if __name__ == '__main__':
    main()
