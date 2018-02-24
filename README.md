
![prism_logo_blk_sm](https://user-images.githubusercontent.com/3596509/36518800-3d21b60e-1745-11e8-9a52-549b07dc9da1.png)

A Python framework for Probabilistic Acoustic Sediment Mapping. See project website [here](https://www.danielbuscombe.com/prism/) for more details


### Contributing & Credits
Software Developer: Dr. Daniel Buscombe, Northern Arizona University, Flagstaff, AZ 86011, daniel.buscombe@nau.edu

Example backscatter data (.tiff files) originate from data collected by R2Sonic and distributed for use as part of the R2Sonic 2017 Multispectral Backscatter competition.

Bed observation data from Patricia Bay are digitized from data presented in: B.~Biffard. Seabed remote sensing by single-beam echosounder: models, methods and applications. Doctoral dissertation, University of Victoria, Canada, 2011.

Bed observation data from Portsmouth (NEWBEX) are digitized from data presented in: T.~Weber, L.~and Ward. Observations of backscatter from sand and gravel seafloors between 170 and 250 kHz. Journal of the Acoustical Society of America, vol.~138, no.~4, pp.~2169 - 2180, 2015.

## Setup

### Installing in a conda virtual env (recommended)

Windows:

```
conda create --name prism_test python=3
activate prism_test
pip install prism_mbes #(or pip install git+https://github.com/dbuscombe-usgs/prism.git)
```

Linux:

```
conda create --name prism_test python=3
source activate prism_test
```

Then run the test ::

```
python -c "import prism; prism.test.dotest()" 
```

run the GUI ::


```
python -c "import prism; prism.gui_funcs.gui()" 
```

finally deactivate the venv ::

```
deactivate
```

Linux:

```
source deactivate
```

If you get gdal/osgeo/ogr/os errors, install GDAL (Windows only)::
1. Go to: https://www.lfd.uci.edu/~gohlke/pythonlibs/#gdal
2. Download the appropriate file (for example, python 3.6, 64 bit = GDAL‑2.2.3‑cp36‑cp36m‑win32.whl )
3. install using pip:

```
pip install GDAL‑2.2.3‑cp36‑cp36m‑win32.whl
```

### Installing as a library accessible outside of virtual env


1. From PyPI::

```
pip install prism_mbes
```

2. the latest 'bleeding edge' (pre-release) version directly from github::

```
pip install git+https://github.com/dbuscombe-usgs/prism.git
```

(Windows users) install git from here: https://git-scm.com/download/win


3. from github repo clone::

```
git clone git@github.com:dbuscombe-usgs/prism.git
cd prism
python setup.py install
```

or a local installation:

```
python setup.py install --user
```



