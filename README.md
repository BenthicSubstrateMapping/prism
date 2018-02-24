
![prism_logo_blk_sm](https://user-images.githubusercontent.com/3596509/36518800-3d21b60e-1745-11e8-9a52-549b07dc9da1.png)

A Python framework for Probabilistic Acoustic Sediment Mapping. See project website [here](https://www.danielbuscombe.com/prism/) for more details


### Contributing & Credits
Software Developer: Dr. Daniel Buscombe, Northern Arizona University, Flagstaff, AZ 86011, daniel.buscombe@nau.edu

Example backscatter data (.tiff files) originate from data collected by R2Sonic and distributed for use as part of the R2Sonic 2017 Multispectral Backscatter competition.

Bed observation data from Patricia Bay are digitized from data presented in: B.~Biffard. Seabed remote sensing by single-beam echosounder: models, methods and applications. Doctoral dissertation, University of Victoria, Canada, 2011.

Bed observation data from Portsmouth (NEWBEX) are digitized from data presented in: T.~Weber, L.~and Ward. Observations of backscatter from sand and gravel seafloors between 170 and 250 kHz. Journal of the Acoustical Society of America, vol.~138, no.~4, pp.~2169 - 2180, 2015.

CRF subfunctions using the pydensecrf wrapper (https://github.com/lucasb-eyer/pydensecrf) 

## Setup

### Installing in a conda virtual env (recommended)

Windows:

```
conda create --name prism_test python=3
activate prism_test
pip install numpy Cython
pip install prism_mbes #(or pip install git+https://github.com/dbuscombe-usgs/prism.git)
```

Linux:

```
conda create --name prism_test python=3
source activate prism_test
pip install numpy Cython
pip install prism_mbes #(or pip install git+https://github.com/dbuscombe-usgs/prism.git)
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

4. linux users, using a virtual environment:

```
virtualenv venv
source venv/bin/activate
pip install numpy Cython
pip install prism_mbes  #(or pip install git+https://github.com/dbuscombe-usgs/prism.git)
deactivate ##(or source venv/bin/deactivate)
```


### Running the test

Then run the test ::

```
python -c "import prism; prism.test.dotest()" 
```

### Using the GUI

run the GUI ::

```
python -c "import prism; prism.gui_funcs.gui()" 
```

## Using prism within python scripts

A full worked example using the NEWBEX data set

```

def run_prism():

   #==================================================================================
   ##GMM parameters
   covariance = 'full'
   tol = 1e-2

   ##CRF parameters
   theta = 300 
   mu = 100 
   n_iter = 15

   # general settings
   gridres = 1  # grid size in m
   buff = 10 # buffer distance on each bed observation
   prob_thres = 0.1 #probability threshold
   chambolle = 0.0  #chambolle filter
   test_size = 0.5

   ## update this with the full file path
   bs100 = 'newbex_mosaic_100.tiff'
   bs200 = 'newbex_mosaic_200.tiff'
   bs400 = 'newbex_mosaic_400.tiff'
   refs_file = 'newbex_bed.shp'

   prefix = 'newbex'


   #======== READ
   #==================================================================================
   input = [bs100, bs200, bs400]
   img, bs = read_geotiff(input, gridres, chambolle)

   bed = read_shpfile(refs_file, bs)
   Lc = get_sparse_labels(bs, bed, buff)

   if np.ndim(img)>2:
      mask = img[:,:,0]==0
   else:
      mask = img==0

   #======== GMM
   #==================================================================================
   g = fit_GMM(img, Lc, test_size, covariance, tol)
   y_pred_gmm, y_prob_gmm, y_gmm_prob_per_class = apply_GMM(g, img, prob_thres)

   #======== CRF
   #==================================================================================
   y_pred_crf, y_prob_crf, y_crf_prob_per_class = apply_CRF(img, Lc, bed['labels'], n_iter, prob_thres, theta, mu)

   #======== PLOT
   #==================================================================================
   cmap = plt.get_cmap('tab20b',len(bed['labels'])-1).colors

   cmap1 = []
   cmap1.append('gray')
   for k in cmap:
      cmap1.append(colors.rgb2hex(k))

   plot_dists_per_sed(Lc, img, bed, cmap1, prefix)

   plot_gmm(mask, y_pred_gmm, y_prob_gmm, bs, bed, cmap, prefix)
   plot_crf(mask, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix)

   plot_gmm_image(mask, y_pred_gmm, y_prob_gmm, bs, bed, cmap, prefix)
   plot_crf_image(mask, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix)

   plot_gmm_crf(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix)
   plot_gmm_crf_images(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix)
   plot_bs_maps(img, bed, bs, cmap, prefix)

   plot_confmatCRF(y_pred_crf, Lc, bed, prefix)
   plot_confmatGMM(y_pred_gmm, Lc, bed, prefix)

   #======== EXPORT
   #==================================================================================
   export_bed_data(bed, prefix)
   export_gmm_gtiff(mask, y_pred_gmm.copy(), y_prob_gmm.copy(), bs, prefix)
   export_crf_gtiff(mask, y_pred_crf.copy(), y_prob_crf.copy(), bs, prefix)

if __name__ == '__main__':
   run_prism()

```



