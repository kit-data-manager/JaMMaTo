from distutils.core import setup
setup(
  name = 'JAMMATO',         
  packages = ['jammato'],   
  version = '1.1',      
  license='cc',        
  description = 'A package for mapping metadata attributes from proprietary file format schemas to a json schema document.',   
  author = 'Nicolas Blumenroehr',                   
  author_email = 'nicolas.blumenroehr@gmail.com',      
  url = 'https://github.com/user/nicolasblumenroehr',  
  download_url = 'https://github.com/kit-data-manager/JaMMaTo/archive/refs/tags/3.0.3.tar.gz',   
  keywords = ['Schema', 'Mapping', 'DICOM', 'JSON'],   
  install_requires=[            
        'pydicom',
        'jsonschema',
        'urllib3',
        'datetime',
        'typing',
        'zipfile'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',    
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3.10'
  ],
)
