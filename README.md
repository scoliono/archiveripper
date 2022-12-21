# Archive.org Ripper

This script lets you download books page-by-page from [archive.org](https://archive.org) in the event that there is no PDF link. After the script has downloaded all the pages separately, it stitches the images to one pdf file. Any book with a <14 day loan period is like this, as you can see:

![](./archive.png)

## Credentials

The script needs your login credentials to borrow the book, then it will run on its own using your session. If you plan on using the script more than once, you can store your email and password in a config.py file (in the same directory) with the following structure:

```python
config = {
    'email': 'your email',
    'password': 'your password'
}
```

Do not use this program in an illegal manner. Thanks!

## Screenshots

![](./screenshot.png)
![](./explorer.png)

## Current bugs
- When downloading books with multiple hundreds of pages, after a while, the downloaded images are only 4Kb and are not the usual image format (UnidentifiedImageError). I have to write a function which detects this and start over from the first page where the download went wrong.

## Planned Features

- Searching for books instead of inputting id directly
- GUI
- Option to convert epub
