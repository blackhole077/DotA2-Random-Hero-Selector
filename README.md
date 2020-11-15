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

## Future Works and Directions

Currently (11/15/20) this project is only partially finished. With only the basic functionality in place, end-users are unable to do more than provide user-defined hero preference lists and select random heroes. Below are things that are slated as "future work".

### Adding ad-hoc filtering functionality

As of now, the callback functions are in place to filter the hero pool, but the GUI sub-components have not been created. Due to how Tkinter handles placing GUI components, having the panel match the intended design will take time.

### Unit Testing

As of now, the system works, but lacks any unit tests. Naturally, this results in abysmal coverage. Therefore, a future direction with this project is to understand the standard for testing GUI code, along with making sure that these tests adhere to the same standard as the main code.