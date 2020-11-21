import tkinter as tk
import tkinter.ttk as ttk
from io import BytesIO
from os import getcwd
from os.path import join
from tkinter import filedialog, messagebox
from typing import Dict, Iterable, List, Union
from json import JSONDecodeError
import requests
from PIL import Image, ImageTk

from random_hero_select import \
    RandomHeroSelectManager as RandomHeroSelectManager


class Checkbar(tk.Frame):
    """
        Create a row or grid of checkboxes.

        Attributes
        ----------
        vars: List[tkinter.Checkbutton]
            The list of checkboxes.
        labels: List[str]
            The names attached to the checkboxes, as well as the
            potential value of a given checkbox if fetch_selected_labels.

        Parameters
        ----------
        parent: Union[tkinter.Frame, tkinter.Canvas]
            The parent container or component the Checkbar is attached to.
        labels: List[str]
            The list of labels for the checkboxes.
        max_per_row: int
            The maximum number of checkboxes allowed before a new row is created.
            Default behavior will create only one row if the number of checkboxes
            (determined by the length of labels) is less than or equal to this value.
        
        Returns
        -------
        None.
    """

    def __init__(self, parent:Union['tk.Frame', 'tk.Canvas'], labels:List[str], max_per_row: int=5) -> None:
        tk.Frame.__init__(self, parent)
        self.vars = []
        self.labels = labels
        row = 0
        column = 0
        for index, label in enumerate(labels):
            if len(labels) > max_per_row:
                if index % max_per_row == 0:
                    row += 1
                    column = 0
            var = tk.IntVar()
            chk = tk.Checkbutton(self, text="{:20s}".format(label.replace("_", " ").title()), variable=var)
            chk.grid(row=row, column=column, sticky='w')
            column += 1
            self.vars.append(var)
    
    def state(self) -> Iterable[int]:
        """
            Fetch the state of all checkboxes in the Checkbar.

            Parameters
            ----------
            None.

            Returns
            -------
            checkbox_states: Iterable[int]
                A map object that contains integer values between [0,1] that
                indicate whether the checkbox is toggled on or not.
        """

        return map((lambda var: var.get()), self.vars)
    
    def clear(self) -> None:
        """
            Clear all checkboxes in the Checkbar.

            Clears all checkboxes by setting their value to 0.

            Parameters
            ----------
            None.

            Returns
            -------
            None.
        """

        for var in self.vars:
            var.set(0)

    def fetch_selected_labels(self) -> List[str]:
        """
            Fetch the labels of the checkboxes that were toggled in the Checkbar.

            Parameters
            ----------
            None.

            Returns
            -------
            selected_labels: List[str]
                A list of all labels whose checkboxes were toggled.
        """

        return [label_value for (label_value, checkbox_value) in zip(self.labels, list(self.state())) if checkbox_value]

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
        parent: Union[tkinter.Frame, tkinter.Canvas]
            The Frame (or Frame) that will contain this subcomponent
        
        Returns
        -------
        None.
    """

    def __init__(self, parent: Union['tk.Frame', 'tk.Canvas']) -> None:
        self.current_image = ImageTk.PhotoImage(Image.open('images/default_vert.jpg'))
        self.photo_placeholder = tk.Label(parent, image=self.current_image)
        self.photo_placeholder.image = self.current_image
        self.photo_placeholder.pack(side='top', padx=(10, 10), pady=(10,10))
        self.hero_text = tk.StringVar()
        self.photo_label = tk.Label(parent, textvariable=self.hero_text, height=1)
        self.photo_label.config(relief=tk.SUNKEN)
        self.photo_label.config(font=("Courier", 18))
        self.photo_label.pack(padx=(10, 10), pady=(10, 10))

class FilterGUI:
    """
        The subcomponent used to generate checkbox-based filters for the DotA2 Random Hero Selector.

        Attributes
        ----------
        filter_parent: tkinter.Frame
            A basic container to house the checkboxes.
        filter_parent_label: tkinter.Label
            The label that contains the name of the filter.
        checkboxes: Checkbar
            The checkboxes used to control which filters, if any, are to be applied.

        Parameters
        ----------
        parent: Union[tkinter.Frame, tkinter.ttk.Labelframe, tkinter.Canvas]
            The parent container or component the FilterPanel is attached to.
        filter_name: str
            The name of the filter. Should correspond to some value present
            in the hero_configuration JSON file.
        filter_values: List[str]
            The list of possible values that are allowed to be toggled.
        
        Returns
        -------
        None.
    """

    def __init__(self, parent: Union['tk.Frame', 'tk.ttk.Labelframe', 'tk.Canvas'], filter_name: str, filter_values: List[str]) -> None:
        self.filter_parent = tk.Frame(parent)
        name = filter_name.replace('_', ' ').title()
        self.filter_parent_label = tk.Label(self.filter_parent, text=f"Filter by {name}")
        self.filter_parent.pack(side='top')
        self.filter_parent_label.pack(side='top')
        s = tk.ttk.Separator(self.filter_parent, orient=tk.HORIZONTAL)
        s.pack(fill='x')
        self.checkboxes = Checkbar(self.filter_parent, filter_values)
        self.checkboxes.pack(padx=(10, 10), pady=(10, 10))

class FilterPanel:
    """
        The secondary GUI component for the DotA2 Random Hero Selector.

        This GUI component houses multiple subcomponents, along with
        two buttons that control the application/removal of filters.

        Attributes
        ----------
        filter_parent: tkinter.ttk.Labelframe
            A container that houses all filters.
        filters: Dict[str, Checkbox]
            A dictionary structure that maps the names
            of the filters along with their respective checkboxes.
            This is passed to the manager/logic_layer for filtering the hero pool.
        filter_button_frame: tkinter.Frame
            A basic container to separate the buttons from the checkboxes.
        filter_application_button: tkinter.Button
            The button used to apply all filters selected.
            If no filters are selected, the behavior is identical to all filters being selected.
        filter_clear_button: tkinter.Button
            The button used to clear all filters and reset the hero pool to its original form.
        
        Parameters
        ----------
        parent: Union['tk.Frame', 'tk.Canvas']
            The parent container or component the FilterPanel is attached to.
        filter_dict: Dict[str, List[str]]
            The data structure used to populate the text and values for the filters
            inside of the FilterPanel component.
        logic_layer: RandomHeroSelectManager
            The custom class that serves as the logic layer for randomly selecting heroes.
            It also contains all callback functions.

        Returns
        -------
        None.
    """

    def __init__(self, parent: Union['tk.Frame', 'tk.Canvas'], filter_dict: Dict[str, List[str]], logic_layer: RandomHeroSelectManager) -> None:
        self.filter_parent = tk.ttk.Labelframe(parent, text='Filters')
        self.filters = {}
        # Generate FilterGUIs for each filter specified
        for key, value in filter_dict.items():
            filter = FilterGUI(self.filter_parent, key, value)
            # Update the filters dictionary structure
            self.filters[key] = filter.checkboxes
        # Set up the button subcomponent
        self.filter_button_frame = tk.Frame(parent)
        self.filter_application_button = tk.Button(self.filter_button_frame, text='Apply Filters', width=10, height=1, fg='blue', command= lambda: logic_layer.callback_generate_masks(self.filters))
        self.filter_clear_button = tk.Button(self.filter_button_frame, text='Clear Filters', width=10, height=1, fg='blue', command= lambda: logic_layer.callback_clear_masks(self.filters))
        # Pack all components
        self.filter_application_button.pack(side='left')
        self.filter_clear_button.pack(side='right')
        self.filter_parent.pack(side='top', padx=(10, 10), pady=(10, 10))
        self.filter_button_frame.pack(side='bottom', padx=(10, 10), pady=(10, 10))

class MenuBar:
    """
        A secondary GUI component for the DotA2 Random Hero Selector.

        This GUI component serves as the menu bar for selecting new files to be used.
        It's primary usage is to switch between various preference lists freely, should
        the user wish to.

        Attributes
        ----------

        Parameters
        ----------

        Returns
        -------
        None.
    """

    def __init__(self, parent: 'tk.Tk', manager: RandomHeroSelectManager) -> None:

        self.menu_bar = tk.Menu(parent)
        self.manager = manager
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open New Preference File", command=self.open_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=parent.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

    def open_file(self):
        file_name = tk.filedialog.askopenfilename(initialdir=join(getcwd(), 'config/'), title='Select Preference List', filetypes=(("JSON files", "*.json"),("All Files","*.*")))
        try:
            self.manager.callback_open_new_preference_list(file_name)
        except JSONDecodeError as _json_error:
            error_message = f"An error occurred when attempting to use the selected file. Reverting to the default preference list.\nError Details:\n{_json_error}"
            tk.messagebox.showerror("File Error", error_message)

class RandomHeroSelectGUI:
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

        # Load in the random selection logic
        self.manager = RandomHeroSelectManager()
        # Create the root window
        self.root = tk.Tk()
        # Set the title
        self.root.title("DotA2 Random Hero Selector")
        # Set up the Menu Bar
        self.menu=MenuBar(self.root, self.manager)
        self.root.config(menu=self.menu.menu_bar)
        # Turn off resizing
        self.root.resizable(0,0)
        # Create the main canvas
        self.main_canvas = tk.Canvas(self.root)
        # Pack the main canvas
        self.main_canvas.pack()
        # Generate the hero portrait component and attach it
        self.hero_portrait_frame = tk.Frame(self.main_canvas)
        self.hero_portrait = HeroPortrait(self.hero_portrait_frame)
        # Pack the HeroPortrait component into the main canvas
        self.hero_portrait_frame.pack(side='left')
        # Create the Random button and attach the appropriate callback parameters from the HeroPortrait component
        self.random_button = tk.Button(self.hero_portrait_frame, text='Next Hero Please!', height=5, width=32, command = lambda: self.manager.callback_generate_random_hero(self.hero_portrait.photo_placeholder, self.hero_portrait.photo_label, self.hero_portrait.hero_text))
        # Make the button look raised
        self.random_button.config(relief=tk.RAISED)
        # Pack the button towards the bottom of the hero_portait frame (bottom-left) with padding.
        self.random_button.pack(side='bottom', padx=(10, 10), pady=(10, 10))
        self.filter_frame = FilterPanel(self.main_canvas, self.manager.gui_config, self.manager)
        # Run the root window GUI
        self.root.mainloop()


if __name__ == "__main__":
    r = RandomHeroSelectGUI()
