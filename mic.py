#!/usr/bin/env python

import pyaudio
import socket
import select

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
CHUNK = 1024

audio = pyaudio.PyAudio()

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('', 1339))
serversocket.listen(5)


def callback(data, frame_count, time_info, status):
    #for s in read_list[1:]:
      #  continue
    print('data :',data)
    return (None, pyaudio.paContinue)


# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=callback)
# stream.start_stream()

read_list = [serversocket]
print ("recording...")

try:
    while True:
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is serversocket:
                (clientsocket, address) = serversocket.accept()
                read_list.append(clientsocket)
                print ("Connection from", address)
            else:
                data = s.recv(1024)
                print (address, ' >> ', data.strip())
                if not data:
                    read_list.remove(s)
#                s.send(b'<?xml version=\"1.0\"?>\n <result>\n <interpretation grammar=\"builtin:speech/transcribe\" confidence=\"0.000\">\n <input mode=\"speech\">Hello-mrit</input>\n <instance>en-IN</instance>\n </interpretation>\n </result>')
except KeyboardInterrupt:
    pass


print ("finished recording")

serversocket.close()
# stop Recording
stream.stop_stream()
stream.close()
audio.terminate()
