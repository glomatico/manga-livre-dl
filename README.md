# Manga Livre DL
I don't really read manga, but a friend of mine asked me to create a script to download manga from https://mangalivre.net/. And so I did it.

## Setup
1. Install Python 3.7 or newer
2. Install manga-livre-dl with pip
    ```
    pip install manga-livre-dl
    ```

## Usage
```
usage: manga-livre-dl [-h] [-c CHAPTER_SELECTION [CHAPTER_SELECTION ...]] [-f FINAL_PATH] [-o] [-p] [-a] [-n] [-e] [-v]
                   url [url ...]

positional arguments:
  url                   mangalivre.net manga URL

options:
  -h, --help            show this help message and exit
  -c CHAPTER_SELECTION [CHAPTER_SELECTION ...], --chapter-selection CHAPTER_SELECTION [CHAPTER_SELECTION ...]
                        Chapter selection. Can be "all", "last" or a list of chapters (default: ['all'])
  -f FINAL_PATH, --final-path FINAL_PATH
                        Final path (default: Manga Livre DL)
  -o, --overwrite       Overwrite existing files (default: False)
  -p, --print-chapters  Print chapters and exit (default: False)
  -a, --ask-scan        Ask for scan selection (default: False)
  -n, --no-pdf          Don't make PDF and delete images (default: False)
  -e, --print-exceptions
                        Print exceptions (default: False)
  -v, --version         show program's version number and exit
```
