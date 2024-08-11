# SHTMLDG
Simple HTML Documentation Generator which uses XML files as an input.

## Prerequisites
* Python 3;
* Python 3 `yattag` library.
  * On **Ubuntu** and its derivatives you can use `sudo apt install python3-yattag` to install it, and it might be similar for other Unix-like systems.
  * On **Windows** you can use `python3 -m pip install yattag` to install it.

## Command-line usage
You need to specify source and destination for documentation generator.

Example:
```
./program.py ../src ../site
```

This will use XML files in `../src` directory, and generate HTML documentation in `../site` directory.

## XML file format
**TODO:** This section.

## Examples
You can use the example documentation XML files to generate an example documentation website.
You can run this by executing either:
* On **Unix:** `./make_example_docs.Unix.sh`;
* On **Windows:** `.\make_example_docs.Windows.bat`.
