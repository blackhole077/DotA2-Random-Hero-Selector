# The Random Button With You in Mind

## What This Project Achieved
This project demonstrates **basic Tkinter knowledge**, along with using **Boolean masking on Pandas DataFrames** for filtering.
Additionally, this project can be used locally and is very lightweight for its purpose. Though an internet connection is required to download
hero portraits initially, after all portraits are downloaded it can be used completely offline.

Finally, this project serves to **demonstrate the developer's knowledge in standard Python practices**, including proper documentation, docstring usage, and type annotation.

## Introduction

Do you ever feel nostalgic for the halcyon days of selecting random heroes in DotA 2? Ever feel annoyed about only being able to random on your first two picks, or possibly picking a hero you really didn't want? Then this GUI is a great fit for you!

Small, lightweight, and easy to use, this tool gives you a risk-free place to satisfy your cravings! You can even set up a personalized "random pool" to make sure you never, ever roll certain heroes!

Future features will include ad-hoc filtering! With filters ranging from primary attributes to types of crowd control, these robust filters make sure your random pick is the best fit for the team.

## Purpose and Motivation

This project was initially designed due to a personal annoyance I, the developer, felt when friends of mine constantly pressed the random button when selecting heroes. This usually resulted in arguments about bad drafting, sparking the (wildly uncreative) idea of having a tool that mimicked the process for you.

Initially, the project was a simple command-line tool, but this made the tool feel somewhat limited. Consequently, the simplicity of the underlying logic lent itself well as a project to learn Tkinter with.

## What the Expectations Were

To give an idea of why certain design decisions were made (good or bad), it helps to have an understanding of what this project was **expected to do**. As such, below is an bulleted list of those expectations.

- Update the original implementation to be more robust and customizable by an end user
- Create a user-friendly GUI that contains the intended functionality
- Add ad-hoc filtering based on different aspects of a given hero
- Add hero portraits to provide glance value to the overall program, along with code to fetch images if not available locally

For personal expectations regarding this project, I include the following expectations as well.

- Codebase should be well-documented with proper doc-strings and in-line comments wherever applicable
- Codebase should make use of type hinting/type annotation wherever applicable
- Codebase should be designed in such a way that individual portions of code are not highly coupled

Overall, the personal goals for this project was to **demonstrate good coding practices in a simple project**.

## Required Packages and Libraries

The following libraries are necessary to ensure that the program runs properly.

- `Python3` (specifically `Python 3.5+`)
- `scipy.special`
- `numpy`
- `pandas`
- `PIL (Python Imaging Library)`

Other libraries (e.g., `tkinter`) are assumed to be builtin libraries for Python.

It is strongly recommended that a **virtual environment** is used if you intend to develop this work further. Examples of Python virtual environments include **venv** and **Anaconda**.

## How to Run the Program

The program assumes that you're using `Python 3.5+`, which can be determined by either typing in `python --version` or `python3 --version`.

To run the program, simply navigate to the directory that houses this repository and type in the following command: `python random_hero_select_gui.py` or `python3 random_hero_select_gui.py`

## Future Works and Directions

Currently the project contains all basic functionality, including ad-hoc filtering. However, there are additional features that could be introduced should there be additional demand for it.

### Hiding the filter panel

As of right now, the filter panel is somewhat unwieldy, consuming more than 2/3 the available GUI space. As such, a feature that could be implemented is some sort of button or command that
effectively "hides" the panel at the end-users' discretion.

### A file menu for selecting new hero preference lists

While there is a default hero list that can be modified directly for adjusting preference values, completely new lists of heroes cannot be hot-swapped easily, requiring the end-user to instead dive into the source code itself to make such changes. Therefore, adding a menu bar with some window dialog would alleviate this situation.

### Unit Testing

As of now, the system works, but lacks any unit tests. Naturally, this results in abysmal coverage. Therefore, a future direction with this project is to understand the standard for testing GUI code, along with making sure that these tests adhere to the same standard as the main code.
