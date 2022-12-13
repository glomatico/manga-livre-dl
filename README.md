# manga-livre-downloader
I don't really read manga, but a friend of mine asked me to create a script to download manga from https://mangalivre.net/. And so I did it.

## Setup
1. Install Python 3.8 or higher
2. Install imgdl with pip: 
    ```
    pip install imgdl
    ```

## Usage
```
python manga_livre_downloader.py [URLS] [OPTIONS]
```
The manga will be saved in `./Manga Livre Downloader` as .PDF by default, but the directory can be changed using `--final-path` argument.

You can specify which chapters to download using the `--chapter-selection` argument. It downloads all chapters by default.

Use `--help` argument to see all available options.
