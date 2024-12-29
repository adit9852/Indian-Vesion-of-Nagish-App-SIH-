import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from itertools import count
import tkinter as tk
from tkinter import messagebox
import string
import time

class HearingImpairmentAssistant(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hearing Impairment Assistant")
        self.geometry("600x500")
        self.configure(bg="lightblue")

        self.recognizer = sr.Recognizer()
        self.isl_gif = [...]  # List of GIF phrases as in the original code

        # Add a label for title
        self.title_label = tk.Label(self, text="HEARING IMPAIRMENT ASSISTANT", font=("Helvetica", 20), bg="lightblue")
        self.title_label.pack(pady=20)

        # Microphone image (idle and active)
        self.mic_img_idle = ImageTk.PhotoImage(Image.open("mic_idle.png").resize((50, 50)))
        self.mic_img_active = ImageTk.PhotoImage(Image.open("mic_active.png").resize((50, 50)))

        # Microphone label (to show visual cue)
        self.mic_label = tk.Label(self, image=self.mic_img_idle, bg="lightblue")
        self.mic_label.pack(pady=10)

        # Add buttons to start and quit
        self.start_button = tk.Button(self, text="Start Live Voice", font=("Helvetica", 16), command=self.start_recognition)
        self.start_button.pack(pady=10)

        self.quit_button = tk.Button(self, text="Quit", font=("Helvetica", 16), command=self.quit)
        self.quit_button.pack(pady=10)

        # Add a text area to display recognized speech
        self.result_label = tk.Label(self, text="Recognized Speech:", font=("Helvetica", 14), bg="lightblue")
        self.result_label.pack(pady=10)

        self.result_text = tk.Text(self, height=4, width=50, font=("Helvetica", 14))
        self.result_text.pack(pady=10)

    def start_recognition(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)

            # Update microphone image to active (listening)
            self.mic_label.config(image=self.mic_img_active)
            self.update()  # Force the GUI to update

            messagebox.showinfo("Listening", "Say something")

            try:
                # Listen and recognize speech
                audio = self.recognizer.listen(source)

                # After listening, switch mic back to idle
                self.mic_label.config(image=self.mic_img_idle)
                self.update()

                # Recognize speech using Google API
                recognized_text = self.recognizer.recognize_google(audio)
                recognized_text = recognized_text.lower().translate(str.maketrans("", "", string.punctuation))
                self.result_text.insert(tk.END, f"You said: {recognized_text}\n")

                if recognized_text == "goodbye":
                    self.result_text.insert(tk.END, "Goodbye!\n")
                    return

                if recognized_text in self.isl_gif:
                    self.show_gif(recognized_text)
                else:
                    self.show_alphabet_images(recognized_text)

            except sr.UnknownValueError:
                self.result_text.insert(tk.END, "Sorry, I could not understand the audio.\n")
            except sr.RequestError as e:
                self.result_text.insert(tk.END, f"Could not request results from the speech recognition service; {e}\n")

            # Switch mic image back to idle after processing
            self.mic_label.config(image=self.mic_img_idle)
            self.update()

    def show_gif(self, phrase):
        class ImageLabel(tk.Label):
            def load(self, im):
                if isinstance(im, str):
                    im = Image.open(im)
                self.frames = []
                try:
                    for i in count(1):
                        self.frames.append(ImageTk.PhotoImage(im.copy()))
                        im.seek(i)
                except EOFError:
                    pass

                self.config(image=self.frames[0])
                self.next_frame()

            def next_frame(self):
                if self.frames:
                    self.loc = (self.loc + 1) % len(self.frames)
                    self.config(image=self.frames[self.loc])
                    self.after(self.delay, self.next_frame)

        gif_window = tk.Toplevel(self)
        gif_window.title("Sign Language Translation")
        gif_window.geometry("400x300")
        lbl = ImageLabel(gif_window)
        lbl.pack()
        lbl.load(f'ISL_Gifs/{phrase}.gif')

    def show_alphabet_images(self, text):
        for char in text:
            if char.isalpha():
                image_path = f'letters/{char}.jpg'
                img = Image.open(image_path)
                img_np = np.asarray(img)
                plt.imshow(img_np)
                plt.draw()
                plt.pause(0.8)
        plt.close()

if __name__ == "__main__":
    app = HearingImpairmentAssistant()
    app.mainloop()
