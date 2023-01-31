import setuptools
import manga_livre_dl

version = manga_livre_dl.__version__

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name = 'manga-livre-dl',
    version = version,
    description = 'Download manga from mangalivre.net',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/glomatico/manga-livre-dl',
    packages = setuptools.find_packages(),
    author = 'glomatico',
    install_requires = ['imgdl'],
    entry_points = {'console_scripts': ['manga-livre-dl = manga_livre_dl:main']}
)
