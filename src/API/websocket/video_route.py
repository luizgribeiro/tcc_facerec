from imutils.video import VideoStream
from flask import Response
from flask import Flask, jsonify
from flask import request 
import cv2 
import io
from PIL import Image
from datetime import datetime
import base64
import face_recognition
from PIL import Image
import numpy as np 
import face_recognition
import json
import time




class VideoRoute:

  def __init__(self, frame_cont, socketio):
    self.frame_cont = frame_cont
    self.socketio = socketio 
    self.add_websocket_route(socketio)


  def request_to_frame(self, request):

    request_data = json.loads(request)
    base64_request_string = request_data['image_data'].split(',')[1]
  
    base64_bytes = base64_request_string.encode("utf-8") 
    jpg_file_string = base64.decodestring(base64_bytes) 
    
    nparr = np.fromstring(jpg_file_string, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return frame

  def add_websocket_route(self, socketio):
    socketio.on_event('raw_frame', self.handle_frame)


  def handle_frame(self, request):
    try:
      start = time.time()
      frame = self.request_to_frame(request)

      processed_frame = self.frame_cont.process_frame(frame)

      img_encoded_string = self.frame_cont.gen_jpg_string_from_frame(processed_frame)
      img_string_b64 = base64.encodestring(img_encoded_string)

      self.socketio.emit('processed_frame', {'data': img_string_b64} )
      end = time.time()
      print(f'[INFO]: Tempo total {end-start}')
    except Exception as e:
      print(e)
      self.socketio.emit('broken_frame')






