import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

count=0

position=0

# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)
        imlist=[]
        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS)
            for id, im in enumerate(results.pose_landmarks.landmark):
                h,w,_=image.shape
                X,Y=int(im.x*w),int(im.y*h)
                imlist.append([id,X,Y])


        if ((imlist[12][2] - imlist[14][2])>=15 and (imlist[11][2] - imlist[13][2])>=15):
            position = "down"
        if ((imlist[12][2] - imlist[14][2])<=5 and (imlist[11][2] - imlist[13][2])<=5) and position == "down":
            position = "up"
            count +=1 
            print(count)

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('Push-up counter', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break   
cap.release()