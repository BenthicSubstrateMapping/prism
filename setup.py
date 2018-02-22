#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# Imports
#-----------------------------------------------------------------------------

import os, sys, glob
import inspect

from distutils.core import setup
from distutils.extension import Extension

# Directory of the current file 
SETUP_DIRECTORY = os.path.dirname(os.path.abspath(inspect.getfile(
    inspect.currentframe())))

# Read version from distmesh/__init__.py
with open(os.path.join('prism', '__init__.py')) as f:
    line = f.readline()
    while not line.startswith('__version__'):
        line = f.readline()
exec(line, globals())


install_requires = [
    'numpy','scipy','Pillow','matplotlib', 'cython', 'pyproj', 'scikit-image', 'pydensecrf', 'basemap', 'scikit-learn', 'tkcolorpicker', 'fiona', 'rasterio', 'shapely', 'GDAL'
]

def setupPackage():
   setup(name='prism_mbes',
         version=__version__,
         description='Buscombe, D., 2017',
         #long_description=long_description,
         classifiers=[
             'Intended Audience :: Science/Research',
             'Intended Audience :: Developers',
             'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
             'Programming Language :: Python',
             'Topic :: Scientific/Engineering',
             'Topic :: Scientific/Engineering :: Physics',
         ],
         keywords='sonar sediment substrate classification',
         author='Daniel Buscombe',
         author_email='daniel.buscombe@nau.edu',
         url='https://github.com/dbuscombe-usgs/prism',
         download_url ='https://github.com/dbuscombe-usgs/prism/archive/master.zip',
         install_requires=install_requires,
         license = "GNU GENERAL PUBLIC LICENSE v3",
         packages=['prism'],
         platforms='OS Independent'
   )

if __name__ == '__main__':
    # clean --all does not remove extensions automatically
    if 'clean' in sys.argv and '--all' in sys.argv:
        import shutil
        # delete complete build directory
        path = os.path.join(SETUP_DIRECTORY, 'build')
        try:
            shutil.rmtree(path)
        except:
            pass
        # delete all shared libs from lib directory
        path = os.path.join(SETUP_DIRECTORY, 'prism')
        for filename in glob.glob(path + os.sep + '*.pyd'):
            try:
                os.remove(filename)
            except:
                pass
        for filename in glob.glob(path + os.sep + '*.so'):
            try:
                os.remove(filename)
            except:
                pass
    setupPackage()

