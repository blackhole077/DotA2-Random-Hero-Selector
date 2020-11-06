import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO

class RandomHeroSelectGui:
    def __init__(self):
        root = tk.Tk()
        root.title = "Test GUI"
        root.geometry = ('600x600')
        canvas = tk.Canvas(root, bg='red')
        frame1 = tk.Frame(canvas, bd=1, bg='blue')
        frame2 = tk.Frame(canvas, bg='purple')
        button = tk.Button(frame1, text='Next Hero Please!', height=5, width=32)
        url = "http://cdn.dota2.com/apps/dota2/images/heroes/axe_vert.jpg"
        response = requests.get(url)
        img = ImageTk.PhotoImage(Image.open(BytesIO(response.content)))
        photo_canvas = tk.Canvas(frame1, bg='brown', height=272, width=235)
        photo_canvas.create_image(235, 272, anchor='se', image=img)
        label = tk.Label(frame2, text="Right-Hand-Side Info")
        photo_canvas.pack(side='top', padx=(10, 1), pady=(10,10))
        label.pack(side='left')
        button.pack(side='left', padx=(10, 1), pady=(10, 10))
        frame1.pack(side='left')
        frame2.pack(side='right')
        canvas.pack()
        root.mainloop()
    
    def fetch_image(self):
        # Check if the file exists already locally

        #If not make a request and fetch it from the web and save it
        pass

    def create_image_holder(self, parent, image_width, image_height):
        self.photo_canvas = tk.Canvas(parent, height=image_height, width=image_width)