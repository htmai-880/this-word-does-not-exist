
from setuptools import setup 
  
setup( 
    name='title_maker_pro', 
    version='0.1', 
    description='This word does not exist, word or definition generator.', 
    packages=['title_maker_pro'], 
    install_requires=[ 
        'transformers',
        'stanza'
    ], 
) 