This folder contains Qt .ui files which need to be recompiled into Python files whenever they are changed.

Hopefully, your editor has a way to automate this for you. In VS Code, for example, all you have to do is download the Qt for Python extension and add the following setting:

```json
"qtForPython.uic.args": [
    "-o \"${workspaceFolder}${pathSeparator}archiveripper${pathSeparator}ui${pathSeparator}ui_${fileBasenameNoExtension}.py\""
]
```

If you need to do it by hand, though, you just need to run this command for each file you change:

```sh
pyside6-uic $FILENAME.ui > ../archiveripper/ui/ui_$FILENAME.py
```

And if you receive the error

```
ValueError: source code string cannot contain null bytes
```

trying to import the compiled .py scripts, this is just because they were encoded as little-endian UTF-16 for some stupid reason. You just need to change them to UTF-8.
