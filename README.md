
![prism_logo_blk_sm](https://user-images.githubusercontent.com/3596509/36518800-3d21b60e-1745-11e8-9a52-549b07dc9da1.png)

A Python framework for Probabilistic Acoustic Sediment Mapping. See project website [here](https://www.danielbuscombe.com/prism/) for more details


### Contributing & Credits
Software Developer: Dr. Daniel Buscombe, Northern Arizona University, Flagstaff, AZ 86011, daniel.buscombe@nau.edu

Example backscatter data (.tiff files) originate from data collected by R2Sonic and distributed for use as part of the R2Sonic 2017 Multispectral Backscatter competition.

Bed observation data from Patricia Bay are digitized from data presented in: B.~Biffard. Seabed remote sensing by single-beam echosounder: models, methods and applications. Doctoral dissertation, University of Victoria, Canada, 2011.

Bed observation data from Portsmouth (NEWBEX) are digitized from data presented in: T.~Weber, L.~and Ward. Observations of backscatter from sand and gravel seafloors between 170 and 250 kHz. Journal of the Acoustical Society of America, vol.~138, no.~4, pp.~2169 - 2180, 2015.

CRF subfunctions using the [pydensecrf wrapper](https://github.com/lucasb-eyer/pydensecrf) 

## Setup

### Installing in a conda virtual env (recommended)

PriSM is designed for use with Python 3

Windows:

```
conda create --name prism_test python=3
activate prism_test
pip install Cython
conda install gdal rasterio shapely fiona -y
conda config --add channels conda-forge
conda install pydensecrf
```

![win1](https://user-images.githubusercontent.com/3596509/36634602-3abda3d4-1964-11e8-9a17-970e296c807f.png)

![win2](https://user-images.githubusercontent.com/3596509/36635357-9c4b57b6-1970-11e8-88bf-272674b43222.png)

```
pip install git+https://github.com/dbuscombe-usgs/prism.git
```

![win3](https://user-images.githubusercontent.com/3596509/36634628-a567d768-1964-11e8-8d19-3e8aba9b6f03.png)

If you get an error that looks like this:

![win4](https://user-images.githubusercontent.com/3596509/36635710-3d589a64-1977-11e8-8981-632dbd40f06a.png)


it means you need to install a C++ compiler. Go to this site: http://landinghub.visualstudio.com/visual-cpp-build-tools

and download the Visual C++ Build Tools 2015. Install using the 'default' setting. It takes about 5-10 minutes to install

![win_c++](https://user-images.githubusercontent.com/3596509/36635941-4b1bfd82-197a-11e8-85d4-c85b698886ea.png)

Run the PriSM installation again and it should work:

![win5](https://user-images.githubusercontent.com/3596509/36634775-12aacffe-1967-11e8-98d0-f1b6a7732d37.png)


Linux:

```
conda create --name prism_test python=3
source activate prism_test
pip install numpy Cython
pip install git+https://github.com/dbuscombe-usgs/prism.git
```

finally deactivate the venv ::

```
deactivate
```

Linux:

```
source deactivate
```


### Installing as a library accessible outside of virtual env


1. the latest 'bleeding edge' (pre-release) version directly from github::

```
pip install git+https://github.com/dbuscombe-usgs/prism.git
```

(Windows users) install git from here: https://git-scm.com/download/win


2. from github repo clone::

```
git clone git@github.com:dbuscombe-usgs/prism.git
cd prism
python setup.py install
```

or a local installation:

```
python setup.py install --user
```

3. linux users, using a virtual environment:

```
virtualenv venv
source venv/bin/activate
pip install numpy Cython
pip install git+https://github.com/dbuscombe-usgs/prism.git
deactivate ##(or source venv/bin/deactivate)
```


### Running the test

Then run the test ::

```
python -c "import prism; prism.test.dotest()" 
```

![win6](https://user-images.githubusercontent.com/3596509/36634778-1683d2ec-1967-11e8-9d9e-13cd52029a99.png)

![win7](https://user-images.githubusercontent.com/3596509/36635231-da48e2c4-196e-11e8-985c-aaa0d62d95c5.png)

### Using the GUI

run the GUI ::

```
python -c "import prism; prism.gui_funcs.gui()" 
```

![win8](https://user-images.githubusercontent.com/3596509/36635719-76f30246-1977-11e8-9cae-d2f9caf8c4fd.png)


or alternatively from within the python console like so:

![win9](https://user-images.githubusercontent.com/3596509/36635727-9184bf82-1977-11e8-82fd-ed8b9304aa5f.png)


## More info

Download the [user manual](https://daniel-buscombe.squarespace.com/s/prism_manual-hwpp.pdf) 


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

## Version History

v. 0.1. 2/26/2018. Initial public release




