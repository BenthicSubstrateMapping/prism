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
import pydensecrf.densecrf as dcrf
from pydensecrf.utils import create_pairwise_gaussian, create_pairwise_bilateral, unary_from_labels
from scipy.stats import mode as md
##-------------------------------------------------------------

##-------------------------------------------------------------
def set_unary_from_labels(fp, lp, prob, labels):
   """
   This function ...
   """
   H = fp.shape[0]
   W = fp.shape[1]

   d = dcrf.DenseCRF2D(H, W, len(labels)) # +1)
   U = unary_from_labels(lp.astype('int'), len(labels), gt_prob= prob)

   d.setUnaryEnergy(U)

   return d, H, W

##-------------------------------------------------------------
def set_feats_both(d, fp, scol, compat_col, sspat, compat_spat):
   """
   This function ...
   """

   d = set_feats_spat(d, sspat, compat_spat, mode)
   d = set_feats_col(fp, d, scol, compat_col)

   return d

##-------------------------------------------------------------
def set_feats_spat(d, sspat, compat_spat):
   """
   This function ...
   """

   d.addPairwiseGaussian(sxy=sspat, compat=compat_spat)

   return d

##-------------------------------------------------------------
def set_feats_col(fp, d, scol, compat_col):
   """
   This function ...
   """

   scale = 1

   if np.ndim(fp)==2:

      feats = create_pairwise_bilateral(sdims=(scol, scol), schan=(scale, scale, scale),
                                  img=np.dstack((fp,fp,fp)), chdim=2)

   else:
      feats = create_pairwise_bilateral(sdims=(scol, scol), schan=(scale, scale, scale),
                                  img=fp, chdim=2)

   d.addPairwiseEnergy(feats, compat=compat_col,
                    kernel=dcrf.DIAG_KERNEL,
                    normalization=dcrf.NORMALIZE_SYMMETRIC)

   return d


##-------------------------------------------------------------
def inference(d, n_iter, H, W, labels):
   """
   This function ...
   """
   R = [] ; 
   Q, tmp1, tmp2 = d.startInference()
   for k in range(n_iter):
      print('Iteration: %i' % k)
      d.stepInference(Q, tmp1, tmp2)
      R.append(np.argmax(Q, axis=0).reshape((H, W)))

   R = list(R)

   l, cnt = md(np.asarray(R, dtype='uint8'),axis=0)

   l = np.squeeze(l)
   cnt = np.squeeze(cnt)
   p = cnt/len(R)

   del l, cnt

   preds = np.array(Q, dtype=np.float32).reshape((len(labels), H, W)).transpose(1, 2, 0) ##labels+1

   return np.argmax(Q, axis=0).reshape((H, W)), p, np.squeeze(np.expand_dims(preds, 0))


##-------------------------------------------------------------
def apply_CRF(fp, lp, labels, n_iter, prob_thres, scol, compat_col):
   """
   This function ...
   """

   prob = 0.51 # initial probability of unary labels
   d, H, W = set_unary_from_labels(fp, lp, prob, labels)

   d = set_feats_col(fp, d, scol, compat_col)

   print('Estimating substrates ...')
   res, p1, p2 = inference(d, n_iter, H, W, labels)

   if np.ndim(fp)==2:
      p1[fp==0] = np.nan 
      p2[fp==0] = np.nan 
   else:
      p1[fp[:,:,0]==0] = np.nan 
      p2[fp[:,:,0]==0] = np.nan 

   res = res.astype('float')

   res = 1+res.copy()
   res[np.isnan(res)] = 0
   res[p1<prob_thres] = 0
   res[np.isinf(res)] = np.nan

   if np.ndim(fp)==2:
      res[fp==0] = np.nan 
   else:
      res[fp[:,:,0]==0] = np.nan 

   print('... CRF substrate estimation complete.')

   return res, p1, p2



