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
import numpy as np

##-------------------------------------------------------------
def get_X(img, Lc):
   """
   This function ...
   """
   D = []
   counter = 0
   for item in np.unique(Lc)[1:]:
      ind = np.where(Lc.flatten()==item)[0]
      B=[]
      if np.ndim(img)>2:
         for k in range(np.ndim(img)):
            B.append(img[:,:,k].flatten()[ind])
      else:
         B.append(img[:,:].flatten()[ind])

      D.append( np.vstack(( np.vstack(B), np.ones(len(B[0]))*counter )).T )
      counter += 1

   Dr = np.concatenate(D)
   Dr[np.isinf(Dr)] = 0

   D = Dr[:,:np.shape(Dr)[1]-1]
   l = Dr[:,np.shape(Dr)[1]-1:]
   l = np.squeeze(l)
   return D, l

##-------------------------------------------------------------
def get_sparse_labels(bs, bed, buff):
   """
   This function ...
   """
   ## make sparse labels
   Lc = np.zeros(np.shape(bs[0]['bs']))+99
   nx, ny = np.shape(Lc)
   for k in range(len(bed['Xproj'])): 
      try:
         y = (1/bs[0]['gridres']*np.ceil(bed['Xproj'][k] - bs[0]['xmin'])).astype('int')
         x = (1/bs[0]['gridres']*np.ceil(bs[0]['ymax'] - bed['Yproj'][k])).astype('int')
         Lc[np.max([0,x-buff]):np.min([nx,x+buff]), np.max([0,y-buff]):np.min([ny,y+buff])] = np.ones((buff*2, buff*2))*bed['Ccodes'][k]
      except:
         pass

   Lc += 1
   Lc[bs[0]['bs']==0] = 100

   Lc -= 1
   Lc[Lc==99] = 0 #100

   return Lc.astype('uint8')

