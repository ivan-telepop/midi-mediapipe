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
# S O C K E T   C L I E N T

import numpy as np

def calculate_distance(lm1,lm2):
    return np.linalg.norm(np.array([p1.x, p1.y, p1.z]) - np.array([p2.x, p2.y, p2.z]))


port_names = mido.get_output_names()
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

# Getting the webcam
web_cam = cv2.VideoCapture(0) # or 1 durring second camera connected



#hands

hands = mp.solutions.hands.Hands(static_image_mode=False,
                                 max_num_hands=6,
                                 min_tracking_confidence=0.1,
                                 min_detection_confidence=0.5)

mpDraw = mp.solutions.drawing_utils


with mp.solutions.hands.Hands(static_image_mode=False,
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
                print(" *** DETECTED LEN:", len(result.multi_hand_landmarks))
                print("DETECTED HANDS:", result.multi_hand_landmarks)
                print('Handedness:', result.multi_handedness)
                # Handedness: [classification {
                #   index: 1
                #   score: 0.901068747
                #   label: "Right"
                # }
                
                for one in result.multi_hand_landmarks:
                    print(f"TYPE AND LENGHT OF RESULT: {len(result.multi_hand_landmarks)}")
                    
                    for id, lm in enumerate(one.landmark):
                        print("ID=  ", id)
                        print("Landmark=   ", lm)
                        image_height, image_width, _ = image.shape
                        c_x, c_y = int(lm.x * image_width), int(lm.y * image_height)
                        cv2.circle(image, (c_x, c_y), 5, (240, 160, 80))
                        pointers = [4, 8, 12, 16, 20]
                        base_knucles = [1,5,9,13,17]
                        #distances_between_knuckles = [calculate_distance(pointers[ind],base_knucles[ind]) for ind in range(len(pointers))]
                        if id in pointers or id in base_knucles:
                             print("LANDMARK_POSITION IS : X",int(lm.x) ,"Y : ",int(lm.y))
                             print("ID OF LANDMARK IS ",id)
                             # FONT & DRAW TEXT PARAMS
                             font = cv2.FONT_HERSHEY_SIMPLEX
                             font_scale = 0.5
                             _color = (0, 189, 69) if id in pointers else (255,51,51) # Green or red color in BGR
                             thickness = 2
                    # \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \          
                             # Just created some digit mark for understanding how to handle coords and comunicate with the MIDI
                             # Intermediate work but it will help to do later more then i did
                             formated_X = str(lm.x).lstrip('-0.')
                             formated_Y = str(lm.y).lstrip('-0.')
                             dot_value = lm.x - lm.y
                             formated_Z = str(lm.z).lstrip('-0.')
                             #mark_coords = (int(formated_X[:3]), int(formated_Y[:3]))
                             mark_coords = (c_x,c_y) if lm else (0,0)
                             COORD_MARK = str(dot_value).lstrip('-0.') #f"X: {int(formated_X[:3])} Y: {int(formated_Y[:3])}"
                             # Sending to another process
                             try:
                                # mido_process = multi_p.Process(target=midi_message_handler,args=(port_names[0],int(COORD_MARK[1:3])))
                                # mido_process.start()
                                # mido_process.join()
                                midi_message_handler(port_name=port_names[0],msg_data=int(COORD_MARK[1:3]))
                             except BaseException as e:
                                 print(f"EXCEPTION IS: {e}", f"Current data is:{str(COORD_MARK[1:3])}")
                             if mark_coords:
                                cv2.putText(image,COORD_MARK[1:3],mark_coords, font, font_scale, _color, thickness)
                    mpDraw.draw_landmarks(image, one, mp.solutions.hands.HAND_CONNECTIONS)
            cv2.imshow('Camera Capturing', image)
            cv2.waitKey(1)
            if cv2.waitKey(1) == ord('q'):
                break