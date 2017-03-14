import pyaudio, wave, math
import socket, sys, time, datetime, os
from collections import deque
import audioop
import zmq

CHUNK = 4096 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SILENCE_LIMIT = 3 
PREV_AUDIO = 1  

context = zmq.Context()

class UnexpectedStateError(Exception):
    pass

class FailedRequestError(Exception):
    pass

class Client:
    def __init__(self, addr):

        self.addr = addr
        self.connect()

    def connect(self):
        statesock = context.socket(zmq.SUB)
        statesock.setsockopt(zmq.LINGER, 0)
        statesock.connect("tcp://"+self.addr+":5560")
        statesock.setsockopt(zmq.SUBSCRIBE,'')
        statesock.SNDTIMEO = 2000
        self.statesock = statesock

        cmdsock = context.socket(zmq.REQ)
        cmdsock.setsockopt(zmq.LINGER, 0)
        cmdsock.connect("tcp://"+self.addr+":5561")
        cmdsock.SNDTIMEO = 2000
        cmdsock.RCVTIMEO = 2000
        self.cmdsock = cmdsock

    def reset(self):
        try:
            self.send("DIE")
        except zmq.ZMQError:
            pass

        self.cmdsock.disconnect("tcp://"+self.addr+":5561")
        self.cmdsock.close()
        self.statesock.disconnect("tcp://"+self.addr+":5560")
        self.statesock.close()
        self.connect()

    def send(self, cmd, msg=""):
        print self.addr, " > ", cmd, msg
        self.cmdsock.send_string(cmd + ":" + msg)
        response = self.cmdsock.recv()
        #print self.addr, "<-", response
        if response == "ERROR":
            raise FailedRequestError("client returned ERROR")

        return response

    def expect(self, expectedstate, timeout=2000):
        print self.addr, "[" + expectedstate + "]"
        self.statesock.RCVTIMEO = timeout
        [state, data] = self.statesock.recv().split(':')
        if state != expectedstate:
            raise UnexpectedStateError("unexpected state " + state)

        return data

def audio_int(num_samples=50):

    print "# measuring noise floor..."
    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK)
    values = [math.sqrt(abs(audioop.avg(stream.read(CHUNK), 4))) 
    for x in range(num_samples)] 
    values = sorted(values, reverse=True)
    r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
    print "# average noise floor: " + "%.2f" % r
    stream.close()
    p.terminate()
    return r

def listen_for_speech(threshold, num_phrases=1):

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print "# listening..."
    audio2send = []
    cur_data = ''
    rel = RATE/CHUNK
    slid_win = deque(maxlen=SILENCE_LIMIT * rel)
    prev_audio = deque(maxlen=PREV_AUDIO * rel) 
    started = False
    n = num_phrases
    response = []

    while (num_phrases == -1 or n > 0):
        cur_data = stream.read(CHUNK)
        slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
        if(sum([x > threshold for x in slid_win]) > 0):
            if(not started):
                print "# voice detected, starting record..."
                started = True
            audio2send.append(cur_data)
        elif (started is True):
            filename = save_speech(list(prev_audio) + audio2send, p)
            started = False
            slid_win = deque(maxlen=SILENCE_LIMIT * rel)
            prev_audio = deque(maxlen=0.5 * rel) 
            audio2send = []
            n -= 1
        else:
            prev_audio.append(cur_data)

    print "# done recording!"
    stream.close()
    p.terminate()

    return response

def save_speech(data, p):

    data = ''.join(data)
    wf = wave.open('output/record.wav', 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(44100) 
    wf.writeframes(data)
    wf.close()
    return 'record.wav'

class Recorder(object):

    def __init__(self, channels=1, rate=44100, frames_per_buffer=512):
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer

    def open(self, fname, mode='wb'):
        return RecordingFile(fname, mode, self.channels, self.rate,
                            self.frames_per_buffer)

class RecordingFile(object):
    def __init__(self, fname, mode, channels, 
                rate, frames_per_buffer):
        self.fname = fname
        self.mode = mode
        self.channels = channels
        self.rate = rate
        self.frames_per_buffer = frames_per_buffer
        self._pa = pyaudio.PyAudio()
        self.wavefile = self._prepare_file(self.fname, self.mode)
        self._stream = None

    def __enter__(self):
        return self

    def __exit__(self, exception, value, traceback):
        self.close()

    def record(self, duration):
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer)
        for _ in range(int(self.rate / self.frames_per_buffer * duration)):
            audio = self._stream.read(self.frames_per_buffer)
            self.wavefile.writeframes(audio)
        return None

    def start_recording(self):
        self._stream = self._pa.open(format=pyaudio.paInt16,
                                        channels=self.channels,
                                        rate=self.rate,
                                        input=True,
                                        frames_per_buffer=self.frames_per_buffer,
                                        stream_callback=self.get_callback())
        self._stream.start_stream()
        return self

    def stop_recording(self):
        self._stream.stop_stream()
        return self

    def get_callback(self):
        def callback(in_data, frame_count, time_info, status):
            self.wavefile.writeframes(in_data)
            return in_data, pyaudio.paContinue
        return callback


    def close(self):
        self._stream.close()
        self._pa.terminate()
        self.wavefile.close()

    def _prepare_file(self, fname, mode='wb'):
        wavefile = wave.open(fname, mode)
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self._pa.get_sample_size(pyaudio.paInt16))
        wavefile.setframerate(self.rate)
        return wavefile