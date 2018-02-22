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
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pyproj
import os
import numpy as np
from mpl_toolkits.basemap import Basemap
from prism.common_funcs import get_X
##-------------------------------------------------------------

##-------------------------------------------------------------
def plot_bs_maps(img, bed, bs, cmap, prefix):
   """
   This function ...
   """

   lonmin = bs[0]['lonmin']
   lonmax = bs[0]['lonmax']
   latmin = bs[0]['latmin']  
   latmax = bs[0]['latmax']

   #base = '..'+os.sep+'outputs'+os.sep+prefix+'_'
   base = prefix+'_'

   cmap = colors.ListedColormap(cmap)

   fig = plt.figure(dpi=300)
   ax1 = fig.add_subplot(111)
   im=plt.imshow(img, extent=[lonmin, lonmax, latmin, latmax]) ##, cmap=cmap, vmin=0, vmax=len(bed['labels']))
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   #plt.title('GMM-estimated substrate map', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   plt.savefig(base+'bs_map', dpi=300, bbox_inches='tight')
   plt.close('all')
   del fig


   fig = plt.figure(dpi=300)
   ax1 = fig.add_subplot(111)
   plt.imshow(img, extent=[lonmin, lonmax, latmin, latmax]) ##, cmap=cmap, vmin=0, vmax=len(bed['labels']))
   im = plt.scatter(bed['Xlon'], bed['Ylat'], 10, bed['Ccodes'], cmap=cmap, lw=.5, edgecolors='k', vmin=0, marker='s')
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   #plt.title('GMM-estimated substrate map', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'bs_map_bed_obs', dpi=300, bbox_inches='tight')
   plt.close('all')
   del fig

   #----------------------------------------------------------------
   X = bed['Xlon']
   Y = bed['Ylat']

   n = 0.0075

   if np.ndim(img)>2: #multispectral

      fig = plt.figure(frameon=False, dpi=300)
      ax1 = fig.add_subplot(131)
      map = Basemap(projection='merc', epsg='4326',
          resolution = 'i', #h #f
          llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
          urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

      try:
         map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
      except:
         map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
      finally:
         pass

      x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
      y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

      trans = pyproj.Proj(init=bs[0]['crs']['init'])

      glon, glat = np.meshgrid(x, y)
      glon, glat = trans(glon, glat, inverse=True)

      mx,my = map.projtran(glon, glat)

      tmp = np.flipud(img[:,:,0]).astype('float')
      tmp[tmp==0] = np.nan

      map.pcolormesh(mx, my, tmp, cmap='RdBu') #, cmap=cmap, vmin=0, vmax=len(bed['labels']))

      parallels = np.arange(np.min(glat),np.max(glat),0.005)
      map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

      meridians = np.arange(np.min(glon),np.max(glon),0.005)
      map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)


      ax1 = fig.add_subplot(132)
      map = Basemap(projection='merc', epsg='4326',
          resolution = 'i', #h #f
          llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
          urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

      try:
         map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
      except:
         map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
      finally:
         pass

      x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
      y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

      trans = pyproj.Proj(init=bs[0]['crs']['init'])

      glon, glat = np.meshgrid(x, y)
      glon, glat = trans(glon, glat, inverse=True)

      mx,my = map.projtran(glon, glat)

      tmp = np.flipud(img[:,:,1]).astype('float')
      tmp[tmp==0] = np.nan

      map.pcolormesh(mx, my, tmp, cmap='RdBu') #, cmap=cmap, vmin=0, vmax=len(bed['labels']))

      parallels = np.arange(np.min(glat),np.max(glat),0.005)
      map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

      meridians = np.arange(np.min(glon),np.max(glon),0.005)
      map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)


      ax1 = fig.add_subplot(133)
      map = Basemap(projection='merc', epsg='4326',
          resolution = 'i', #h #f
          llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
          urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

      try:
         map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
      except:
         map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
      finally:
         pass

      x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
      y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

      trans = pyproj.Proj(init=bs[0]['crs']['init'])

      glon, glat = np.meshgrid(x, y)
      glon, glat = trans(glon, glat, inverse=True)

      mx,my = map.projtran(glon, glat)

      tmp = np.flipud(img[:,:,2]).astype('float')
      tmp[tmp==0] = np.nan

      map.pcolormesh(mx, my, tmp, cmap='RdBu') #, cmap=cmap, vmin=0, vmax=len(bed['labels']))

      parallels = np.arange(np.min(glat),np.max(glat),0.005)
      map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

      meridians = np.arange(np.min(glon),np.max(glon),0.005)
      map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

      plt.savefig(base+'bs_map_image.png', dpi=300, bbox_inches='tight') #base+
      plt.close('all')
      del map, fig


   else: #monospectral

      fig = plt.figure(frameon=False, dpi=300)
      ax1 = fig.add_subplot(311)
      map = Basemap(projection='merc', epsg='4326',
          resolution = 'i', #h #f
          llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
          urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

      try:
         map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
      except:
         map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
      finally:
         pass

      x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
      y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

      trans = pyproj.Proj(init=bs[0]['crs']['init'])

      glon, glat = np.meshgrid(x, y)
      glon, glat = trans(glon, glat, inverse=True)

      mx,my = map.projtran(glon, glat)

      tmp = np.flipud(img).astype('float')
      tmp[tmp==0] = np.nan

      map.pcolormesh(mx, my, tmp, cmap='RdBu') #, cmap=cmap, vmin=0, vmax=len(bed['labels']))

      parallels = np.arange(np.min(glat),np.max(glat),0.005)
      map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

      meridians = np.arange(np.min(glon),np.max(glon),0.005)
      map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

      plt.savefig(base+'bs_map_image.png', dpi=300, bbox_inches='tight') #base+
      plt.close('all')
      del map, fig


##-------------------------------------------------------------
def plot_dists_per_sed(Lc, img, bed, cmap, prefix):
   """
   This function ...
   """

   #base = '..'+os.sep+'outputs'+os.sep+prefix+'_'
   base = prefix+'_'

   cmap = colors.ListedColormap(cmap)

   D, l = get_X(img, Lc)

   labs = bed['labels']

   fig = plt.figure(dpi=300)
   fig.subplots_adjust(hspace=0.4)
   ax=plt.subplot(231) 
   ax.set_facecolor((.5, .5, .5))

   b = np.arange(np.min(img),np.max(img),20)

   if np.ndim(img)>2: #multispectral

      counter = 1
      for k in np.unique(l):
         d, bins2 = np.histogram(D[l==k,0], b, normed=True)
         if np.all(np.isnan(d)):
            d, bins2 = np.histogram(D[l==k,0], normed=True)
         plt.plot(bins2[1:], d/np.nansum(d), '-o', color=cmap.colors[counter], linewidth=1, label=labs[counter], markersize=1)
         counter += 1

      plt.setp(plt.xticks()[1], fontsize=6)#, rotation=45)
      plt.setp(plt.yticks()[1], fontsize=6)#, rotation=45)
      plt.xlim(np.min(img),np.max(img)); plt.ylim(0,1)
      plt.legend(loc=2, fontsize=5)
      plt.xlabel('Backscatter Freq. 1 [-]', fontsize=6)
      plt.ylabel('Cumulative frequency', fontsize=6)  

      ax=plt.subplot(232)
      ax.set_facecolor((.5, .5, .5))
      counter = 1
      for k in np.unique(l):
         d, bins2 = np.histogram(D[l==k,1], b, normed=True)
         if np.all(np.isnan(d)):
            d, bins2 = np.histogram(D[l==k,0], normed=True)
         plt.plot(bins2[1:], d/np.sum(d), '-o', color=cmap.colors[counter], linewidth=1, label=labs[counter], markersize=1)
         counter += 1

      plt.setp(plt.xticks()[1], fontsize=6)#, rotation=45)
      plt.setp(plt.yticks()[1], fontsize=6)#, rotation=45)
      plt.xlim(np.min(img),np.max(img)); plt.ylim(0,1)
      plt.xlabel('Backscatter Freq. 2 [-]', fontsize=6)

      ax=plt.subplot(233)
      ax.set_facecolor((.5, .5, .5))
      counter = 1
      for k in np.unique(l):
         d, bins2 = np.histogram(D[l==k,2], b, normed=True)
         if np.all(np.isnan(d)):
            d, bins2 = np.histogram(D[l==k,0], normed=True)
         plt.plot(bins2[1:], d/np.sum(d), '-o', color=cmap.colors[counter], linewidth=1, label=labs[counter], markersize=1)
         counter += 1

      plt.setp(plt.xticks()[1], fontsize=6)#, rotation=45)
      plt.setp(plt.yticks()[1], fontsize=6)#, rotation=45)
      plt.xlim(np.min(img),np.max(img)); plt.ylim(0,1)
      plt.xlabel('Backscatter Freq. 3 [-]', fontsize=6)

      plt.savefig(base+'Dists_bs_per_sed', dpi=300, bbox_inches='tight')
      plt.close('all')
      del fig

   else:

      counter = 1
      for k in np.unique(l):
         d, bins2 = np.histogram(D[l==k,0], b, normed=True)
         if np.all(np.isnan(d)):
            d, bins2 = np.histogram(D[l==k,0], normed=True)
         plt.plot(bins2[1:], d/np.sum(d), '-o', color=cmap.colors[counter], linewidth=1, label=labs[counter], markersize=1)
         counter += 1
      plt.setp(plt.xticks()[1], fontsize=6)#, rotation=45)
      plt.setp(plt.yticks()[1], fontsize=6)#, rotation=45)
      plt.xlim(np.min(img),np.max(img)); plt.ylim(0,1)
      plt.legend(loc=2, fontsize=5)
      plt.xlabel('Backscatter Freq. [-]', fontsize=6)
      plt.ylabel('Cumulative frequency', fontsize=6)  

      plt.savefig(base+'Dists_bs_per_sed', dpi=300, bbox_inches='tight')
      plt.close('all')
      del fig

##-------------------------------------------------------------
def plot_gmm(mask, y_pred, y_prob, bs, bed, cmap, prefix):
   """
   This function ...
   """

   y_prob[mask==1] = np.nan   
   y_pred[mask==1] = np.nan
   
   cmap = colors.ListedColormap(cmap)

   lonmin = bs[0]['lonmin']
   lonmax = bs[0]['lonmax']
   latmin = bs[0]['latmin']  
   latmax = bs[0]['latmax']

   #base = '..'+os.sep+'outputs'+os.sep+prefix+'_'
   base = prefix+'_'

   #----------------------------------------------------------------

   fig = plt.figure(dpi=300)
   ax1 = fig.add_subplot(111)
   im=plt.imshow(y_pred, extent=[lonmin, lonmax, latmin, latmax], cmap=cmap, vmin=0, vmax=len(bed['labels']))
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('GMM-estimated substrate map', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'GMM_pred_map.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del fig


   fig = plt.figure(dpi=300)
   ax1 = fig.add_subplot(111)
   im=plt.imshow(y_pred, extent=[lonmin, lonmax, latmin, latmax], cmap=cmap, vmin=0, vmax=len(bed['labels']))
   plt.scatter(bed['Xlon'], bed['Ylat'], 3, bed['Ccodes'], cmap=cmap, lw=.5, edgecolors='k', vmin=0, marker='s')
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('GMM-estimated substrate map with bed obs.', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'GMM_pred_map_obs.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del fig


   fig = plt.figure(dpi=300)
   ax1 = fig.add_subplot(111)
   im=plt.imshow(y_prob, extent=[lonmin, lonmax, latmin, latmax], cmap='RdBu', vmin=0.5, vmax=1.0)
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('GMM posterior probability', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax, extend='min')
   #cb.set_ticks(.5+np.arange(len(labs)+1)) 
   #cb.ax.set_yticklabels(labs)
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'GMM_pred_prob_map.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del fig

##-------------------------------------------------------------
def plot_gmm_image(mask, y_pred, y_prob, bs, bed, cmap, prefix):
   """
   This function ...
   """

   y_prob[mask==1] = np.nan   
   y_pred[mask==1] = np.nan
   
   cmap = colors.ListedColormap(cmap)

   #base = '..'+os.sep+'outputs'+os.sep+prefix+'_'
   base = prefix+'_'

   #----------------------------------------------------------------
   X = bed['Xlon']
   Y = bed['Ylat']

   n = 0.0075
   fig = plt.figure(frameon=False, dpi=300)
   ax1 = fig.add_subplot(111)
   map = Basemap(projection='merc', epsg='4326',
       resolution = 'i', #h #f
       llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
       urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

   try:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
   except:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
   finally:
      pass

   x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
   y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

   trans = pyproj.Proj(init=bs[0]['crs']['init'])

   glon, glat = np.meshgrid(x, y)
   glon, glat = trans(glon, glat, inverse=True)

   mx,my = map.projtran(glon, glat)

   im=map.pcolormesh(mx, my, np.flipud(y_pred), cmap=cmap, vmin=0, vmax=len(bed['labels']))
   gx,gy = map.projtran(X, Y)

   #map.scatter(gx, gy, 5, bed['Ccodes'], cmap=cmap, vmin=0, vmax=len(bed['labels']), marker='s', edgecolor='k', lw=0.25)

   parallels = np.arange(np.min(glat),np.max(glat),0.005)
   map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   meridians = np.arange(np.min(glon),np.max(glon),0.005)
   map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   plt.title('GMM substrate classification', fontsize=4)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=4) 
   cb.ax.set_label('Substrate Type')

   plt.savefig(base+'GMM_map_image.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del map, fig


   ##-----------------------------------------------------------------------------
   n = 0.0075
   fig = plt.figure(frameon=False, dpi=300)
   ax1 = fig.add_subplot(111)
   map = Basemap(projection='merc', epsg='4326',
       resolution = 'i', #h #f
       llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
       urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

   try:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
   except:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
   finally:
      pass

   x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
   y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

   trans = pyproj.Proj(init=bs[0]['crs']['init'])

   glon, glat = np.meshgrid(x, y)
   glon, glat = trans(glon, glat, inverse=True)

   mx,my = map.projtran(glon, glat)

   im = map.pcolormesh(mx, my, np.flipud(y_prob), cmap='RdBu', vmin=0.5, vmax=1.0) #len(bed['labels']))
   gx,gy = map.projtran(X, Y)

   #map.scatter(gx, gy, 5, bed['Ccodes'], cmap=cmap, vmin=0, vmax=len(bed['labels']), marker='s', edgecolor='k', lw=0.25)

   parallels = np.arange(np.min(glat),np.max(glat),0.005)
   map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   meridians = np.arange(np.min(glon),np.max(glon),0.005)
   map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   plt.title('GMM posterior probability', fontsize=4)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax, extend='min')
   #cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   #cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=4) 
   cb.ax.set_label('Posterior Prob.')

   plt.savefig(base+'GMM_prob_image.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del map, fig



##-------------------------------------------------------------
def plot_crf(mask, y_pred, y_prob, bs, bed, cmap, prefix):
   """
   This function ...
   """
   
   y_prob[mask==1] = np.nan   
   y_pred[mask==1] = np.nan
   
   #base = '..'+os.sep+'outputs'+os.sep+prefix+'_'
   base = prefix+'_'

   cmap = colors.ListedColormap(cmap)

   lonmin = bs[0]['lonmin']
   lonmax = bs[0]['lonmax']
   latmin = bs[0]['latmin']  
   latmax = bs[0]['latmax']

   #----------------------------------------------------------------

   fig = plt.figure(dpi=300)
   ax1 = fig.add_subplot(111)
   im=plt.imshow(y_pred, extent=[lonmin, lonmax, latmin, latmax], cmap=cmap, vmin=0, vmax=len(bed['labels']))
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('CRF-estimated substrate map', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'CRF_pred_map.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del fig


   fig = plt.figure(dpi=300)
   ax1 = fig.add_subplot(111)
   im=plt.imshow(y_pred, extent=[lonmin, lonmax, latmin, latmax], cmap=cmap, vmin=0, vmax=len(bed['labels']))
   plt.scatter(bed['Xlon'], bed['Ylat'], 3, bed['Ccodes'], cmap=cmap, lw=.5, edgecolors='k', vmin=0, marker='s')
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('CRF-estimated substrate map with bed obs.', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'CRF_pred_map_obs.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del fig


   fig = plt.figure(dpi=300)
   ax1 = fig.add_subplot(111)
   im=plt.imshow(y_prob, extent=[lonmin, lonmax, latmin, latmax], cmap='RdBu', vmin=0.5, vmax=1.0)
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('CRF posterior probability', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax, extend='min')
   #cb.set_ticks(.5+np.arange(len(labs)+1)) 
   #cb.ax.set_yticklabels(labs)
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'CRF_pred_prob_map.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del fig

##-------------------------------------------------------------
def plot_crf_image(mask, y_pred, y_prob, bs, bed, cmap, prefix):
   """
   This function ...
   """
   y_prob[mask==1] = np.nan   
   y_pred[mask==1] = np.nan
   
   #base = '..'+os.sep+'outputs'+os.sep+prefix+'_'
   base = prefix+'_'

   cmap = colors.ListedColormap(cmap)

   #----------------------------------------------------------------
   X = bed['Xlon']
   Y = bed['Ylat']

   n = 0.0075
   fig = plt.figure(frameon=False, dpi=300)
   ax1 = fig.add_subplot(111)
   map = Basemap(projection='merc', epsg='4326',
       resolution = 'i', #h #f
       llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
       urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

   try:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
   except:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
   finally:
      pass

   x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
   y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

   trans = pyproj.Proj(init=bs[0]['crs']['init'])

   glon, glat = np.meshgrid(x, y)
   glon, glat = trans(glon, glat, inverse=True)

   mx,my = map.projtran(glon, glat)

   im=map.pcolormesh(mx, my, np.flipud(y_pred), cmap=cmap, vmin=0, vmax=len(bed['labels']))
   gx,gy = map.projtran(X, Y)

   #map.scatter(gx, gy, 5, bed['Ccodes'], cmap=cmap, vmin=0, vmax=len(bed['labels']), marker='s', edgecolor='k', lw=0.25)

   parallels = np.arange(np.min(glat),np.max(glat),0.005)
   map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   meridians = np.arange(np.min(glon),np.max(glon),0.005)
   map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   plt.title('CRF substrate classification', fontsize=4)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=4) 
   cb.ax.set_label('Substrate Type')

   plt.savefig(base+'CRF_map_image.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del map, fig


   ##-----------------------------------------------------------------------------
   n = 0.0075
   fig = plt.figure(frameon=False, dpi=300)
   ax1 = fig.add_subplot(111)
   map = Basemap(projection='merc', epsg='4326',
       resolution = 'i', #h #f
       llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
       urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

   try:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
   except:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
   finally:
      pass

   x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
   y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

   trans = pyproj.Proj(init=bs[0]['crs']['init'])

   glon, glat = np.meshgrid(x, y)
   glon, glat = trans(glon, glat, inverse=True)

   mx,my = map.projtran(glon, glat)

   im=map.pcolormesh(mx, my, np.flipud(y_prob), cmap='RdBu', vmin=0.5, vmax=1.0) ##len(bed['labels']))
   gx,gy = map.projtran(X, Y)

   #map.scatter(gx, gy, 5, bed['Ccodes'], cmap=cmap, vmin=0, vmax=len(bed['labels']), marker='s', edgecolor='k', lw=0.25)

   parallels = np.arange(np.min(glat),np.max(glat),0.005)
   map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   meridians = np.arange(np.min(glon),np.max(glon),0.005)
   map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   plt.title('CRF posterior probability', fontsize=4)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax, extend='min')
   #cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   #cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=4) 
   cb.ax.set_label('Posterior Prob.')

   plt.savefig(base+'CRF_prob_image.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del map, fig



##-------------------------------------------------------------
def plot_gmm_crf(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix):
   """
   This function ...
   """
   y_prob_gmm[mask==1] = np.nan   
   y_pred_gmm[mask==1] = np.nan
   y_prob_crf[mask==1] = np.nan   
   y_pred_crf[mask==1] = np.nan
   
   cmap = colors.ListedColormap(cmap)

   lonmin = bs[0]['lonmin']
   lonmax = bs[0]['lonmax']
   latmin = bs[0]['latmin']  
   latmax = bs[0]['latmax']

   #base = '..'+os.sep+'outputs'+os.sep+prefix+'_'
   base = prefix+'_'

   #----------------------------------------------------------------

   fig = plt.figure(dpi=300)
   fig.subplots_adjust(hspace=0.6)

   ax1 = fig.add_subplot(221)
   im=plt.imshow(y_pred_gmm, extent=[lonmin, lonmax, latmin, latmax], cmap=cmap, vmin=0, vmax=len(bed['labels']))
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('GMM-estimated substrate map', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=6) 
   cb.remove()

   ax1 = fig.add_subplot(222)
   im=plt.imshow(y_pred_crf, extent=[lonmin, lonmax, latmin, latmax], cmap=cmap, vmin=0, vmax=len(bed['labels']))
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('CRF-estimated substrate map', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'GMM_CRF_pred_map.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del fig


   fig = plt.figure(dpi=300)
   fig.subplots_adjust(hspace=0.6)

   ax1 = fig.add_subplot(221)
   im=plt.imshow(y_pred_gmm, extent=[lonmin, lonmax, latmin, latmax], cmap=cmap, vmin=0, vmax=len(bed['labels']))
   plt.scatter(bed['Xlon'], bed['Ylat'], 3, bed['Ccodes'], cmap=cmap, lw=.5, edgecolors='k', vmin=0, marker='s')
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('GMM-estimated substrate map with bed obs.', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=6) 
   cb.remove()

   ax1 = fig.add_subplot(222)
   im=plt.imshow(y_pred_crf, extent=[lonmin, lonmax, latmin, latmax], cmap=cmap, vmin=0, vmax=len(bed['labels']))
   plt.scatter(bed['Xlon'], bed['Ylat'], 3, bed['Ccodes'], cmap=cmap, lw=.5, edgecolors='k', vmin=0, marker='s')
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('CRF-estimated substrate map with bed obs.', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'GMM_CRF_pred_map_obs.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del fig


   fig = plt.figure(dpi=300)
   fig.subplots_adjust(hspace=0.6)

   ax1 = fig.add_subplot(221)
   im=plt.imshow(y_prob_gmm, extent=[lonmin, lonmax, latmin, latmax], cmap='RdBu', vmin=0.5, vmax=1.0)
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('GMM posterior probability', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   #divider = make_axes_locatable(ax1)
   #cax = divider.append_axes("right", size="5%")
   #cb=plt.colorbar(im, cax=cax)
   ##cb.set_ticks(.5+np.arange(len(labs)+1)) 
   ##cb.ax.set_yticklabels(labs)
   #cb.ax.tick_params(labelsize=6) 

   ax1 = fig.add_subplot(222)
   im=plt.imshow(y_prob_crf, extent=[lonmin, lonmax, latmin, latmax], cmap='RdBu', vmin=0.5, vmax=1.0)
   plt.ylim(latmin, latmax)
   plt.xlim(lonmin, lonmax)
   ax1.get_xaxis().get_major_formatter().set_useOffset(False)
   ax1.get_yaxis().get_major_formatter().set_useOffset(False)
   la = ax1.get_xticklabels()
   plt.setp(la, fontsize=6)#, rotation=30)
   la = ax1.get_yticklabels()
   plt.setp(la, fontsize=6, rotation=60)
   plt.title('CRF posterior probability', loc='left', fontsize=6)
   ax1.spines['right'].set_visible(False)
   ax1.spines['top'].set_visible(False)
   ax1.spines['left'].set_visible(False)
   ax1.spines['bottom'].set_visible(False)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax, extend='min')
   #cb.set_ticks(.5+np.arange(len(labs)+1)) 
   #cb.ax.set_yticklabels(labs)
   cb.ax.tick_params(labelsize=6) 

   plt.savefig(base+'GMM_CRF_pred_prob_map.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del fig


##-------------------------------------------------------------
def plot_gmm_crf_images(mask, y_pred_gmm, y_prob_gmm, y_pred_crf, y_prob_crf, bs, bed, cmap, prefix):
   """
   This function ...
   """
   y_prob_gmm[mask==1] = np.nan   
   y_pred_gmm[mask==1] = np.nan
   y_prob_crf[mask==1] = np.nan   
   y_pred_crf[mask==1] = np.nan
   
   #base = '..'+os.sep+'outputs'+os.sep+prefix+'_'
   base = prefix+'_'

   cmap = colors.ListedColormap(cmap)

   #----------------------------------------------------------------
   X = bed['Xlon']
   Y = bed['Ylat']

   n = 0.0075

   fig = plt.figure(frameon=False, dpi=300)
   fig.subplots_adjust(hspace=0.4)

   ax1 = fig.add_subplot(221)
   map = Basemap(projection='merc', epsg='4326',
       resolution = 'i', #h #f
       llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
       urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

   try:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
   except:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
   finally:
      pass

   x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
   y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

   trans = pyproj.Proj(init=bs[0]['crs']['init'])

   glon, glat = np.meshgrid(x, y)
   glon, glat = trans(glon, glat, inverse=True)

   mx,my = map.projtran(glon, glat)

   im=map.pcolormesh(mx, my, np.flipud(y_pred_gmm), cmap=cmap, vmin=0, vmax=len(bed['labels']))
   gx,gy = map.projtran(X, Y)

   #map.scatter(gx, gy, 5, bed['Ccodes'], cmap=cmap, vmin=0, vmax=len(bed['labels']), marker='s', edgecolor='k', lw=0.25)

   parallels = np.arange(np.min(glat),np.max(glat),0.005)
   map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   meridians = np.arange(np.min(glon),np.max(glon),0.005)
   map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   plt.title('GMM substrate classification', fontsize=4)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=4) 
   cb.ax.set_label('Substrate Type')

   ax1 = fig.add_subplot(222)
   map = Basemap(projection='merc', epsg='4326',
       resolution = 'i', #h #f
       llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
       urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

   try:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
   except:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
   finally:
      pass

   x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
   y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

   trans = pyproj.Proj(init=bs[0]['crs']['init'])

   glon, glat = np.meshgrid(x, y)
   glon, glat = trans(glon, glat, inverse=True)

   mx,my = map.projtran(glon, glat)

   im=map.pcolormesh(mx, my, np.flipud(y_pred_crf), cmap=cmap, vmin=0, vmax=len(bed['labels']))
   gx,gy = map.projtran(X, Y)

   #map.scatter(gx, gy, 5, bed['Ccodes'], cmap=cmap, vmin=0, vmax=len(bed['labels']), marker='s', edgecolor='k', lw=0.25)

   parallels = np.arange(np.min(glat),np.max(glat),0.005)
   map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   meridians = np.arange(np.min(glon),np.max(glon),0.005)
   map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   plt.title('CRF substrate classification', fontsize=4)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax)
   cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=4) 
   cb.ax.set_label('Substrate Type')

   plt.savefig(base+'GMM_CRF_map_image.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del map, fig


   ##-----------------------------------------------------------------------------
   n = 0.0075

   fig = plt.figure(frameon=False, dpi=300)
   fig.subplots_adjust(hspace=0.4)

   ax1 = fig.add_subplot(221)
   map = Basemap(projection='merc', epsg='4326',
       resolution = 'i', #h #f
       llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
       urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

   try:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
   except:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
   finally:
      pass

   x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
   y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

   trans = pyproj.Proj(init=bs[0]['crs']['init'])

   glon, glat = np.meshgrid(x, y)
   glon, glat = trans(glon, glat, inverse=True)

   mx,my = map.projtran(glon, glat)

   im=map.pcolormesh(mx, my, np.flipud(y_prob_gmm), cmap='RdBu', vmin=0.5, vmax=1.0) #, vmin=0, vmax=len(bed['labels']))
   gx,gy = map.projtran(X, Y)

   #map.scatter(gx, gy, 5, bed['Ccodes'], cmap=cmap, vmin=0, vmax=len(bed['labels']), marker='s', edgecolor='k', lw=0.25)

   parallels = np.arange(np.min(glat),np.max(glat),0.005)
   map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   meridians = np.arange(np.min(glon),np.max(glon),0.005)
   map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   plt.title('GMM posterior probability', fontsize=4)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax, extend='min')
   #cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   #cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=4) 
   cb.ax.set_label('Posterior Prob.')


   ax1 = fig.add_subplot(222)
   map = Basemap(projection='merc', epsg='4326',
       resolution = 'i', #h #f
       llcrnrlon=np.min(X)-n, llcrnrlat=np.min(Y)-n,
       urcrnrlon=np.max(X)+n, urcrnrlat=np.max(Y)+n)

   try:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='World_Imagery', xpixels=1000, ypixels=None, dpi=300)
   except:
      map.arcgisimage(server='http://server.arcgisonline.com/ArcGIS', service='ESRI_Imagery_World_2D', xpixels=1000, ypixels=None, dpi=300)
   finally:
      pass

   x = np.arange(bs[0]['xmin'],bs[0]['xmax'],bs[0]['gridres'])
   y = np.arange(bs[0]['ymin'],bs[0]['ymax'],bs[0]['gridres'])

   trans = pyproj.Proj(init=bs[0]['crs']['init'])

   glon, glat = np.meshgrid(x, y)
   glon, glat = trans(glon, glat, inverse=True)

   mx,my = map.projtran(glon, glat)

   im=map.pcolormesh(mx, my, np.flipud(y_prob_crf), cmap='RdBu', vmin=0.5, vmax=1.0) #len(bed['labels']))
   gx,gy = map.projtran(X, Y)

   #map.scatter(gx, gy, 5, bed['Ccodes'], cmap=cmap, vmin=0, vmax=len(bed['labels']), marker='s', edgecolor='k', lw=0.25)

   parallels = np.arange(np.min(glat),np.max(glat),0.005)
   map.drawparallels(parallels,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   meridians = np.arange(np.min(glon),np.max(glon),0.005)
   map.drawmeridians(meridians,labels=[1,0,0,1], color='w',fontsize=3, rotation=45, linewidth=0.25)

   plt.title('CRF posterior probability', fontsize=4)

   divider = make_axes_locatable(ax1)
   cax = divider.append_axes("right", size="5%")
   cb=plt.colorbar(im, cax=cax, extend='min')
   #cb.set_ticks(.5+np.arange(len(bed['labels'])+1)) 
   #cb.ax.set_yticklabels(bed['labels'])
   cb.ax.tick_params(labelsize=4) 
   cb.ax.set_label('Posterior Prob.')


   plt.savefig(base+'GMM_CRF_prob_image.png', dpi=300, bbox_inches='tight') #base+
   plt.close('all')
   del map, fig



