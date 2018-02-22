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
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix
import itertools
import os
##-------------------------------------------------------------

##-------------------------------------------------------------
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          cmap=plt.cm.Blues,
                          dolabels=True):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        cm[np.isnan(cm)] = 0

    plt.imshow(cm, interpolation='nearest', cmap=cmap, vmax=1, vmin=0)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    if dolabels==True:
       tick_marks = np.arange(len(classes))
       plt.xticks(tick_marks, classes, rotation=45, fontsize=6) # 
       plt.yticks(tick_marks, classes, fontsize=6)

       plt.ylabel('True label',fontsize=6)
       plt.xlabel('Estimated label',fontsize=6)

    else:
       plt.axis('off')

    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if cm[i, j]>.05:
           plt.text(j, i, format(cm[i, j], fmt),
                 fontsize=5,
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()

    return cm


##-------------------------------------------------------------
def plot_confmatGMM(y_pred, Lc, bed, prefix):
   """
   This function ...
   """

   base = '..'+os.sep+'outputs'+os.sep+prefix+'_'

   y = y_pred.copy()
   del y_pred
   l = Lc.copy()
   del Lc

   l = l.astype('float')
   l[l==0] = np.nan

   y[np.isnan(l)] = np.nan

   ytrue = l.flatten()
   ypred = y.flatten()

   ytrue = ytrue[~np.isnan(ytrue)]
   ypred = ypred[~np.isnan(ypred)]

   cm = confusion_matrix(ytrue, ypred)

   cm = cm / cm.sum(axis=1)[:, np.newaxis]
   cm[np.isnan(cm)] = 0

   cm2 = cm[1:,1:]
   cm2 = cm2 / cm2.sum(axis=1)[:, np.newaxis]

   fig=plt.figure()
   plt.subplot(221)
   plot_confusion_matrix(cm, classes=bed['labels'], normalize=True)
   plt.title('A', loc='left', fontsize=6)

   ax1=plt.subplot(222)
   plot_confusion_matrix(cm2, classes=bed['labels'][1:], normalize=True)
   plt.title('B', loc='left', fontsize=6)

   plt.savefig(base+'GMM_confusion_matrix.png', dpi=300, bbox_inches='tight') 
   #plt.close()
   #del fig

##-------------------------------------------------------------
def plot_confmatCRF(y_pred, Lc, bed, prefix):
   """
   This function ...
   """

   base = '..'+os.sep+'outputs'+os.sep+prefix+'_'

   y = y_pred.copy()
   del y_pred
   l = Lc.copy()
   del Lc

   l = l.astype('float')
   l[l==0] = np.nan

   y[np.isnan(l)] = np.nan

   ytrue = l.flatten()
   ypred = y.flatten()

   ytrue = ytrue[~np.isnan(ytrue)]
   ypred = ypred[~np.isnan(ypred)]

   cm = confusion_matrix(ytrue, ypred)

   cm = cm / cm.sum(axis=1)[:, np.newaxis]
   cm[np.isnan(cm)] = 0

   cm2 = cm[1:,1:]
   cm2 = cm2 / cm2.sum(axis=1)[:, np.newaxis]

   fig=plt.figure()
   plt.subplot(221)
   plot_confusion_matrix(cm, classes=bed['labels'], normalize=True)
   plt.title('A', loc='left', fontsize=6)

   ax1=plt.subplot(222)
   plot_confusion_matrix(cm2, classes=bed['labels'][1:], normalize=True)
   plt.title('B', loc='left', fontsize=6)

   plt.savefig(base+'CRF_confusion_matrix.png', dpi=300, bbox_inches='tight') 
   #plt.close()
   #del fig


