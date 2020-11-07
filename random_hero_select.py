'''
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
'''
import os
import sys
from io import BytesIO
from json import load
from typing import List, Optional, Union

import numpy as np
import pandas as pd
import requests
from PIL import Image, ImageTk
from scipy.special import softmax


class RandomHeroSelectManager():
    def __init__(self, preference_location:Optional[str]="config/default_hero_list.json", configuration_location:Optional[str]="config/hero_configuration.json"):
        self.available_images = [f for f in os.listdir('images/') if os.path.isfile(os.path.join('images/', f))]
        self.hero_dataframe = self.generate_hero_dataframe(preference_location, configuration_location)
        self.mask = None
        # Set the filtered to be equal to the original
        self.filtered_dataframe = self.hero_dataframe
        self.hero_probabilities = None

    def generate_mask(self, column_to_check:str, desired_values:Union[List[str],List[int]]):
        return np.in1d(hero_dataframe[column_to_check].values, desired_values)
    
    def generate_combined_mask(self, mask_1, mask_2):
        return mask_1 & mask_2
    
    def callback_primary_stat_mask(self, values):
        self.mask = self.generate_combined_mask(self.mask, self.generate_mask('primary_stat', values)) 
        self.generate_filtered_hero_dataframe()

    def callback_position_mask(self, values):
        self.mask = self.generate_combined_mask(self.mask, self.generate_mask('position', values)) 
        self.generate_filtered_hero_dataframe()

    def callback_attack_type_mask(self, values):
        self.mask = self.generate_combined_mask(self.mask, self.generate_mask('attack_type', values)) 
        self.generate_filtered_hero_dataframe()

    def callback_crowd_control_mask(self, values):
        self.mask = self.generate_combined_mask(self.mask, self.generate_mask('crowd_control_tags', values))
        self.generate_filtered_hero_dataframe()

    def generate_filtered_hero_dataframe(self):
        self.filtered_dataframe = self.hero_dataframe[self.mask]
        self.hero_probabilities = self.generate_probability_list()
    
    def callback_generate_random_hero(self, photo_placeholder:'tkinter.Label', photo_label, hero_text):
        random_hero = self.filtered_dataframe.sample(weights=self.hero_probabilities).index.values[0]
        cleaned_hero_text = random_hero.replace('_', ' ').title()
        img = self.fetch_image(f"{self.hero_dataframe.loc[random_hero, 'image_prefix']}_vert.jpg")
        photo_placeholder.configure(image=img)
        photo_placeholder.image = img
        hero_text.set(cleaned_hero_text)
        photo_label.update()
        
    def fetch_image(self, image_stub: str):
        if image_stub in self.available_images:
            return ImageTk.PhotoImage(Image.open(os.path.join('images/', image_stub)))
        else:
            url = f"http://cdn.dota2.com/apps/dota2/images/heroes/{image_stub}"
            response = requests.get(url)
            if not response.ok:
                return ImageTk.PhotoImage(Image.open('images/default_vert.jpg'))
            with open(os.path.join('images/', image_stub), 'wb') as _file:
                _file.write(response.content)
            return ImageTk.PhotoImage(Image.open(BytesIO(response.content)))


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

def main():
    '''The main function for rolling (and re-rolling) a random hero
       according to your weighted preferences.
    '''
    hero_dataframe = generate_hero_dataframe('config/default_hero_list.json', 'config/hero_configuration.json')
    print(hero_dataframe)
    mask = np.in1d(hero_dataframe['primary_stat'].values, ['strength', 'intelligence'])
    mask_2 = hero_dataframe['attack_type'] == 'ranged'
    mask_comp = mask & mask_2
    df_slice = hero_dataframe[mask_comp]
    print(df_slice)
    weighted_probabilities = generate_probability_list(df_slice['preference'].values)
    for _ in range(5):
        print(df_slice.sample(weights=weighted_probabilities).index.values)
    # TODO: Write call for converting JSON files into DataFrame
    # TODO: Test that weighted random via softmax works as intended
    # TODO: Write this main function as a callback on start for tkinter
    pass

if __name__ == "__main__":
    main()
