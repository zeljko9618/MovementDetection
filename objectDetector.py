import cv2 as cv
import os
import time

# Ensure the "screenshots" directory exists
if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

video = cv.VideoCapture(1)  # 1 means I am using my second camera

first_frame = None
screenshot_count = 0

while True:
    check, frame = video.read()
    # Converting frames from bgr to gray
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray_blur_frame = cv.GaussianBlur(gray_frame, (3, 3), 0)
    # 3 needs to be positive and odd, higher number, higher blur

    if first_frame is None:
        first_frame = gray_blur_frame

    # Difference between first frame and all others
    delta_frame = cv.absdiff(first_frame, gray_blur_frame)

    # Threshold on binary frame
    thresh_frame = cv.threshold(delta_frame, 60, 255, cv.THRESH_BINARY)[1]

    # Removing noises from the frame
    cleaned_frame = cv.dilate(thresh_frame, None, iterations=2)

    # Counters around the objekt
    contours, check = cv.findContours(image=cleaned_frame, mode=cv.RETR_EXTERNAL, method=cv.CHAIN_APPROX_SIMPLE)
    for contour in contours:

        # ignore small objects
        if cv.contourArea(contour) < 4000:
            continue
        x, y, w, h = cv.boundingRect(contour)

        # creating a rectangle with two points x,y the first one and x+w,y+h
        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        # Wait for 1 second before saving the screenshot
        time.sleep(1)
        screenshot_count += 1
        filename = f"screenshots/screenshot{screenshot_count}.png"
        cv.imwrite(filename, frame)
        print(f"Screenshot saved as {filename}")

    # Display the resulting frame
    cv.imshow("Video", frame)

    # Exit option
    key = cv.waitKey(1)
    if key == ord("q"):
        break

# Release the video capture object and close all OpenCV windows
video.release()
cv.destroyAllWindows()