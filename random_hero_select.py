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
import numpy as np
from scipy.special import softmax
import pandas as pd
from json import load
from typing import List

def generate_probability_list(preference_list: List[int]) -> 'numpy.array':
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

    return softmax(preference_list)

def generate_hero_dataframe(preference_location: str, configuration_location:str) -> 'pandas.DataFrame':
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