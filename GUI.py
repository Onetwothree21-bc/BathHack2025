import tkinter as tk
from tkinter import font

import WebScrapper

window = tk.Tk()
window.title("Fake new detector")
window.geometry("600x400")
window.configure(bg="lightblue")

def resize_text(event):
    # Dynamically calculate new font size based on window width
    new_size = max(10, int(event.width / 25))
    font_title.configure(size=new_size)
window.bind("<Configure>", resize_text)

font_title = font.Font(family = "Comic Sans MS", size = 35, weight = "bold")
font_label = font.Font(family = "Comic Sans MS", size = 24)
font_button = font.Font(family = "Comic Sans MS", size = 12, weight = "bold")
bg_color = "lightblue"
entry_bg = "lightblue"
button_color = "#FF69B4"
button_fg = "white"

def unfull_screen(event=None):
    window.attributes("-fullscreen", False)
window.bind("<Escape>", unfull_screen)

main_frame = tk.Frame(window, bg=bg_color)
main_frame.pack(expand=True, fill="both")

title = tk.Label(main_frame, text="The Cool Kids 😎", font=font_title, bg="lightblue", fg="#FF1493")
title.pack(pady = 20)

input_frame = tk.Frame(main_frame, bg=bg_color)
input_frame.pack(pady = 20)

label = tk.Label(input_frame, text="Enter news URL", font=font_label, bg="lightblue", fg="#FF1493")
label.grid(row = 0, column = 0, padx = 5)

entry = tk.Entry(input_frame,  bg="lightblue")
entry.grid(row = 0, column = 1, padx = 5)

def button_click():
    url = entry.get()
    entry.delete(0, tk.END)
    WebScrapper.web_scrapper(url)

button = tk.Button(main_frame, text = "Enter", command = button_click, font=font_button,
                   bg=button_color, fg=button_fg, relief="raised", bd=4)
button.pack(pady = 20)

window.mainloop()