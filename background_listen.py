#!/usr/bin/env python

from threading import Thread
from queue import Queue
import speech_recognition as sr


class SpeechToText:
    """
    Converts audio input from microphone to text
    """

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.audio_queue = Queue()
        self.text = ""

    def run(self):

        # function for background thread
        def recognize_worker():
            while True:
                audio = self.audio_queue.get()
                if audio is None: break

                try:
                    chunk = self.recognizer.recognize_google(audio)
                    print(chunk)
                    self.text += chunk + ". "
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print("Could not request results from Google Speech Recognition service; {0}".format(e))

                self.audio_queue.task_done()

        recognize_thread = Thread(target=recognize_worker, daemon=True)
        recognize_thread.start()

        with sr.Microphone() as source:
            try:
                self.recognizer.adjust_for_ambient_noise(source)
                while True:
                    self.audio_queue.put(self.recognizer.listen(source))
            except KeyboardInterrupt:
                pass

        self.audio_queue.join()
        self.audio_queue.put(None)
        recognize_thread.join()


if __name__ == "__main__":
    model = SpeechToText()
    model.run()
    print("final transcript: ")
    print(model.text)
