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
from osgeo import gdal,ogr,osr
import numpy as np
import os
from shapely.geometry import Point, mapping
from fiona import collection
import csv
##-------------------------------------------------------------

##-------------------------------------------------------------
def export_bed_data(bed, prefix):
   """
   This function ...
   """

   base = '..'+os.sep+'outputs'+os.sep+prefix+'_'

   rows = zip(bed['Xlon'], bed['Ylat'], bed['Cnames'], bed['Ccodes'])

   with open(base+'bed_observations.csv', 'w', newline='') as csvfile:
      spamwriter = csv.writer(csvfile, delimiter=',') #quotechar='|', quoting=csv.QUOTE_MINIMAL
      spamwriter.writerow(('longitude' ,'latitude', 'ID', 'code'))
      for row in rows:
         spamwriter.writerow(row)

   schema = { 'geometry': 'Point', 'properties': { 'name': 'str' } }
   with collection(base+'bed_observations.shp', "w", "ESRI Shapefile", schema) as output:
      with open(base+'bed_observations.csv', 'r') as f:
         reader = csv.DictReader(f)
         for row in reader:
            point = Point(float(row['longitude']), float(row['latitude']))
            output.write({
                'properties': {
                    'name': row['ID']
                },
                'geometry': mapping(point)
            })

##-------------------------------------------------------------
def export_crf_gtiff(mask, y_pred, y_prob, bs, prefix):
   """
   This function ...
   """

   prob = y_prob.copy()
   pred = y_pred.copy()
   del y_prob, y_pred

   prob[mask==1] = np.nan   
   pred[mask==1] = np.nan
   
   base = '..'+os.sep+'outputs'+os.sep+prefix+'_'

   proj = osr.SpatialReference()
   proj.ImportFromEPSG(4326) 
   datout = np.squeeze(np.ma.filled(pred))

   del pred

   datout[np.isnan(datout)] = -99
   driver = gdal.GetDriverByName('GTiff')
   cols,rows = np.shape(datout)    

   outFile = os.path.normpath(base+'crf_map.tif')
   ds = driver.Create( outFile, rows, cols, 1, gdal.GDT_Float32, [ 'COMPRESS=LZW' ] )        
   if proj is not None:  
     ds.SetProjection(proj.ExportToWkt()) 

   xmin, ymin, xmax, ymax = [bs[0]['lonmin'], bs[0]['latmin'], bs[0]['lonmax'], bs[0]['latmax']]

   xres = (xmax - xmin) / float(rows)
   yres = (ymax - ymin) / float(cols)

   geotransform = (xmin, xres, 0, ymax, 0, -yres)

   ds.SetGeoTransform(geotransform)
   ss_band = ds.GetRasterBand(1)
   ss_band.WriteArray(datout) 
   ss_band.SetNoDataValue(-99)
   ss_band.FlushCache()
   ss_band.ComputeStatistics(False)
   del ds   


   #-----------------------------------------------------------
   proj = osr.SpatialReference()
   proj.ImportFromEPSG(4326) 
   datout = np.squeeze(np.ma.filled(prob))

   del prob

   datout[np.isnan(datout)] = -99
   driver = gdal.GetDriverByName('GTiff')
   cols,rows = np.shape(datout)    

   outFile = os.path.normpath(base+'crf_prob_map.tif')
   ds = driver.Create( outFile, rows, cols, 1, gdal.GDT_Float32, [ 'COMPRESS=LZW' ] )        
   if proj is not None:  
     ds.SetProjection(proj.ExportToWkt()) 

   ds.SetGeoTransform(geotransform)
   ss_band = ds.GetRasterBand(1)
   ss_band.WriteArray(datout) 
   ss_band.SetNoDataValue(-99)
   ss_band.FlushCache()
   ss_band.ComputeStatistics(False)
   del ds  

##-------------------------------------------------------------
def export_gmm_gtiff(mask, y_pred, y_prob, bs, prefix):
   """
   This function ...
   """
   prob = y_prob.copy()
   pred = y_pred.copy()
   del y_prob, y_pred

   prob[mask==1] = np.nan   
   pred[mask==1] = np.nan
   
   base = '..'+os.sep+'outputs'+os.sep+prefix+'_'

   proj = osr.SpatialReference()
   proj.ImportFromEPSG(4326) 
   datout = np.squeeze(np.ma.filled(pred))

   del pred

   datout[np.isnan(datout)] = -99
   driver = gdal.GetDriverByName('GTiff')
   cols,rows = np.shape(datout)    

   outFile = os.path.normpath(base+'gmm_map.tif')
   ds = driver.Create( outFile, rows, cols, 1, gdal.GDT_Float32, [ 'COMPRESS=LZW' ] )        
   if proj is not None:  
     ds.SetProjection(proj.ExportToWkt()) 

   xmin, ymin, xmax, ymax = [bs[0]['lonmin'], bs[0]['latmin'], bs[0]['lonmax'], bs[0]['latmax']]

   xres = (xmax - xmin) / float(rows)
   yres = (ymax - ymin) / float(cols)

   geotransform = (xmin, xres, 0, ymax, 0, -yres)

   ds.SetGeoTransform(geotransform)
   ss_band = ds.GetRasterBand(1)
   ss_band.WriteArray(datout) 
   ss_band.SetNoDataValue(-99)
   ss_band.FlushCache()
   ss_band.ComputeStatistics(False)
   del ds   


   #-----------------------------------------------------------
   proj = osr.SpatialReference()
   proj.ImportFromEPSG(4326) 
   datout = np.squeeze(np.ma.filled(prob))

   del prob

   datout[np.isnan(datout)] = -99
   driver = gdal.GetDriverByName('GTiff')
   cols,rows = np.shape(datout)    

   outFile = os.path.normpath(base+'gmm_prob_map.tif')
   ds = driver.Create( outFile, rows, cols, 1, gdal.GDT_Float32, [ 'COMPRESS=LZW' ] )        
   if proj is not None:  
     ds.SetProjection(proj.ExportToWkt()) 

   ds.SetGeoTransform(geotransform)
   ss_band = ds.GetRasterBand(1)
   ss_band.WriteArray(datout) 
   ss_band.SetNoDataValue(-99)
   ss_band.FlushCache()
   ss_band.ComputeStatistics(False)
   del ds  

