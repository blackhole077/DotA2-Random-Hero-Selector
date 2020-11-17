"""
    What Hero Do I Want? A Random-Button Killer
    Written by Jeevan Rajagopal
    01/13/20
    Purpose: Given a list of DotA 2 Heroes and
    how willing the user is to play said hero
    on a numeric scale from 0 to n, randomly
    select from a weighted distribution of
    heroes. This allows the user to have the
    fun of random selection, without making
    their allies suffer the consequences.
"""

import os
import sys
from io import BytesIO
from json import load
from typing import List, Optional, Union, Dict

import numpy as np
import pandas as pd
import requests
from PIL import Image, ImageTk
from scipy.special import softmax


class RandomHeroSelectManager:
    """
        Construct a logic layer that handles callback functions
        and user-defined information.

        This class is used to convert user-defined data into
        Pandas DataFrames, which are then used for rolling
        random heroes that fit user-defined filters and parameters.
        
        Attributes
        ----------
        available_images: List[str]
            A list of file paths corresponding to hero portraits.
        hero_dataframe: pandas.DataFrame
            The data structure used to hold the hero information,
            along with filter-specific information.
        mask: numpy.array
            A boolean array that masks out certain heroes in the
            hero_dataframe data structure. Multiple filters and
            masks are combined by LOGCIAL AND into a single mask.
        filtered_dataframe: pandas.DataFrame
            A DataFrame that represents a filtered subsection of
            the main hero_dataframe. This is equivalent to the
            main DataFrame if no masks are present.
        hero_probabilities: numpy.array
            A 1D Numpy array that represents the likelihood of
            a given hero being selected. Due to the use of the
            Softmax function, all probabilities will sum to 1.

        Parameters
        ----------
        preference_location: Optional[str]
            The file path location of the JSON file to use
            for hero preferences. The values are scaled from
            0 to 4, with higher numbers indicating a higher
            desire to play.
        configuration_location: Optional[str]
            The file path location of the JSON file that
            contains the filter-specific information, along
            with other static pieces of information.
    """

    def __init__(self, preference_location:Optional[str]="config/default_hero_list.json", configuration_location:Optional[str]="config/hero_configuration.json"):
        self.available_images = [f for f in os.listdir('images/') if os.path.isfile(os.path.join('images/', f))]
        with open("config/gui_filter_configuration.json", 'r') as _file:
            self.gui_config = load(_file)
        self.hero_dataframe:'pandas.DataFrame' = self.generate_hero_dataframe(preference_location, configuration_location)
        self.mask = None
        # Set the filtered to be equal to the original
        self.filtered_dataframe = self.hero_dataframe
        self.hero_probabilities = None

    def generate_mask(self, column_to_check:str, desired_values:Union[List[str],List[int]]):
        """
            Generate a filter to apply.

            Generates a boolean array that checks, for a given column, if the value
            contained in said column is present in the list of desired values.

            NOTE: The shape of the mask should be equal to the number of heroes
            present in the data structure. Basically masks.shape = (num_heroes, )

            Parameters
            ----------
            column_to_check: str
                The name of the column to use for reference
            desired_values: Union[List[str], List[int]]
                A list containing either string values or integer 
                values that represent a 'whitelist' of accepted values
                for the mask.

            Returns
            -------
            masks: numpy.array
                A boolean array that masks out certain heroes in the
                hero_dataframe data structure. Multiple filters and
                masks are combined by LOGCIAL AND into a single mask.
        """

        if isinstance(self.hero_dataframe[column_to_check].values[0], list):
            boolean_values = []
            for values in self.hero_dataframe[column_to_check].values:
                boolean_values.append(np.any(np.isin(values, desired_values)))
            return np.array(boolean_values)
        else:
            return np.in1d(self.hero_dataframe[column_to_check].values, desired_values)
    
    def generate_combined_mask(self, mask_1, mask_2):
        """
            Generates a combination of multiple masks.

            Given two boolean masks, this function
            applies a LOGICAL AND to combine them into
            one mask.

            NOTE: The shape of the mask should be equal to the number of heroes
            present in the data structure. Basically masks.shape = (num_heroes, )

            Parameters
            ----------
            mask_1: numpy.array
                A boolean array that masks out certain heroes in the
                hero_dataframe data structure. Multiple filters and
                masks are combined by LOGICAL AND into a single mask.
            mask_2: numpy.array
                A boolean array that masks out certain heroes in the
                hero_dataframe data structure. Multiple filters and
                masks are combined by LOGICAL AND into a single mask.

            Returns
            -------
            combined_mask: numpy.array
                A boolean array that masks out certain heroes in the
                hero_dataframe data structure. Multiple filters and
                masks are combined by LOGICAL AND into a single mask.
        """

        # If both masks are None values, then return None
        if mask_1 is None and mask_2 is None:
            return None
        # If the first mask is not initialized but the second is, return the second mask
        if mask_1 is None and not mask_2 is None:
            return mask_2
        # If the first mask is initialized but the second isn't, return the first mask
        if not mask_1 is None and mask_2 is None:
            return mask_1
        # If both masks are present, then combine them with LOGICAL AND
        return mask_1 & mask_2
    
    def callback_generate_masks(self, checkbox_dict: Dict[str, 'random_hero_select_gui.Checkbar']):
        """
            A callback function to filter the heroes based on the values in all filters.

            This function creates and applies multiple filters that results in a
            subset of heroes whose primary attribute matches the desired values.

            Parameters
            ----------
            checkbox_dict: Dict[str, `random_hero_select_gui.Checkbar`]
                A dictionary structure that contains the name of the filter
                as the key, and any selected values for the filter as the value.
                If no values are selected for a particular filter, the default
                behavior is that all values are treated as being selected.

            Returns
            -------
            None.
        """

        self.filtered_dataframe = self.reset_filtered_hero_dataframe()
        for key, value in checkbox_dict.items():
            checkbox_values = value.fetch_selected_labels()
            # If no values are selected, behavior should be equivalent to all values being selected.
            if not checkbox_values:
                checkbox_values = value.labels
            # Generate a mask and combine it with the existing mask (if one is present)
            self.mask = self.generate_combined_mask(self.mask, self.generate_mask(key, checkbox_values))
        # If all values in the mask are False, then reset the entire thing.
        if not any(self.mask):
            # TODO: Add something to tell the user their current filters don't work.
            self.reset_filtered_hero_dataframe()
            self.callback_clear_masks(checkbox_dict)
            return
        # Generate the filtered dataframe if everything looks good
        self.generate_filtered_hero_dataframe()

    def callback_clear_masks(self, checkbox_dict):
        """
            Clear out all selected filter values.

            This function resets all checkboxes in all filters and resets the hero pool.

            Parameters
            ----------
            checkbox_dict: Dict[str, `random_hero_select_gui.Checkbar`]
                A dictionary structure that contains the name of the filter
                as the key, and any selected values for the filter as the value.
                If no values are selected for a particular filter, the default
                behavior is that all values are treated as being selected.
            
            Returns
            -------
            None.
        """

        for checkboxes in checkbox_dict.values():
            checkboxes.clear()
        self.reset_filtered_hero_dataframe()

    def generate_filtered_hero_dataframe(self):
        """
            Apply existing filters to create the filtered DataFrame and create the probabilities.

            This function applies any existing masks onto the main DataFrame,
            after which the new probabilities are generated.

            Parameters
            ----------
            None.

            Returns
            -------
            None.
        """

        self.filtered_dataframe = self.hero_dataframe[self.mask]
        self.hero_probabilities = self.generate_probability_list()
    
    def reset_filtered_hero_dataframe(self):
        """
            Clear existing filters to reset the filtered DataFrame and create the probabilities.

            This function removes any existing masks onto the main DataFrame,
            after which the new probabilities are generated.

            Parameters
            ----------
            None.

            Returns
            -------
            None.
        """

        self.mask = None
        self.filtered_dataframe = self.hero_dataframe
        self.hero_probabilities = self.generate_probability_list()

    def callback_generate_random_hero(self, photo_placeholder:'tkinter.Label', photo_label:'tkinter.Label', hero_text:'tkinter.StringVar') -> None:
        """
            A callback function to randomly select a hero and display the corresponding image.

            This function selects a random hero from the filtered list of available heroes,
            searches for the corresponding image and then displays the image in the HeroPortrait.

            Parameters
            ----------
            photo_placeholder: tkinter.Label
                A label that serves to house the image.
                NOTE: Originally a Canvas was used for this purpose,
                but ultimately Label proved more understandable for this project.
            photo_label: tkinter.Label
                A label that houses the name of the hero the image belongs to.
            hero_text: tkinter.StringVar
                A variable that holds the actual mutable text data corresponding
                to the randomly selected hero.

            Returns
            -------
            None.
        """
        
        random_hero = self.filtered_dataframe.sample(weights=self.hero_probabilities).index.values[0]
        cleaned_hero_text = random_hero.replace('_', ' ').title()
        img = self.fetch_image(f"{self.hero_dataframe.loc[random_hero, 'image_prefix']}_vert.jpg")
        photo_placeholder.configure(image=img)
        photo_placeholder.image = img
        hero_text.set(cleaned_hero_text)
        photo_label.update()
        
    def fetch_image(self, image_stub: str) -> 'ImageTk.PhotoImage':
        """
            Fetch the image corresponding to the randomly selected hero.

            This function attempts to retrieve a hero portrait locally.
            If the image is not available locally, it is fetched from the
            DotA2 website directly and saved in the local `images` folder.

            Parameters
            ----------
            image_stub: str
                A string that uniquely identifies the hero that was selected.
                It is also used in the URL, if the local file is not present.
            
            Returns
            -------
            hero_portrait: ImageTk.PhotoImage
                The image that is currently displayed. A default image is loaded
                upon initialization.
        """

        # If the image already exists locally, use it instead
        if image_stub in self.available_images:
            image = Image.open(os.path.join('images/', image_stub))
        else:
            # Fetch the image from the DotA2 CDN
            url = f"http://cdn.dota2.com/apps/dota2/images/heroes/{image_stub}"
            response = requests.get(url)
            # If the response is no good, then display the default image.
            if not response.ok:
                image = Image.open('images/default_vert.jpg')
            else:
                # Write the image to a file (maintaining the naming scheme)
                with open(os.path.join('images/', image_stub), 'wb') as _file:
                    _file.write(response.content)
                # Read the bytes as an image
                image = Image.open(BytesIO(response.content))
        # Open the image and resize it to the default size (width: 235px, height: 272px) as some images are larger.
        return ImageTk.PhotoImage(image.resize(size=(235, 272)))

    def generate_probability_list(self) -> 'numpy.array':
        """
            Generate a weighted list based on preferences.

            Generates a probability distribution based on
            the softmax function to transform discrete values
            into a probability distribution that sums to 1.0

            Parameters
            ----------
            preference_list: List[int]
                A list of preference values ranging from 1 to 4.
                This list must match the number of desired heroes.
            
            Returns
            -------
            weighted_probabilities: np.array(float)
                A list of real-value probabilities generated via
                the softmax function. All values will sum to 1.
        """

        preference_list = self.filtered_dataframe['preference'].values
        return softmax(preference_list)

    def generate_hero_dataframe(self, preference_location: str, configuration_location:str) -> 'pandas.DataFrame':
        """
            Generate a dataframe that contains all user-specified data.

            Using the user-defined preference JSON file and the configuration
            file that contains semi-static information regarding each hero,
            generate a Dataframe to use while the program is active.

            NOTE: Since Pandas is prone to memory leakage, try not to call
            this function multiple times. If anything, it should only be
            used once total.

            Parameters
            ----------
            preference_location: str
                The name of the JSON file that contains the preferences for
                each hero in DotA 2.
            configuration_location: str
                The name of the JSON file that contains the basic information
                about each hero in DotA 2, such as primary attribute and attack type.

            Returns
            -------
            hero_dataframe: pandas.DataFrame
                A DataFrame object that contains all information in both files.
        """
        
        hero_dict = {}
        with open(configuration_location, 'r') as _config_file:
            hero_dict = load(_config_file)
        pref_dict = {}
        with open(preference_location, 'r') as _preference_file:
            pref_dict = load(_preference_file)
        # Manually update one dictionary with values from the other to prevent overwriting
        for key in hero_dict.keys():
            hero_dict[key].update(pref_dict.get(key))
        # Clean out the preference dictionary
        pref_dict.clear()
        return pd.DataFrame.from_dict(hero_dict, orient='index')