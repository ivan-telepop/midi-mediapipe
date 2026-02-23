import base64
import json
import sys
import cv2
import mediapipe as mp
import os
import time
from cv2.typing import Scalar
from dotenv import dotenv_values
import socket
import mido
import multiprocessing as multi_p


import numpy as np

def calculate_distance(lm1,lm2):
        # Эта функция должна дать расстояние между лендмарками, на основе растояний расчитать интенсивность динамики
        # temp solution
        return np.linalg.norm(np.array([lm1.x, lm1.y, lm1.z]) - np.array([lm2.x, lm2.y, lm2.z]))


port_names = mido.get_output_names()
# Opened MIDI
note = 60

# Note velocity calculator
def velocity_calculator(val):
    return int(val / 4)


def midi_message_handler(port_name: str, msg_data: int, velocity: int):
    """MIDI Message handler - temp solution

    Args:
        port_name (str): one of the opened ports
        msg_data (int): note data sent to port
    """
    with  mido.open_output(port_name) as port:
        init_msg = mido.Message('note_on', velocity=velocity, note=msg_data)
        port.send(init_msg)
        close_msg = mido.Message('note_off', velocity=velocity, note=msg_data)
        port.send(close_msg)


# Named Landmarks

# 0 - WRIST
# 1 - THUMB_CMC
# 2 - THUMB_MCP
# 3 - THUMB_IP
# 4 - THUMB_TIP
# 5 - INDEX_FINGER_MCP
# 6 - INDEX_FINGER_PIP
# 7 - INDEX_FINGER_DIP
# 8 - INDEX_FINGER_TIP
# 9 - MIDDLE_FINGER_MCP
# 10 - MIDDLE_FINGER_PIP
# 11 - MIDDLE_FINGER_DIP
# 12 - MIDDLE_FINGER_TIP
# 13 - RING_FINGER_MCP
# 14 - RING_FINGER_PIP
# 15 - RING_FINGER_DIP
# 16 - RING_FINGER_TIP
# 17 - PINKY_MCP
# 18 - PINKY_PIP
# 19 - PINKY_DIP
# 20 - PINKY_TIP



config = dotenv_values(".env")

# Connecting the webcam
web_cam = cv2.VideoCapture(0) # or 1 if it exist



#hands

mp_hands = mp.solutions.hands

mpDraw = mp.solutions.drawing_utils


with mp_hands.Hands(static_image_mode=False,
                                 max_num_hands=6,
                                 min_tracking_confidence=0.1,
                                 min_detection_confidence=0.5) as hands:

        mpDraw = mp.solutions.drawing_utils
        while True:
            _, image = web_cam.read()
            result = hands.process(image)
            print(result)
            # passing while not hands
            if not result.multi_hand_landmarks:
                print("NO HANDS DETECTED")
                continue
            else:
                # Debug usage prints 
                print("DETECTED LANDMARKS IS:", type(result.multi_hand_landmarks[0]))
                print('Handedness:', result.multi_handedness)
                # Finding needed lm's
                pointers = [4, 8, 12, 16, 20]
                base_knucles = [1,5,9,13,17]
                landmarks_list = [one.landmark for one in result.multi_hand_landmarks]
                for lm_one in pointers:
                    # evaluating distance on pointers 
                    _ind = pointers.index(lm_one) # Retr from pointers index for knowing index for retrieving base_knukles
                    bs_2 = base_knucles[_ind]
                    lm1 = landmarks_list[0][lm_one]
                    lm2 = landmarks_list[0][bs_2]
                    signal_value = calculate_distance(lm1=lm1,lm2=lm2) * 100.5
                    # Striped signal value 
                    signal_strip = str(signal_value).lstrip('-0.')
                    print("SIGNAL VALUE :",int(signal_value)) #signal_strip[1:3])
                for one in result.multi_hand_landmarks:
                    for id, lm in enumerate(one.landmark):
                        image_height, image_width, _ = image.shape
                        c_x, c_y = int(lm.x * image_width), int(lm.y * image_height)
                        cv2.circle(image, (c_x, c_y), 5, (240, 160, 80))
                        # print(
                        #     f'Index finger tip coordinates: (',
                        #     f'{one.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                        #     f'{one.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
                        # )

                        # The grid of keyboard with 60 notes # - This param could be set by user
                        KEYBOARD_GRID_X = image_width / 60 
                        KEYBOARD_GRID_Y = image_height / 60 # TEMP SOLUTIION

                        if id in pointers or id in base_knucles:
                             font = cv2.FONT_HERSHEY_SIMPLEX
                             font_scale = 0.5
                             _color = (0, 189, 69) if id in pointers else (255,51,51) # Green or red color in BGR
                             thickness = 2
                    # \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \          
                             formated_X = str(lm.x).lstrip('-0.')
                             formated_Y = str(lm.y).lstrip('-0.')
                             dot_value = lm.x - lm.y
                             formated_Z = str(lm.z).lstrip('-0.')
                             mark_coords = (c_x,c_y) if lm else (0,0) # Coordinates 
                             try:
                                midi_message_handler(port_name=port_names[0],msg_data=int(signal_value),velocity=120)#msg_data=COORD_MARK)
                             except BaseException as e:
                                 print(f"EXCEPTION: {e}")
                             if mark_coords:
                                cv2.putText(image,str(int(signal_value)),mark_coords, font, font_scale, _color, thickness)
                                # image: Image on which the line will be drawn.
                                # start_point: Starting coordinate (x, y).
                                # end_point: Ending coordinate (x, y).
                                # color: Line color in BGR format (e.g., (0, 255, 0) for green).
                                # thickness: Line thickness in pixels
                                for line_x in range(0,image_width,int(KEYBOARD_GRID_X)):
                                    cv2.line(image, (line_x,0), (line_x, int(image_height)), (12, 238, 238), 1)
                                    #cv2.line(image, (0,line_x), (0, int(image_width)), (12, 238, 238), 1)
                                    
                                    # for line_y in range(0,image_height,int(KEYBOARD_GRID_Y)):
                                    #     cv2.line(image, (line_x, line_y), (line_x, line_y), (255, 0, 0), 2)
                    # PRINT DISTANCE 
                    WHRIST_X = one.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                    WHRIST_Y = one.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                    # Which note ?
                    INDEX_FINGER_TIP_X = one.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                    INDEX_FINGER_TIP_Y = one.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                    
                    # print(f"WHRIST X: {WHRIST_X}    WHRIST Y: {WHRIST_Y}")
                    print(f"INDEX X: {INDEX_FINGER_TIP_X}    INDEX Y: {INDEX_FINGER_TIP_Y}")
             

                    mpDraw.draw_landmarks(image, one, mp.solutions.hands.HAND_CONNECTIONS)


            cv2.imshow('Camera Capturing', image)
            cv2.waitKey(1)
            if cv2.waitKey(1) == ord('q'):
                break