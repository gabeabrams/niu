from distutils.core import setup

setup(
  name = 'niu',
  packages = ['niu'],
  version = '0.2',
  description = 'A grouping and pairing library',
  author = 'Gabriel Abrams',
  author_email = 'gabeabrams@gmail.com',
  url = 'https://github.com/gabeabrams/niu',
  download_url = 'https://github.com/gabeabrams/niu/archive/0.1.tar.gz',
  keywords = ['grouping', 'pairing', 'matching'],
  install_requires=[
    'pulp'
  ],
  classifiers = []
)