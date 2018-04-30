'''
Created on 25 Jul 2017

@author: jdrumgoole
'''

from pymongo_import.version import __VERSION__

from setuptools import setup, find_packages
import os
import glob

pyfiles = [ f for f in os.listdir( "." ) if f.endswith( ".py" ) ]

    
setup(
    name = "pymongo_log",
    version =__VERSION__,
    
    author = "Joe Drumgoole",
    author_email = "joe@joedrumgoole.com",
    description = "A logging handler to write python logging output to MongoDB",
    long_description =
    '''
Write logging output to a MongoDB database (called AUDIT) via a custom logging handler.
''',

    license = "AGPL",
    keywords = "MongoDB python logging",
    url = "https://github.com/jdrumgoole/pymongo_log",
    
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',


        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Affero General Public License v3',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.6' ],
   
    install_requires = [  "pymongo",
                          "nose"],
       
    packages=find_packages(),

    test_suite='nose.collector',
    tests_require=['nose'],
)
