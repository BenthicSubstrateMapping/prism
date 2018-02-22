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
from __future__ import division
import rasterio
from scipy.ndimage import zoom
import numpy as np
import fiona
import pyproj
from shapely.geometry.polygon import Polygon
from shapely.geometry import Point
##-------------------------------------------------------------

##-------------------------------------------------------------
def read_csvfile(refs_file, bs):
   """
   This function ...
   """
   dat = np.genfromtxt(refs_file, delimiter=',', names=True, dtype=[float, float, float, "|S10"] )

   X = dat['X']
   Y = dat['Y']
   C = dat['ID']
   Cnames = dat['label']
   del dat

   Clist = []
   for k in np.unique(C):
      Clist.append(Cnames[C==k][0])

   # just looking at points within bounding box of survey
   ## ========================================================= 
   polygon = Polygon ([(bs[0]['lonmin'], bs[0]['latmin']),
    (bs[0]['lonmin'], bs[0]['latmax']),
    (bs[0]['lonmax'], bs[0]['latmax']),
    (bs[0]['lonmax'], bs[0]['latmin'])])

   ind1 = []
   for k in range(len(X)):
      if polygon.contains(Point(X[k], Y[k])):
         ind1.append(1)
      else:
         ind1.append(0)
   
   ind1 = np.asarray(ind1)
   ind1 = np.where(ind1==1)[0]

   # just looking at points within survey extent
   ## ========================================================= 
   obs_x, obs_y = bs[0]['trans'](np.asarray(X)[ind1], np.asarray(Y)[ind1])

   gres = bs[0]['gridres']
   nx, ny = np.shape(bs[0]['bs'])
   ind2 = []
   for k in range(len(obs_x)):
      y = (1/gres*np.round(obs_x[k] - bs[0]['xmin'])).astype('int')
      x = (1/gres*np.round(bs[0]['ymax'] - obs_y[k])).astype('int')
      if bs[0]['bs'][x,y]>0:
         ind2.append(k)

   X = np.asarray(X)[ind1][ind2]
   Y = np.asarray(Y)[ind1][ind2]
   Cnames = np.asarray(Cnames)[ind1][ind2]
   Ccodes = np.asarray(C)[ind1][ind2]

   # transform lat/lon to projected coordinate system of survey
   obs_x, obs_y = bs[0]['trans'](X, Y)

   # get labels and recode from 1
   vals = np.unique(Ccodes)

   labels = [Clist[val-1].decode("utf-8") for val in vals.astype('int')]

   labels = ['unknown']+labels

   Ccodes = np.asarray(Ccodes)
   counter=0
   for v in vals.astype('int'):
      Ccodes[Ccodes==v] = counter
      counter +=1

   Ccodes += 1

   return {'Xlon':X, 'Ylat':Y, 'Xproj':obs_x, 'Yproj':obs_y, 'Ccodes':Ccodes, 'Cnames':Cnames, 'labels':labels}

##-------------------------------------------------------------
def read_shpfile(refs_file, bs):
   """
   This function ...
   """

   print('Reading and filtering bed observation data ...')
   shape = fiona.open(refs_file)
   X = []; Y= []; C=[]
   for tmp in shape:
      if len(np.squeeze(tmp['geometry']['coordinates'])) > 2:
         xy = np.squeeze(np.mean(tmp['geometry']['coordinates'], axis=1))
         X.append(xy[0])
         Y.append(xy[1])
      else:
         X.append(tmp['geometry']['coordinates'][0])
         Y.append(tmp['geometry']['coordinates'][1])

      C.append(tmp['properties'][list(tmp['properties'].keys())[0]])

   shape.close()
   Clist = np.unique(C).tolist()

   if np.all(np.isreal(Clist)):
      Ccodes = C
   else:
      Ccodes = [Clist.index(c) for c in C]

   # just looking at points within bounding box of survey
   ## ========================================================= 
   polygon = Polygon ([(bs[0]['lonmin'], bs[0]['latmin']),
    (bs[0]['lonmin'], bs[0]['latmax']),
    (bs[0]['lonmax'], bs[0]['latmax']),
    (bs[0]['lonmax'], bs[0]['latmin'])])

   ind1 = []
   for k in range(len(X)):
      if polygon.contains(Point(X[k], Y[k])):
         ind1.append(1)
      else:
         ind1.append(0)
   
   ind1 = np.asarray(ind1)
   ind1 = np.where(ind1==1)[0]

   # just looking at points within survey extent
   ## ========================================================= 
   obs_x, obs_y = bs[0]['trans'](np.asarray(X)[ind1], np.asarray(Y)[ind1])

   gres = bs[0]['gridres']
   nx, ny = np.shape(bs[0]['bs'])
   ind2 = []
   for k in range(len(obs_x)):
      y = (1/gres*np.round(obs_x[k] - bs[0]['xmin'])).astype('int')
      x = (1/gres*np.round(bs[0]['ymax'] - obs_y[k])).astype('int')
      if bs[0]['bs'][x,y]>0:
         ind2.append(k)

   X = np.asarray(X)[ind1][ind2]
   Y = np.asarray(Y)[ind1][ind2]
   Ccodes = np.asarray(Ccodes)[ind1][ind2]
   Cnames = np.asarray(C)[ind1][ind2]

   # transform lat/lon to projected coordinate system of survey
   obs_x, obs_y = bs[0]['trans'](X, Y)

   # get labels and recode from 1
   vals = np.unique(Ccodes)

   labels = []
   for val in vals:
      labels.append(str(Cnames[Ccodes==val][0])) #.decode("utf-8")

   #labels = [Cnames[val] for val in vals.astype('int')]

   labels = ['unknown']+labels

   Ccodes = np.asarray(Ccodes)
   counter=0
   for v in vals.astype('int'):
      Ccodes[Ccodes==v] = counter
      counter +=1

   Ccodes += 1

   return {'Xlon':X, 'Ylat':Y, 'Xproj':obs_x, 'Yproj':obs_y, 'Ccodes':Ccodes, 'Cnames':Cnames, 'labels':labels}


##-------------------------------------------------------------
def read_geotiff(input, gridres, chambolle):
   """
   This function ...
   """
   ## input = list of strings of filenames
   ## output gridres = grd resolution in m

   print('Reading GeoTIFF data ...')
   if type(input) is not list:
      input = [input]

   ## read all arrays
   bs = []
   for layer in input:
      with rasterio.open(layer) as src:
         layer = src.read()[0,:,:]
      w, h = (src.width, src.height)
      xmin, ymin, xmax, ymax = src.bounds
      crs = src.get_crs()
      del src
      bs.append({'bs':layer, 'w':w, 'h':h, 'xmin':xmin, 'xmax':xmax, 'ymin':ymin, 'ymax':ymax, 'crs':crs})

   #get pyproj transformation object
   trans = pyproj.Proj(init=bs[0]['crs']['init'])

   ## resize arrays so common grid
   ##get bounds
   xmax = max([x['xmax'] for x in bs])
   xmin = min([x['xmin'] for x in bs])
   ymax = max([x['ymax'] for x in bs])
   ymin = min([x['ymin'] for x in bs])
   ## make common grid
   yp, xp = np.meshgrid(np.arange(xmin, xmax, gridres), np.arange(ymin, ymax, gridres))

   ## get extents in lat/lon
   lonmin, latmin = trans(xmin, ymin, inverse=True)
   lonmax, latmax = trans(xmax, ymax, inverse=True)

   nx, ny = np.shape(yp)
   for k in range(len(bs)):
      bs[k]['bs'] = zoom(bs[k]['bs'], (nx/bs[k]['h'], ny/bs[k]['w']))
      bs[k]['h'] = nx
      bs[k]['w'] = ny
      bs[k]['xmin'] = xmin
      bs[k]['xmax'] = xmax
      bs[k]['ymin'] = ymin
      bs[k]['ymax'] = ymax
      bs[k]['latmin'] = latmin
      bs[k]['latmax'] = latmax
      bs[k]['lonmin'] = lonmin
      bs[k]['lonmax'] = lonmax
      bs[k]['trans'] = trans
      bs[k]['gridres'] = gridres

   img = np.dstack([x['bs'] for x in bs]).astype('uint8')

   if chambolle>0:
      from skimage.restoration import denoise_tv_chambolle
      if len(bs)>1:
         tv = denoise_tv_chambolle(img, weight=chambolle, multichannel=True)
      else:
         tv = denoise_tv_chambolle(img, weight=chambolle, multichannel=False)
      img = (255*tv).astype('uint8')
      del tv

   return np.squeeze(img), bs



