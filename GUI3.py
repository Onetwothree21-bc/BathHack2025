import tkinter as tk
from tkinter import font, ttk
import WebScrapper  # Replace with your actual webscrapper module

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
window.geometry("600x500")

# --- Fonts ---
font_title = font.Font(family="Comic Sans MS", size=35, weight="bold")
font_label = font.Font(family="Comic Sans MS", size=18)
font_button = font.Font(family="Comic Sans MS", size=12, weight="bold")

# --- Scrollable Canvas Setup ---
canvas = tk.Canvas(window, highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# --- Layout ---
title_label = tk.Label(scrollable_frame, text="The Cool Kids 😎", font=font_title)
title_label.pack(pady=20)

input_frame = tk.Frame(scrollable_frame)
input_frame.pack(pady=10, padx=20, fill="x")
input_frame.columnconfigure(1, weight=1)

url_label = tk.Label(input_frame, text="Enter news URL:", font=font_label)
url_label.grid(row=0, column=0, padx=5, sticky="w")

entry_var = tk.StringVar()
url_entry = tk.Entry(input_frame, textvariable=entry_var, font=font_label, relief="solid")
url_entry.grid(row=0, column=1, padx=5, sticky="ew")

# --- Output Label (clean look, no white box) ---
output_label = tk.Label(scrollable_frame, text="", font=font_label, wraplength=500, justify="center")
output_label.pack(pady=10)

# --- Confidence Meter ---
confidence_var = tk.DoubleVar()
confidence_bar = ttk.Progressbar(scrollable_frame, variable=confidence_var, maximum=100, length=300)
confidence_label = tk.Label(scrollable_frame, text="", font=font_label)

# --- Output and Prediction Logic ---
def on_button_click():
    url = entry_var.get().strip()
    if not url:
        show_output("Please enter a valid URL.")
        hide_confidence()
        return

    url_entry.delete(0, tk.END)

    try:
        WebScrapper.web_scrapper(url)
        headline = WebScrapper.get_headline(url)

        # Placeholder logic
        fake_probability = 73.6
        is_fake = fake_probability > 50
        result = "❌ Fake News Detected!" if is_fake else "✅ Seems Legit!"

        show_output(f"Headline:\n{headline}\n\nResult: {result}")
        show_confidence(fake_probability)

    except Exception as e:
        show_output("⚠️ Error processing the URL.")
        hide_confidence()
        print(f"Error: {e}")

def show_output(text):
    output_label.config(text=text)

def show_confidence(value):
    confidence_var.set(value)
    confidence_label.config(text=f"Fake News Probability: {value:.1f}%")
    if not confidence_bar.winfo_ismapped():
        confidence_bar.pack(pady=5)
        confidence_label.pack(pady=5)

def hide_confidence():
    confidence_var.set(0)
    confidence_label.config(text="")
    confidence_bar.forget()
    confidence_label.forget()

# --- Buttons ---
submit_button = tk.Button(scrollable_frame, text="Analyze", command=on_button_click, font=font_button)
submit_button.pack(pady=10)

def clear_all():
    entry_var.set("")
    output_label.config(text="")
    hide_confidence()

clear_button = tk.Button(scrollable_frame, text="Clear", command=clear_all, font=font_button)
clear_button.pack(pady=5)

# --- Theme Switching ---
def apply_theme(theme_name):
    theme = themes[theme_name]
    window.configure(bg=theme["bg"])
    canvas.config(bg=theme["bg"])
    scrollable_frame.config(bg=theme["bg"])
    title_label.config(bg=theme["bg"], fg=theme["text"])
    input_frame.config(bg=theme["bg"])
    url_label.config(bg=theme["bg"], fg=theme["text"])
    url_entry.config(bg=theme["entry_bg"], fg="black")
    output_label.config(bg=theme["bg"], fg=theme["text"])
    submit_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
    clear_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
    theme_button.config(bg=theme["button_bg"], fg=theme["button_fg"])
    confidence_label.config(bg=theme["bg"], fg=theme["text"])

def toggle_theme():
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    apply_theme(current_theme)

theme_button = tk.Button(scrollable_frame, text="Change Theme", command=toggle_theme, font=font_button)
theme_button.pack(pady=5)

# --- ESC to Exit Fullscreen ---
window.bind("<Escape>", lambda e: window.attributes("-fullscreen", False))

# --- Font Resize on Window Resize ---
def resize_text(event):
    new_size = max(10, int(event.width / 25))
    font_title.configure(size=new_size)

window.bind("<Configure>", resize_text)

# --- Scroll with Mouse ---
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))   # Linux

# --- Apply Initial Theme ---
apply_theme(current_theme)

window.mainloop()
