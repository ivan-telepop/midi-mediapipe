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





def midi_message_handler(port_name: str, msg_data: int):
    """MIDI Message handler - temp solution

    Args:
        port_name (str): one of the opened ports
        msg_data (int): note data sent to port
    """
    with  mido.open_output(port_name) as port:
        init_msg = mido.Message('note_on', note=msg_data)
        port.send(init_msg)
        close_msg = mido.Message('note_off', note=msg_data)
        port.send(close_msg)







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
                        print(
                            f'Index finger tip coordinates: (',
                            f'{one.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
                            f'{one.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
                        )
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
                             COORD_MARK = int(signal_value)
                             try:
                                midi_message_handler(port_name=port_names[0],msg_data=int(signal_value))#msg_data=COORD_MARK)
                             except BaseException as e:
                                 print(f"EXCEPTION: {e}")
                             if mark_coords:
                                cv2.putText(image,str(COORD_MARK),mark_coords, font, font_scale, _color, thickness)
                    mpDraw.draw_landmarks(image, one, mp.solutions.hands.HAND_CONNECTIONS)
            cv2.imshow('Camera Capturing', image)
            cv2.waitKey(1)
            if cv2.waitKey(1) == ord('q'):
                break