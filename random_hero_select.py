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

def open_file(filename, verbose=False):
    '''Attempts to open the file and parse it to convert <Hero_Name, Desire to Play> lines into
       hero name, weights respectively and append them to the appropriate lists.
    '''
    name_list = []
    weights = []
    if not os.path.exists(filename):
        print('Cannot find file {}. Check that you have it'.format(filename),
              'in the same directory as the .exe')
        sys.exit(0)
    with open(filename, 'r') as file:
        for line in file:
            name, weight = line.split(',')
            name_list.append(name)
            weights.append(weight)
    if verbose:
        print('Number of entries: {} entries'.format(len(name_list)))
        print('Number of entries (weights): {} entries'.format(len(weights)))
    return name_list, weights

def create_weighted_list(name_list, weight_list, verbose=False):
    '''Given a name list and its corresponding weight list, create
       a weighted name list which will be sampled with uniform randomness.
    '''
    weighted_name_list = []
    for i in range(len(name_list)):
        num_duplicate = int(weight_list[i])
        if num_duplicate > 1:
            weighted_name_list.extend([name_list[i] for j in range(num_duplicate)])
        else:
            continue
        if verbose:
            print('Number of times duplicated: {} times'.format(num_duplicate))
    return weighted_name_list

def main():
    '''The main function for rolling (and re-rolling) a random hero
       according to your weighted preferences.
    '''
    hero_name_list, weights_list = open_file("hero_list.txt", False)
    weighted_hero_list = create_weighted_list(hero_name_list, weights_list, False)
    print(np.random.choice(weighted_hero_list, 1))
    choice = input("Press Enter to re-roll or q to quit...")
    while choice != 'q':
        if not choice:
            print(np.random.choice(weighted_hero_list, 1))
        choice = input("Press Enter to re-roll or q to quit...")

main()
