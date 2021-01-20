import os
import re
import socket
import sys
import threading
import time
# import thread module
from _thread import start_new_thread
from datetime import datetime

import pyaudio

# Audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4000 #250 ms audio in a chunk
RECORD_SECONDS = 20

PORT = 9001
HOST = "127.0.0.1"

def socket_stream(s):
    while(1):
        data = s.recv(1024)
        if data:
            print('Data', datetime.now().time() , data)

def main():
    host = ""
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    audio = pyaudio.PyAudio()


    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

    #In ASR - first 44 bytes are assume wav header
    #For wav - first 44 bytes is the wav file header
    s.send(b'1111111111-1111111111-1111111111-1111111111-')

    start_new_thread(socket_stream, (s,))

    for i in range(0, int((RATE / CHUNK) * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        #print('data...', i)
        s.send(data)

    print("finished streaming and Shutting down")
    stream.stop_stream()
    stream.close()
    audio.terminate()
    s.close()


if __name__ == '__main__':
    main()
