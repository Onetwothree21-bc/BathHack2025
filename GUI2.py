import tkinter as tk
from tkinter import font
from tkinter import ttk
import WebScrapper
import SearchingAPI
import classification_algorithm as alg

# --- Theme Settings ---
themes = {
    "light": {
        "bg": "lightblue",
        "text": "#FF1493",
        "entry_bg": "white",
        "button_bg": "#FF69B4",
        "button_fg": "white",
    },
    "dark": {
        "bg": "#1e1e1e",
        "text": "#00FFFF",
        "entry_bg": "#2c2c2c",
        "button_bg": "#444444",
        "button_fg": "#FFFFFF",
    }
}

current_theme = "light"

# --- Initialize Window ---
window = tk.Tk()
window.title("Fake News Detector")
window.geometry("600x400")

# --- Fonts ---
font_title = font.Font(family="Comic Sans MS", size=35, weight="bold")
font_label = font.Font(family="Comic Sans MS", size=20)
font_button = font.Font(family="Comic Sans MS", size=12, weight="bold")


# --- Function to Apply Theme ---
def apply_theme(theme_name):
    theme = themes[theme_name]
    window.configure(bg=theme["bg"])
    main_frame.config(bg=theme["bg"])
    title_label.config(bg=theme["bg"], fg=theme["text"])
    input_frame.config(bg=theme["bg"])
    url_label.config(bg=theme["bg"], fg=theme["text"])
    url_entry.config(bg=theme["entry_bg"], fg="black")
    output_label.config(bg=theme["bg"], fg=theme["text"])
    submit_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
    theme_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
    clear_button.config(bg=theme["button_bg"], fg=theme["button_fg"])


# --- Layout ---
main_frame = tk.Frame(window)
main_frame.pack(expand=True, fill="both")

title_label = tk.Label(main_frame, text="The Cool Kids 😎", font=font_title)
title_label.pack(pady=20)

input_frame = tk.Frame(main_frame)
input_frame.pack(pady=10, padx=20, fill="x")
input_frame.columnconfigure(1, weight=1)

url_label = tk.Label(input_frame, text="Enter news URL:", font=font_label)
url_label.grid(row=0, column=0, padx=5, sticky="w")

entry_var = tk.StringVar()
url_entry = tk.Entry(input_frame, textvariable=entry_var, font=font_label, relief="solid")
url_entry.grid(row=0, column=1, padx=5, sticky="ew")

output_label = tk.Label(main_frame, text="", font=font_label, wraplength=500, justify="center")
output_label.pack(pady=10)

# --- Confidence Meter ---
confidence_var = tk.DoubleVar()
confidence_bar = ttk.Progressbar(main_frame, variable=confidence_var, maximum=100, length=300)

confidence_label = tk.Label(main_frame, text="", font=font_label)



def on_button_click():
    url = entry_var.get().strip()
    """
    if not url:
        output_label.config(text="Please enter a valid URL.")
        confidence_var.set(0)
        confidence_label.config(text="")
        return
    """

    url_entry.delete(0, tk.END)

    try:
        WebScrapper.web_scrapper(url)
        headline = WebScrapper.get_headline(url)
        SearchingAPI.searchArticle(headline)

        # --- Placeholder logic ---
        result = alg.prob(WebScrapper.web_scrapper(url)) # Replace with your model's output
        #is_fake = fake_probability > 50

        # Show progress bar and label
        if not confidence_bar.winfo_ismapped():
            confidence_bar.pack(pady=5)
            confidence_label.pack(pady=5)

        #confidence_var.set(fake_probability)
        #confidence_label.config(text=f"Fake News Probability: {fake_probability:.1f}%")

        
        #result = "❌ Fake News Detected!" if is_fake else "✅ Seems Legit!"

        # Update GUI
        output_label.config(text=f"Headline:\n{headline}\n\nResult: {result}")
        #confidence_var.set(fake_probability)
        #confidence_label.config(text=f"Fake News Probability: {fake_probability:.1f}%")

        if result == 0:
            result = "Fake News"
        else:
            result = "Real News"

    except Exception as e:
        output_label.config(text="⚠️ Error processing the URL.")
        confidence_var.set(0)
        confidence_label.config(text="")
        confidence_bar.forget()
        confidence_label.forget()
        print(f"Error: {e}")

def clear_all():
    entry_var.set("")
    output_label.config(text="")
    confidence_var.set(0)
    confidence_label.config(text="")
    confidence_bar.forget()
    confidence_label.forget()



submit_button = tk.Button(main_frame, text="Analyze", command=on_button_click, font=font_button)
submit_button.pack(pady=10)

clear_button = tk.Button(main_frame, text="Clear", command=clear_all, font=font_button)
clear_button.pack(pady=5)


# --- Theme Toggle Button ---
def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme(current_theme)

theme_button = tk.Button(main_frame, text="Change Theme", command=toggle_theme, font=font_button)
theme_button.pack()

# --- ESC to Exit Fullscreen ---
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))

# --- Resize Title on Window Resize ---
def resize_text(event):
    new_size = max(10, int(event.width / 25))
    font_title.configure(size=new_size)

window.bind("<Configure>", resize_text)

# --- Apply Initial Theme ---
apply_theme(current_theme)

window.mainloop()
