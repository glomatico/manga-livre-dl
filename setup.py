from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name = 'manga-livre-dl',
    version = '1.1',
    description = 'Download manga from mangalivre.net',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/glomatico/manga-livre-dl',
    packages = find_packages(),
    author = 'glomatico',
    install_requires = ['imgdl'],
    entry_points = {'console_scripts': ['manga-livre-dl = manga_livre_dl:main']}
)
