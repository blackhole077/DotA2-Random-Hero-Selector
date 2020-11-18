# The Random Button With You in Mind
## Quick Start Information
### Required Packages and Libraries

The following libraries are necessary to ensure that the program runs properly.

- `Python3` (specifically `Python 3.5+` for type annotations)
- `scipy.special`
- `numpy`
- `pandas`
- `PIL (Python Imaging Library)`

Other libraries (e.g., `tkinter`) are assumed to be built-in libraries for Python.

> The reason for `Python 3.5+` is due to the use of type annotations, which is **not present in earlier versions**. If these type annotations are removed, then this project will likely work with `Python 3.3+`

It is strongly recommended that a **virtual environment** is used if you intend to develop this work further. Examples of Python virtual environments include **venv** and **Anaconda**.

### How to Run the Program

The program assumes that you're using `Python 3.5+`, which can be determined by either typing in `python --version` or `python3 --version`.

To run the program, simply navigate to the directory that houses this repository and type in the following command: `python random_hero_select_gui.py` or `python3 random_hero_select_gui.py`

## Introduction

Do you ever feel nostalgic for the halcyon days of selecting random heroes in DotA 2? Ever feel annoyed about only being able to random on your first two picks, or possibly picking a hero you really didn't want? Then this GUI is a great fit for you!

Small, lightweight, and easy to use, this tool gives you a risk-free place to satisfy your cravings! You can even set up a personalized "random pool" to make sure you never, ever roll certain heroes!

This implementation includes dynamic filtering! Ranging from primary attributes to types of crowd control, these robust filters make sure your random pick is the best fit for the team.

## Purpose and Motivation

This project was initially designed due to the personal annoyance I felt when friends of mine consistently pressed the random button when selecting heroes. This usually resulted in arguments about bad drafting, sparking the (wildly uncreative) idea of having a tool that mimicked the process for you.

Initially, this was a command-line tool, but this was not accessible to users who weren't already familiar with such tools. Consequently, the simplicity of the underlying logic lent itself well as a project to learn Tkinter with.

## What the Expectations Were


To give an idea of why certain design decisions were made, it helps to have an understanding of what this project was **expected to do**. As such, below is an bulleted list of those expectations.

- Update the original implementation to be more robust and customizable by an end user
- Create a user-friendly GUI that contains the program's functionality
- Add ad hoc filtering based on different aspects of a given hero
- Add hero portraits to provide glance value to the program, along with code to fetch images online if needed

For personal expectations regarding this project, I include the following expectations as well.

- Codebase should be well-documented with proper doc-strings and in-line comments wherever applicable
- Codebase should make use of type hinting/type annotation wherever applicable
- Codebase should be designed in such a way that individual portions of code are not highly coupled

Overall, the personal goal for this project was to **demonstrate good coding practices in a simple project**.

## What This Project Achieved
This project demonstrates **basic Tkinter knowledge**, along with using **Boolean masking on Pandas DataFrames** for filtering.
Additionally, this project can be used locally and is very lightweight for its purpose. Though an internet connection is required to download
hero portraits initially, after all portraits are downloaded it can be used completely offline.

Finally, this project serves to **demonstrate the developer's knowledge in standard Python practices**, including proper documentation, docstring usage, and type annotation.

## Future Works and Directions

Currently the project contains all basic functionality, including ad hoc filtering. However, there are additional features that could be introduced should there be additional demand for it.

### Hiding the filter panel

As of right now, the filter panel is somewhat unwieldy, consuming more than 2/3 of the available GUI space. As such, a feature that could be implemented is some sort of button or command that effectively "hides" the panel at the end-user's discretion.

### A file menu for selecting new hero preference lists

While there is a default hero list that can be modified directly for adjusting preference values, completely new lists of heroes cannot be hot-swapped easily, requiring the end-user to instead dive into the source code itself to make such changes. Therefore, adding a menu bar with some window dialog would alleviate this situation.

### Unit Testing

As of now, the system works, but lacks any unit tests. Naturally, this results in abysmal coverage. Therefore, a future direction with this project is to understand the standard for testing GUI code, along with making sure that these tests adhere to the same standard as the main code.
