Run `pyside6-uic $FILENAME.ui > ../archiveripper/ui/ui_$FILENAME.py` every time you change one of the UI files.

At least from my experience on Windows, the resulting .py files may be encoded as little-endian UTF-16 for some dumb reason. If you receive the error

```
ValueError: source code string cannot contain null bytes
```

then you just need to change the encoding to UTF-8.
