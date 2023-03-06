import cv2
import mediapipe as mp
import pyautogui

# initialize mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# initialize video capture object
cap = cv2.VideoCapture(0)

# define volume control range
VOLUME_RANGE = [0, 100]

# initialize current volume
current_volume = 50

while True:
    # read frame from video capture object
    success, frame = cap.read()
    if not success:
        continue

    # convert frame to RGB format
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # detect hands in the frame
    results = hands.process(frame)

    # extract landmarks from the detected hands
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # extract the landmark points for the index and thumb
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

            # calculate the distance between the index and thumb
            distance = ((index_finger.x - thumb.x) ** 2 + (index_finger.y - thumb.y) ** 2) ** 0.5

            # if the distance is less than a certain threshold, increase the volume
            if distance > 0.05:
                current_volume += 3
                current_volume = min(current_volume, VOLUME_RANGE[1])
                pyautogui.press('volumeup')

            # if the distance is greater than a certain threshold, decrease the volume
            elif distance < 0.2:
                current_volume -= 3
                current_volume = max(current_volume, VOLUME_RANGE[0])
                pyautogui.press('volumedown')

    # convert frame back to BGR format for display
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    # display the frame
    cv2.imshow('Hand Gesture Volume Control', frame)

    # check for key press
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# release video capture object and close all windows
cap.release()
cv2.destroyAllWindows()