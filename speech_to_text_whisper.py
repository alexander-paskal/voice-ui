import pyaudio
import wave
import threading
import queue
from faster_whisper import WhisperModel

model = WhisperModel("tiny", device="cpu", compute_type="int8")



# Settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 2


def record_audio():

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    audio_queue = queue.Queue()

    def audio_thread():
        while True:
            frames = []
            for _ in range(int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)

            audio_data = b''.join(frames)
            audio_queue.put(audio_data)

    threading.Thread(target=audio_thread, daemon=True).start()

    return audio_queue


def transcribe_realtime():
    audio_queue = record_audio()

    while True:
        if not audio_queue.empty():
            audio_data = audio_queue.get()

            # save temporary audio file
            with wave.open("temp_audio.wav", "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(audio_data)

            # TRANSCRIBE
            segments, info = model.transcribe("temp_audio.wav", beam_size=1)
            for segment in segments:
                return segment.text
                print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
        


if __name__ == "__main__":
    transcribe_realtime()
