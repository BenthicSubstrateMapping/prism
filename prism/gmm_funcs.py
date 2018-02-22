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
from sklearn import mixture
import numpy as np
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore",category=DeprecationWarning)
    from sklearn import cross_validation
from prism.common_funcs import get_X
##-------------------------------------------------------------

##-------------------------------------------------------------
def fit_GMM(img, Lc, test_size, covariance, tol):
   """
   This function ...
   """
   D, l = get_X(img, Lc)

   # split the data into training and testing portions based on 'test_size'
   X_train, X_test, y_train, y_test = cross_validation.train_test_split(D,l, test_size=test_size, random_state=42)

   print('Fitting GMM ...')
   # set up the gaussian mixture model
   g = mixture.GaussianMixture(n_components=len(np.unique(l)), max_iter=100, 
                            random_state=42, covariance_type=covariance, verbose=0, tol=tol) 

   # find per-label means
   tmp = [X_train[y_train == i].mean(axis=0) for i in range(len(np.unique(l)))]
   # initialize with means
   g.means_init =  np.array(tmp)
   # train model
   g.fit(X_train)

   return g

##-------------------------------------------------------------
def apply_GMM(g, img, prob_thres):
   """
   This function ...
   """
   print('Estimating substrates ...')
   if np.ndim(img)>2: #multispectral

      I = []
      for k in range(np.ndim(img)):
         I.append(img[:,:,k].flatten())

      y_prob = g.predict_proba(np.vstack(I).T).astype('float')

      YP = []
      for k in range(len(g.means_)):
         YP.append(y_prob[:,k].reshape(np.shape(img[:,:,0])))

      y_pred = np.argmax(y_prob, axis=1).astype('float')
      y_pred = y_pred.reshape(np.shape(img[:,:,0]))
      y_pred[img[:,:,0]==0] = np.nan

      y_pred_prob = np.max(y_prob, axis=1).astype('float')
      y_pred_prob = y_pred_prob.reshape(np.shape(img[:,:,0]))
      y_pred_prob[img[:,:,0]==0] = np.nan


   else: #monospectral
      y_prob = g.predict_proba(np.expand_dims(img[:,:].flatten(),1)).astype('float')

      YP = []
      for k in range(len(g.means_)):
         YP.append(y_prob[:,k].reshape(np.shape(img)))

      y_pred = np.argmax(y_prob, axis=1).astype('float')
      y_pred = y_pred.reshape(np.shape(img))
      y_pred[img==0] = np.nan

      y_pred_prob = np.max(y_prob, axis=1).astype('float')
      y_pred_prob = y_pred_prob.reshape(np.shape(img))
      y_pred_prob[img==0] = np.nan


   y_pred = y_pred+1
   y_pred[y_pred_prob<prob_thres] = 0

   #print('proportion unknown:')
   #print(np.sum(y_pred==0)/np.sum(~np.isnan(y_pred)))
   print('... GMM substrate estimation complete.')
   return y_pred, y_pred_prob, YP


