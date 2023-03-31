from distutils.core import setup
setup(
  name = 'jammato',         # How you named your package folder (MyLib)
  packages = ['jammato'],   # Chose the same as "name"
  version = '1.0',      # Start with a small number and increase it with every change you make
  license='cc',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A package for mapping metadata attributes from proprietary file format schemas to a json schema document.',   # Give a short description about your library
  author = 'Nicolas Blumenroehr',                   # Type in your name
  author_email = 'nicolas.blumenroehr@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/user/nicolasblumenroehr',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/kit-data-manager/JaMMaTo/archive/refs/tags/3.0.3.tar.gz',    # I explain this later on
  keywords = ['Schema', 'Mapping', 'DICOM', 'JSON'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
        'pydicom',
        'pydicom',
        'jsonschema',
        'urllib3',
        'datetime',
        'typing',
        'zipfile'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.10'
  ],
)
