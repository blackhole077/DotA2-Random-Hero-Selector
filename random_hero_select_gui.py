import tkinter as tk
import tkinter.ttk as ttk
from io import BytesIO
from typing import Union

import requests
from PIL import Image, ImageTk

from random_hero_select import \
    RandomHeroSelectManager as RandomHeroSelectManager


class HeroPortrait:
    """
        The subcomponent that contains the hero portraits for the DotA2 Random Hero Selector.

        This GUI sub-component serves to house the photo container, as well as
        a text box that indicates the name of the hero the image belongs to.

        Attributes
        ----------
        current_image: ImageTk.PhotoImage
            The image that is currently displayed. A default image is loaded
            upon initialization.
        photo_placeholder: tkinter.Label
            A label that serves to house the image.
            NOTE: Originally a Canvas was used for this purpose,
            but ultimately Label proved more understandable for this project.
        photo_label: tkinter.Label
            A label that houses the name of the hero the image belongs to.
        hero_text: tkinter.StringVar
            A variable that holds the actual mutable text data corresponding
            to the randomly selected hero.

        Parameters
        ----------
        parent: tkinter.Frame
            The Frame (or Frame) that will contain this subcomponent
        
        Returns
        -------
        None.
    """

    def __init__(self, parent: Union['tkinter.Frame', 'tkinter.Canvas']) -> None:
        self.current_image = ImageTk.PhotoImage(Image.open('images/default_vert.jpg'))
        self.photo_placeholder = tk.Label(parent, image=self.current_image)
        self.photo_placeholder.image = self.current_image
        self.photo_placeholder.pack(side='top', padx=(10, 10), pady=(10,10))
        self.hero_text = tk.StringVar()
        self.photo_label = tk.Label(parent, textvariable=self.hero_text, height=1)
        self.photo_label.config(relief=tk.SUNKEN)
        self.photo_label.config(font=("Courier", 18))
        self.photo_label.pack(padx=(10, 10), pady=(10, 10))

class FilterGui:
    def __init__(self, parent: Union['tkinter.Frame', 'tkinter.Canvas']) -> None:
        self.filter_parent = tk.ttk.Labelframe(parent, text='Filters')
        self.upper_filter = tk.Frame(self.filter_parent, bg='grey')
        self.upper_filter_label = tk.Label(self.upper_filter, text="Upper Filter Section")
        self.upper_filter.pack(side='top')
        self.upper_filter_label.pack(side='top')
        self.lower_filter = tk.Frame(self.filter_parent, bg='green')
        self.lower_filter_label = tk.Label(self.lower_filter, text="Lower Filter Section")
        s = tk.ttk.Separator(self.lower_filter, orient=tk.HORIZONTAL)
        s.pack()
        self.lower_filter.pack(side='bottom')
        self.lower_filter_label.pack(side='top')
        self.filter_parent.pack(padx=(10, 10), pady=(10, 10))

class RandomHeroSelectGui:
    """
        The main GUI component for the DotA2 Random Hero Selector.

        This GUI component serves as the main hub that houses the
        Hero Portrait component, along with the random button.
        
        NOTE: In future updates, this will also house the FilterGUI
        and its children components.

        Attributes
        ----------
        root: tkinter.Tk
            The root window that will contain all
            GUI components.
        manager: random_hero_select.RandomHeroSelectManager
            The custom class that serves as the logic
            layer for randomly selecting heroes.
            It also contains all callback functions.
        main_canvas: tkinter.Canvas
            The main canvas that houses all components.
        hero_portrait: HeroPortrait
            A custom component that contains the hero portrait.
            For more information, look at the class documentation
            for HeroPortrait.
        random_button: tkinter.Button
            A component used to activate the random hero selection.


        Parameters
        ----------
        None.

        Returns
        -------
        None.

    """

    def __init__(self) -> None:
        # Create the root window
        self.root = tk.Tk()
        # Set the title
        self.root.title("DotA2 Random Hero Selector")
        # Turn off resizing
        self.root.resizable(0,0)
        # Load in the random selection logic
        self.manager = RandomHeroSelectManager()
        # Create the main canvas
        self.main_canvas = tk.Canvas(self.root, bg='black')
        # Pack the main canvas
        self.main_canvas.pack()
        # Generate the hero portrait component and attach it
        self.hero_portrait_frame = tk.Frame(self.main_canvas)
        self.hero_portrait = HeroPortrait(self.hero_portrait_frame)
        # Pack the HeroPortrait component into the main canvas
        self.hero_portrait_frame.pack(side='left')
        # Create the Random button and attach the approprate callback parameters from the HeroPortrait component
        self.random_button = tk.Button(self.hero_portrait_frame, text='Next Hero Please!', height=5, width=32, command = lambda: self.manager.callback_generate_random_hero(self.hero_portrait.photo_placeholder, self.hero_portrait.photo_label, self.hero_portrait.hero_text))
        # Make the button look raised
        self.random_button.config(relief=tk.RAISED)
        # Pack the button towards the bottom of the hero_portait frame (bottom-left) with padding.
        self.random_button.pack(side='bottom', padx=(10, 10), pady=(10, 10))
        self.filter_frame = FilterGui(self.main_canvas)
        # Run the root window GUI
        self.root.mainloop()


if __name__ == "__main__":
    r = RandomHeroSelectGui()
