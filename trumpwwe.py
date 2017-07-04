import cv2
import sys

if __name__ == '__main__':
    # i stole like more than half this shit
    # Set up tracker.
    
	# Instead of MIL, you can also use
    # BOOSTING, KCF, TLD, MEDIANFLOW or GOTURN
    #MEDIANFLOW seems to be the fastest and most accurate for occlusions of dude's face
    tracker = cv2.Tracker_create("MEDIANFLOW")
    # Read video
    video = cv2.VideoCapture("vid1.mp4")

    # Exit if video not opened.
    if not video.isOpened():
        print("Could not open video")
        sys.exit()

    # Read first frame.
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    my_img = cv2.imread("yashface.png")

    # Define an initial bounding box
    bbox = (180, 83, 60, 60)

    # Uncomment the line below to select a different bounding box
    # bbox = cv2.selectROI(frame, False)

    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)

    while True:
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break

        # Update tracker
        ok, bbox = tracker.update(frame)

        # Draw bounding box
        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            #put in my stuff (resize image then put it in ROI
            assuranceSize = 40
            resized_image = cv2.resize(my_img, (int(bbox[2]+ assuranceSize), int(bbox[3] + assuranceSize)))
            y_coord = int(bbox[1])
            x_coord = int(bbox[0])
            frame[y_coord:y_coord+resized_image.shape[0], x_coord: x_coord + resized_image.shape[1]] = resized_image

            # cv2.rectangle(frame, p1, p2, (0, 0, 255))

        # Display result
        cv2.imshow("Tracking", frame)

        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27: break