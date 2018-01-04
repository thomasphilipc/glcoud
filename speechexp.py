import io
import os
import pyaudio
import wave
import audioop

from google.cloud import  speech
from google.cloud.speech import enums
from google.cloud.speech import types


#audio format


def record_audio():

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = 10
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=44100,
                input=True,
                frames_per_buffer=CHUNK)
    print("* recording")

    frames=[]

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        mx = audioop.max(data,2)
        print (mx)
        frames.append(data)

    print("done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# The name of the image file to annotate
path = os.path.join(
    os.path.dirname(__file__),
    'output.wav')


def create_audio(path):


    with io.open(path, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)

    return audio


config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=44100,
        language_code='en-US')


def process_audio(audio,config):
    client = speech.SpeechClient()
    response = client.recognize(config, audio)
    # Print the first alternative of all the consecutive results.
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))


record_audio()

print("opening audio file")
audio=create_audio(path)

print("process audio file")
process_audio(audio,config)