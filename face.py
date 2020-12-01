import os
import cv2
import sys
import face_recognition as fb


# cap = cv2.VideoCapture("test03.mp4")
cap = cv2.VideoCapture(0)
face_list=[]

while True:
    # Grab a single frame of video
    ret, frame = cap.read()
    # print(ret, frame)
    # Convert the image from BGR color (which OpenCV uses) to RGB
    # color (which face_recognition uses)
    rgb_frame = frame[:, :, ::-1]
    # Find all the faces in the current frame of video
    face_locations = fb.face_locations(rgb_frame)
    print(face_locations)
    for top, right, bottom, left in face_locations:
        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0,
                                                            255), 2)
    # Display the resulting image
    cv2.imshow('Video', frame)

    # Wait for Enter key to stop
    if cv2.waitKey(5) == 13:
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()