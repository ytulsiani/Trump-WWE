import cv2
import sys
import imageio
import os
import string
import random

#time to clean this up for server use

def main():
    #args = get_args()
    id = sys.argv[1]

    # alternative algorithms
    # BOOSTING, KCF, TLD, MEDIANFLOW or GOTURN
    #MEDIANFLOW seems to be the fastest and most accurate for occlusions of dude's face
    tracker = cv2.Tracker_create("MEDIANFLOW")
    # Read video
    video = cv2.VideoCapture("vid1.avi")

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    imageLoc = "./uploads/" + id + ".jpg"
    my_img = cv2.imread(imageLoc)
    print('image upload')

    # what it starts tracking, from the first frame
    #dude's face
    bbox = (180, 83, 60, 60)


    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    img_list = []
    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        # Update tracker
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
            img_list.append(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    print("done processing gif")
    #now we generate gif

    kargs =  {"duration" : .02}
    with imageio.get_writer('./public/gifs/'+id +'.gif', mode='I', **kargs) as writer:
        # for filename in sorted(os.listdir("./frames"), key= lambda x : int(x.split(".")[0])):
        #     image = imageio.imread("./frames/" + filename)
        #     writer.append_data(image)
        for image in img_list:

            writer.append_data(image)
if __name__ == '__main__':
    main()
