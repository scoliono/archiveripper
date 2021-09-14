# Archive.org Ripper

This program lets you download books page-by-page from [archive.org](https://archive.org) in the event that there is no PDF link. Any book with a <14 day loan period is like this, as you can see:

![](./archive.png)

The program needs your login credentials to borrow the book, then it will run on its own using your session.

Do not use this program in an illegal manner. Thanks!

## Setup

Go to the Releases page if you want to download the GUI version, packaged into an executable. This is the most user-friendly option.

For a command-line interface, just clone this repo, create a virtual environment, run `pip install -r requirements.txt`, and then `python ripper.py` with optional arguments.

## Screenshots

![](./screenshot.png)
![](./explorer.png)

## Planned Features

- Searching for books instead of inputting id directly

- Option to convert to pdf or epub instead of saving each page individually
