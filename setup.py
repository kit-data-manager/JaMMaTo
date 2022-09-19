from distutils.core import setup
setup(
  name = 'NEPMetadataMapping',         # How you named your package folder (MyLib)
  packages = ['NEPMetadataMapping'],   # Chose the same as "name"
  version = '2.0.2',      # Start with a small number and increase it with every change you make
  license='cc',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A library for mapping metadata attributes from file format schemas to a json schema document',   # Give a short description about your library
  author = 'Nicolas Blumenroehr',                   # Type in your name
  author_email = 'nicolas.blumenroehr@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/nicolasblumenroehr',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/nicolasblumenroehr/NEP-Metadata-Mapping-Tool/archive/refs/tags/2.0.2.tar.gz',    # I explain this later on
  keywords = ['Schema','Mapping','DICOM','JSON'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pydicom',
          'jsonschema'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: End Users/Desktop',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
