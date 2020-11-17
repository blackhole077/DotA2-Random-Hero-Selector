import tkinter as tk
import tkinter.ttk as ttk
from io import BytesIO
from typing import Union, Dict, List

import requests
from PIL import Image, ImageTk

from random_hero_select import \
    RandomHeroSelectManager as RandomHeroSelectManager

class Checkbar(tk.Frame):
    def __init__(self, parent=None, picks=None, side="left", anchor="w"):
        tk.Frame.__init__(self, parent)
        self.vars = []
        self.labels = picks

        for pick in picks:
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text=pick.capitalize(), variable=var)
            chk.pack(side=side, anchor=anchor, expand="yes")
            self.vars.append(var)
    
    def state(self):
        return map((lambda var: var.get()), self.vars)
    
    def clear(self):
        for var in self.vars:
            var.set(0)

    def fetch_selected_labels(self):
        return  [value for (value, filter) in zip(self.labels, [var.get() for var in self.vars]) if filter]

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
    def __init__(self, parent: Union['tkinter.Frame', 'tkinter.Canvas'], filter_name: str, filter_values: List[str]) -> None:
        self.upper_filter = tk.Frame(parent, bg='grey')
        name = filter_name.replace('_', ' ').title()
        self.upper_filter_label = tk.Label(self.upper_filter, text=f"Filter by {name}")
        self.upper_filter.pack(side='top')
        self.upper_filter_label.pack(side='top')
        self.checkboxes = Checkbar(parent, filter_values)
        self.checkboxes.pack()
        s = tk.ttk.Separator(self.upper_filter, orient=tk.HORIZONTAL)
        s.pack()

class FilterPanel:
    def __init__(self, parent: Union['tkinter.Frame', 'tkinter.Canvas'], filter_dict: Dict[str, List[str]], logic_layer: RandomHeroSelectManager):
        self.filter_parent = tk.ttk.Labelframe(parent, text='Filters')
        self.filters = {}
        for key, value in filter_dict.items():
            filter = FilterGui(self.filter_parent, key, value)
            self.filters[key] = filter.checkboxes
        self.filter_button_frame = tk.Frame(parent)
        self.filter_application_button = tk.Button(self.filter_button_frame, text='Apply Filters', width=10, height=1, fg='blue', command= lambda: logic_layer.callback_generate_masks(self.filters))
        self.filter_clear_button = tk.Button(self.filter_button_frame, text='Clear Filters', width=10, height=1, fg='blue', command= lambda: logic_layer.callback_clear_masks(self.filters))
        self.filter_application_button.pack(side='left')
        self.filter_clear_button.pack(side='right')
        self.filter_parent.pack(side='top', padx=(10, 10), pady=(10, 10))
        self.filter_button_frame.pack(side='bottom', padx=(10, 10), pady=(10, 10))

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
        self.filter_frame = FilterPanel(self.main_canvas, self.manager.gui_config, self.manager)
        # Run the root window GUI
        self.root.mainloop()


if __name__ == "__main__":
    r = RandomHeroSelectGui()
