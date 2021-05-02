from imutils.video import VideoStream
from flask import Response
from flask import Flask, jsonify
from flask import request 
import cv2 
import io
from flask_socketio import send, emit
from PIL import Image
from datetime import datetime
import base64
import face_recognition
from PIL import Image
import numpy as np 
import face_recognition
import json
import logging
import csv
import time 
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler('./detection_log.csv')
file_handler.setLevel(logging.DEBUG)

formater = logging.Formatter('%(message)s')
file_handler.setFormatter(formater)

logger.addHandler(file_handler)


class VideoRoute:

  def __init__(self, frame_cont , socketio):
    self.frame_cont = frame_cont
    self.socketio = socketio 
    self.add_websocket_route()


  def request_to_frame(self, request):

    request_data = json.loads(request)
    base64_request_string = request_data['image_data'].split(',')[1]
  
    base64_bytes = base64_request_string.encode("utf-8") 
    jpg_file_string = base64.decodestring(base64_bytes) 
    
    nparr = np.fromstring(jpg_file_string, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return frame

  def add_websocket_route(self):
    self.socketio.on_event('raw_frame', self.handle_frame)


  def handle_frame(self, request):
    start = time.time()
    try:
      sid = json.loads(request)['socket_id']
      frame = self.request_to_frame(request)

      processed_frame, detected_faces = self.frame_cont.process_frame(frame)

      img_encoded_string = self.frame_cont.gen_jpg_string_from_frame(processed_frame)
      img_string_b64 = base64.encodestring(img_encoded_string)

      emit('processed_frame', {'data': img_string_b64}, room=sid)

      if detected_faces is None:
        n_faces = 0
      else:
        n_faces = len(detected_faces)

      if n_faces:
        emit('update_list', {"faces": detected_faces}, room=sid )
      
      end = time.time()
      logger.debug(f'{sid},{end - start},{n_faces},{start},{end}')
    except Exception as e:
      print(e)
      emit('broken_frame', room=sid)
