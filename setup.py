from setuptools import setup, find_packages


with open('readme.md','r')as f:
    long_description = f.read()

setup(
    name='YTScraper',
    author='Fawad Abbas',
    author_email='fawad.abbas04@gmail.com',
    version='0.1.0',
    description='A simple wrapper for creating datasets from youtube',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/FawadAbbas12/YTScraper',
    license='unlicense',
    # package_dir={'':"YTScraper"},
    # packages=find_packages(where='YTScraper'),
    # install_requires=[
    #     'ediblepickle==1.1.3',
    #     'pytube==12.1.2',
    #     'tqdm==4.65.0'
    # ]
)
