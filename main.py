import threading
import subprocess

import cv2
import imutils

capture = cv2.VideoCapture(0)

capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

ok, start_frame = capture.read()
if not ok or start_frame is None:
    raise SystemExit(
        "Could not read from camera. Check System Settings → Privacy & Security → "
        "Camera and enable Terminal (or Cursor)."
    )

start_frame = imutils.resize(start_frame, width=500)
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

alarm = False
alarm_mode = False
alarm_counter = 0

def beep_alarm():
    global alarm

    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM!!!")
        subprocess.run(["afplay", "resources/mixkit-classic-alarm-995.wav"])
    alarm = False

print("Camera ready. Press 't' to arm, 'q' to quit. Click the Cam window first.")

while True:
    ok, frame = capture.read()
    if not ok or frame is None:
        print("Lost camera frame.")
        break

    frame = imutils.resize(frame, width=500)

    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        if threshold.sum() > 300000:
            print(threshold.sum())
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1

        cv2.imshow("Cam", threshold)
    else:
        cv2.imshow("Cam", frame)

    if alarm_counter > 20:
        if not alarm:
            alarm = True
            threading.Thread(target=beep_alarm).start()

    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
        print("Alarm mode:", "ON" if alarm_mode else "OFF")
    elif key_pressed == ord("q"):
        alarm_mode = False
        break

capture.release()
cv2.destroyAllWindows()
