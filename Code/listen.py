import json
import pyaudio
from vosk import Model, KaldiRecognizer


MODEL_PATH = "vosk-model-small-ru-0.22"

model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
MICROPHONE_INDEX = 2

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=16000,
    input_device_index=MICROPHONE_INDEX,
    input=True,
    frames_per_buffer=8000
)

stream.start_stream()
print("Listening...")
def listening():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "").strip()
            if text:
                yield text
      
            