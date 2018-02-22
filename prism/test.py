#    ____  ____  ___ ____  __  __     
#   |  _ \|  _ \|_ _/ ___||  \/  |  _ 
#   | |_) | |_) || |\___ \| |\/| | (_)
#   |  __/|  _ < | | ___) | |  | |  _ 
#   |_|   |_| \_\___|____/|_|  |_| (_)
#                                     
#   ___                 _      _                  __                   __      
#    | _  _ ||_  _ \/ _|__ ._ |_).__ |_  _.|_ o|o(__|_o _  /\  _ _    (__|_o _ 
#    |(_)(_)||_)(_)/\  |(_)|  |  |(_)|_)(_||_)|||__)|_|(_ /--\(_(_)|_|__)|_|(_ 
#                                                                              
#    __                                          
#   (_  _  _|o._ _  _ .__|_ |\/| _.._ ._ o._  _  
#   __)(/_(_||| | |(/_| ||_ |  |(_||_)|_)|| |(_| 
#                                  |  |       _| 
#
#   |b|y| |D|a|n|i|e|l| |B|u|s|c|o|m|b|e|
#   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#   |d|a|n|i|e|l|.|b|u|s|c|o|m|b|e|@|n|a|u|.|e|d|u|

##-------------------------------------------------------------
# general
from __future__ import division
import sys
import warnings
warnings.filterwarnings("ignore")
import numpy as np
np.seterr(divide='ignore')
np.seterr(invalid='ignore')
import os

# prism functions
from common_funcs import get_sparse_labels
from gmm_funcs import fit_GMM, apply_GMM
from crf_funcs import apply_CRF
from read_funcs import *
from write_funcs import *
from eval_funcs import *
from plot_funcs import *
##-------------------------------------------------------------

##GMM parameters
covariance = 'full'
tol = 1e-2

##CRF parameters
theta = 300 
mu = 100 
n_iter = 15

#==================================================================================
## patricia
gridres = 1
buff = 10
prob_thres = 0.7
chambolle = 0.2
test_size = 0.5
prefix = 'patricia'

bs100 = '..'+os.sep+'data'+os.sep+'patricia2016'+os.sep+'bs'+os.sep+'mosaic_100.tiff'
bs200 = '..'+os.sep+'data'+os.sep+'patricia2016'+os.sep+'bs'+os.sep+'mosaic_200.tiff'
bs400 = '..'+os.sep+'data'+os.sep+'patricia2016'+os.sep+'bs'+os.sep+'mosaic_400.tiff'
refs_file = '..'+os.sep+'data'+os.sep+'patricia2016'+os.sep+'ref'+os.sep+'point_data.shp'

input = [bs100, bs200, bs400]
img, bs = read_geotiff(input, gridres, chambolle)

bed = read_shpfile(refs_file, bs)
Lc = get_sparse_labels(bs, bed, buff)

if np.ndim(img)>2:
   mask = img[:,:,0]==0
else:
   mask = img==0

#### GMM
g = fit_GMM(img, Lc, test_size, covariance, tol)
y_pred_gmm, y_prob_gmm, y_gmm_prob_per_class = apply_GMM(g, img, prob_thres)

#### CRF
y_pred_crf, y_prob_crf, y_crf_prob_per_class = apply_CRF(img, Lc, bed['labels'], n_iter, prob_thres, theta, mu)

### plot
cmap = ['gray', '#FAFAD2','b', '#D2691E','y', '#87CEFA', '#FF7F50']
plot_dists_per_sed(Lc, img, bed, cmap, prefix)

plot_gmm(mask, y_pred_gmm, y_prob_gmm, bs, bed, cmap, prefix)
plot_crf(mask, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix)

plot_gmm_image(mask, y_pred_gmm, y_prob_gmm, bs, bed, cmap, prefix)
plot_crf_image(mask, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix)

plot_gmm_crf(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix)
plot_gmm_crf_images(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix)
plot_bs_maps(img, bed, bs, cmap, prefix)

plot_confmatCRF(y_pred_crf, Lc, bed, prefix)
plot_confmatGMM(y_pred_gmm, Lc, bed, prefix)

## write out data
export_bed_data(bed, prefix)
export_gmm_gtiff(mask, y_pred_gmm.copy(), y_prob_gmm.copy(), bs, prefix)
export_crf_gtiff(mask, y_pred_crf.copy(), y_prob_crf.copy(), bs, prefix)


#==================================================================================
##newbex
gridres = 1
buff = 10
prob_thres = 0.1
chambolle = 0.0
test_size = 0.5
bs100 = '..'+os.sep+'data'+os.sep+'newbex'+os.sep+'bs'+os.sep+'mosaic_100.tiff'
bs200 = '..'+os.sep+'data'+os.sep+'newbex'+os.sep+'bs'+os.sep+'mosaic_200.tiff'
bs400 = '..'+os.sep+'data'+os.sep+'newbex'+os.sep+'bs'+os.sep+'mosaic_400.tiff'
refs_file = '..'+os.sep+'data'+os.sep+'newbex'+os.sep+'ref'+os.sep+'newbex_bed.shp'
prefix = 'newbex'

input = [bs100, bs200, bs400]
img, bs = read_geotiff(input, gridres, chambolle)

bed = read_shpfile(refs_file, bs)
Lc = get_sparse_labels(bs, bed, buff)

if np.ndim(img)>2:
   mask = img[:,:,0]==0
else:
   mask = img==0


#### GMM
g = fit_GMM(img, Lc, test_size, covariance, tol)
y_pred_gmm, y_prob_gmm, y_gmm_prob_per_class = apply_GMM(g, img, prob_thres)

#### CRF
y_pred_crf, y_prob_crf, y_crf_prob_per_class = apply_CRF(img, Lc, bed['labels'], n_iter, prob_thres, theta, mu)

### plot
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

## write out data
export_bed_data(bed, prefix)
export_gmm_gtiff(mask, y_pred_gmm.copy(), y_prob_gmm.copy(), bs, prefix)
export_crf_gtiff(mask, y_pred_crf.copy(), y_prob_crf.copy(), bs, prefix)


#==================================================================================
##bedford 2016
gridres = 1
buff = 10
prob_thres = 0.7
chambolle = 0.2
test_size = 0.5
bs100 = '..'+os.sep+'data'+os.sep+'bedford2016'+os.sep+'bs'+os.sep+'mosaic_100.tiff'
bs200 = '..'+os.sep+'data'+os.sep+'bedford2016'+os.sep+'bs'+os.sep+'mosaic_200.tiff'
bs400 = '..'+os.sep+'data'+os.sep+'bedford2016'+os.sep+'bs'+os.sep+'mosaic_400.tiff'
refs_file = '..'+os.sep+'data'+os.sep+'bedford2016'+os.sep+'ref'+os.sep+'X_y_ID_label.csv'
prefix = 'bedford2016'

input = [bs100, bs200, bs400]
img, bs = read_geotiff(input, gridres, chambolle)

bed = read_csvfile(refs_file, bs)
Lc = get_sparse_labels(bs, bed, buff)

if np.ndim(img)>2:
   mask = img[:,:,0]==0
else:
   mask = img==0

#### GMM
g = fit_GMM(img, Lc, test_size, covariance, tol)
y_pred_gmm, y_prob_gmm, y_gmm_prob_per_class = apply_GMM(g, img, prob_thres)

#### CRF
y_pred_crf, y_prob_crf, y_crf_prob_per_class = apply_CRF(img, Lc, bed['labels'], n_iter, prob_thres, theta, mu)

### plot
cmap = plt.get_cmap('tab20b',len(bed['labels'])-1).colors

cmap1 = []
cmap1.append('gray')
for k in cmap:
   cmap1.append(colors.rgb2hex(k))

plot_dists_per_sed(Lc, img, bed, cmap1, prefix)

plot_gmm(mask, y_pred_gmm, y_prob_gmm, bs, bed, cmap1, prefix)
plot_crf(mask, y_pred_crf, y_prob_crf, bs, bed, cmap1, prefix)

plot_gmm_image(mask, y_pred_gmm, y_prob_gmm, bs, bed, cmap1, prefix)
plot_crf_image(mask, y_pred_crf, y_prob_crf, bs, bed, cmap1, prefix)

plot_gmm_crf(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap1, prefix)
plot_gmm_crf_images(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap1, prefix)
plot_bs_maps(img, bed, bs, cmap1, prefix)

plot_confmatCRF(y_pred_crf, Lc, bed, prefix)
plot_confmatGMM(y_pred_gmm, Lc, bed, prefix)

## write out data
export_bed_data(bed, prefix)
export_gmm_gtiff(mask, y_pred_gmm.copy(), y_prob_gmm.copy(), bs, prefix)
export_crf_gtiff(mask, y_pred_crf.copy(), y_prob_crf.copy(), bs, prefix)


#==================================================================================
##bedford 2017
gridres = 1
buff = 10
prob_thres = 0.7
chambolle = 0.2
test_size = 0.5
bs100 = '..'+os.sep+'data'+os.sep+'bedford2017'+os.sep+'bs'+os.sep+'mosaic_100.tiff'
bs200 = '..'+os.sep+'data'+os.sep+'bedford2017'+os.sep+'bs'+os.sep+'mosaic_200.tiff'
bs400 = '..'+os.sep+'data'+os.sep+'bedford2017'+os.sep+'bs'+os.sep+'mosaic_400.tiff'
refs_file = '..'+os.sep+'data'+os.sep+'bedford2017'+os.sep+'ref'+os.sep+'X_y_ID_label.csv'
prefix = 'bedford2017'

input = [bs100, bs200, bs400]
img, bs = read_geotiff(input, gridres, chambolle)

bed = read_csvfile(refs_file, bs)
Lc = get_sparse_labels(bs, bed, buff)

if np.ndim(img)>2:
   mask = img[:,:,0]==0
else:
   mask = img==0

#### GMM
g = fit_GMM(img, Lc, test_size, covariance, tol)
y_pred_gmm, y_prob_gmm, y_gmm_prob_per_class = apply_GMM(g, img, prob_thres)

#### CRF
y_pred_crf, y_prob_crf, y_crf_prob_per_class = apply_CRF(img, Lc, bed['labels'], n_iter, prob_thres, theta, mu)

### plot
cmap = plt.get_cmap('tab20b',len(bed['labels'])-1).colors

cmap1 = []
cmap1.append('gray')
for k in cmap:
   cmap1.append(colors.rgb2hex(k))

plot_dists_per_sed(Lc, img, bed, cmap1, prefix)

plot_gmm(mask, y_pred_gmm, y_prob_gmm, bs, bed, cmap1, prefix)
plot_crf(mask, y_pred_crf, y_prob_crf, bs, bed, cmap1, prefix)

plot_gmm_image(mask, y_pred_gmm, y_prob_gmm, bs, bed, cmap1, prefix)
plot_crf_image(mask, y_pred_crf, y_prob_crf, bs, bed, cmap1, prefix)

plot_gmm_crf(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap1, prefix)
plot_gmm_crf_images(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap1, prefix)
plot_bs_maps(img, bed, bs, cmap1, prefix)

plot_confmatCRF(y_pred_crf, Lc, bed, prefix)
plot_confmatGMM(y_pred_gmm, Lc, bed, prefix)

## write out data
export_bed_data(bed, prefix)
export_gmm_gtiff(mask, y_pred_gmm.copy(), y_prob_gmm.copy(), bs, prefix)
export_crf_gtiff(mask, y_pred_crf.copy(), y_prob_crf.copy(), bs, prefix)





