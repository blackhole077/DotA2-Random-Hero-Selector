import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO
from random_hero_select import RandomHeroSelectManager as RandomHeroSelectManager

class RandomHeroSelectGui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DotA2 Random Hero Selector")
        self.root.resizable(0,0)
        self.manager = RandomHeroSelectManager()
        self.canvas = tk.Canvas(self.root, bg='red')
        self.frame1 = tk.Frame(self.canvas, bd=1)
        self.frame2 = tk.Frame(self.canvas, bg='purple')
        self.current_image = ImageTk.PhotoImage(Image.open('images/default_vert.jpg'))
        self.photo_placeholder = tk.Label(self.frame1, image=self.current_image)
        self.photo_placeholder.image = self.current_image
        self.photo_placeholder.pack(side='top', padx=(10, 10), pady=(10,10))
        self.hero_text = tk.StringVar()
        self.photo_label = tk.Label(self.frame1, textvariable=self.hero_text, height=1)
        self.photo_label.config(font=("Courier", 18))
        self.photo_label.pack(padx=(10, 10), pady=(10, 10))
        self.current_image = None
        self.button = tk.Button(self.frame1, text='Next Hero Please!', height=5, width=32, command = lambda: self.manager.callback_generate_random_hero(self.photo_placeholder, self.photo_label, self.hero_text))
        self.label = tk.Label(self.frame2, text="Right-Hand-Side Info")
        self.label.pack(side='left')
        self.button.pack(side='bottom', padx=(10, 10), pady=(10, 10))
        self.frame1.pack(side='left')
        self.frame2.pack(side='right')
        self.canvas.pack()
        self.root.mainloop()


r = RandomHeroSelectGui()