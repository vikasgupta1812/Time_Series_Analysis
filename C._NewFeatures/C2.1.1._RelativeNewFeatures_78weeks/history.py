# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

#get variables
import ipykee
keeper = ipykee.Keeper("C._NewFeatures")
session = keeper["C2.1.1._RelativeNewFeatures_78weeks"]
vars_c21 = session.get_variables("master")
variables.keys()

# <codecell>

#get variables
import ipykee
keeper = ipykee.Keeper("C._NewFeatures")
session = keeper["C2.1.1._RelativeNewFeatures_78weeks"]
vars_c21 = session.get_variables("master")
#variables.keys()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = non_nan_res['Error_test'].values
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv('ann_res.csv')
results.columns

# <codecell>

non_nan_res = results[pd.isnull(results).sum(axis=1)==0]

# <codecell>

#%%px
%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Load original data
data = pd.read_csv('popularity-728days_my.csv')

head = list(data.columns[:21]) + range(1,105)
data = pd.DataFrame(columns=head, data=data.values)

# <codecell>

#%%px
#Select data
selection = ((data['Now'] - data['Creation-week']) > 26)&((data['Now'] - data['FirstUsage']) > 26)&((data[78] - data[1]) != 0)
data_sel = data[selection].copy()
#data_sel = data.copy()
print data_sel.shape

# <codecell>

#%%px
periods = range(1,105)

#------------------------------------------------------
#Get maximum intervals and last weeks with zeros usages
def InterMax(data_sel, periods):
    #Get binary vector representation of the selected data
    data_bv = data_sel.copy()
    #Get week's usages
    for i in periods:
        if i!=1:
            data_bv[i] = data_sel[i] - data_sel[i-1]
            
    #Get binary representation
    data_bv[periods] = (data_bv[periods] != 0)*1
    
    inter_max = []
    last_zeros = []
    nb_peaks = []
    inter_mean = []
    inter_std = []
    inter_rel = []
    
    for i in range(0,data_bv.shape[0]):
        ds = data_bv[periods].irow(i)
        nz = ds.nonzero()[0]
        inter = []
        
        nb_peaks.append(len(nz))
        if len(nz)==0:
            nz = [0]
        if len(nz)<2:
            inter = [0]
            #nz = [0]
        else:
            for k in range(0, len(nz)-1):
                val = nz[k+1]-nz[k]
                inter.append(val)
        
        inter = np.array(inter)
        inter_mean.append(inter.mean())
        inter_std.append(inter.std())
        if inter.mean()!=0:
            inter_rel.append(inter.std()/inter.mean())
        else:
            inter_rel.append(0)
                
        last_zeros.append(periods[-1] - nz[-1] + 1)
        inter_max.append(max(inter))
    
    return np.array(inter_max), np.array(last_zeros), np.array(nb_peaks), np.array(inter_mean), np.array(inter_std), np.array(inter_rel)

# <codecell>

#%%px
#Add features
inter_max, last_zeros, nb_peaks, inter_mean, inter_std, inter_rel = InterMax(data_sel, periods)
data_sel['last-zeros'] = last_zeros
data_sel['inter_max'] = inter_max
data_sel['nb_peaks'] = nb_peaks
data_sel['inter_mean'] = inter_mean
data_sel['inter_std'] = inter_std
data_sel['inter_rel'] = inter_rel

# <codecell>

#%%px
data = data_sel[data_sel['nb_peaks']>=0]

# <codecell>

#%%px
data_weeks = data[range(1,105)]

# <codecell>

#%%px
df_time_series = data_weeks.copy()
for i in range(1,105):
    if i!=1:
        df_time_series[i] = data_weeks[i]-data_weeks[i-1]

# <codecell>

#%%px
param1 = 13
df_ts_rolling_sum = pd.rolling_sum(df_time_series, window=param1,axis=1)[range(param1,105)]

# <codecell>

#%%px
ws = 13#window_size
fh = 13#forecast horizont
param2 = 105-param1

def N_M_Transformation(time_serie, ws, fh):
    x_cols = ['x'+str(i) for i in range(1,ws+1)]#columns names
    time_serie_table = pd.DataFrame(columns=x_cols+['y'])
    time_serie_4predict = pd.DataFrame(columns=x_cols)
    #Data for train and test
    for row_num in range(0, param2-fh-ws):
        time_serie_table.loc[row_num] = list(time_serie.icol(range(row_num+1, row_num+ws+1)).values[0])\
        +list(time_serie.icol([row_num+ws+fh]).values[0])#y variable 
    #Data for prediction
    for row_num in range(param2-fh-ws,param2-ws):
        time_serie_4predict.loc[row_num-(param2-fh-ws)] = list(time_serie.icol(range(row_num+1, row_num+ws+1)).values[0]) 
        #print row_num

    return time_serie_table, time_serie_4predict

# <codecell>

#%%px
param3 = param2-fh-ws
print param3

# <codecell>

# %%px
# results = pd.DataFrame(columns=["Index","Error_train","Error_valid", "Error_test"]+range(0,param3))
# results.to_csv('/mnt/w76/notebook/datasets/mikhail/ann_res.csv')

# <codecell>

%matplotlib inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

results = pd.read_csv('ann_res.csv')
results.columns

# <codecell>

non_nan_res = results[pd.isnull(results).sum(axis=1)==0]

# <codecell>

#print error hists
figure(figsize=(15, 5))
subplot(121)
plt.hist(non_nan_res['Error_test'].values, color='r', bins=20, label='test', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_train'].values, color='b', bins=20, label='train', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_valid'].values, color='g', bins=20, label='valid', alpha=1, histtype='step')
plt.title('Errors')
plt.legend(loc='best')
#plt.show()

#print predict value for the last point
subplot(122)
plt.hist(non_nan_res['66'].values, bins=50, label='last point')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[-1]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0')
plt.hist(values[y_last!=0], bins=50, label='y_last!=0')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_test'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = non_nan_res['Error_test'].values
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = non_nan_res['Error_valid'].values
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+1.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+0.99)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+0.09)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0')
plt.hist(values[y_last!=0], bins=50, label='y_last!=0')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

#get variables
import ipykee
keeper = ipykee.Keeper("C._NewFeatures")
session = keeper["C2.1.1._RelativeNewFeatures_78weeks"]
vars_c21 = session.get_variables("master")
#variables.keys()

# <codecell>

# #get variables
# import ipykee
# keeper = ipykee.Keeper("C._NewFeatures")
# session = keeper["C2.1.1._RelativeNewFeatures_78weeks"]
# vars_c21 = session.get_variables("master")
# #variables.keys()

# <codecell>

import ipykee
#ipykee.create_project(project_name="D._UsageForecast", repository="git@github.com:hushchyn-mikhail/CERN_Time_Series.git")
session = ipykee.Session(project_name="D._UsageForecast")

# <codecell>

session.commit("ANN of Neurolab. Trained, predicted. Some results are shown.")

# <codecell>

#get variables
import ipykee
keeper = ipykee.Keeper("C._NewFeatures")
session = keeper["C2.1.1._RelativeNewFeatures_78weeks"]
vars_c21 = session.get_variables("master")
#variables.keys()

# <codecell>

#get variables
# import ipykee
# keeper = ipykee.Keeper("C._NewFeatures")
# session = keeper["C2.1.1._RelativeNewFeatures_78weeks"]
# vars_c21 = session.get_variables("master")
#variables.keys()

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0)*(results['Error_train']<0.1)]

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0) and (results['Error_train']<0.1)]

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0)*(results['Error_train']<0.1)]

# <codecell>

#print error hists
figure(figsize=(15, 5))
subplot(121)
plt.hist(non_nan_res['Error_test'].values, color='r', bins=20, label='test', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_train'].values, color='b', bins=20, label='train', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_valid'].values, color='g', bins=20, label='valid', alpha=1, histtype='step')
plt.title('Errors')
plt.legend(loc='best')
#plt.show()

#print predict value for the last point
subplot(122)
plt.hist(non_nan_res['66'].values, bins=50, label='last point')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[-1]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0')
plt.hist(values[y_last!=0], bins=50, label='y_last!=0')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=0.5)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=0.5)
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0)*(results['Error_valid']<0.1)]

# <codecell>

#print error hists
figure(figsize=(15, 5))
subplot(121)
plt.hist(non_nan_res['Error_test'].values, color='r', bins=20, label='test', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_train'].values, color='b', bins=20, label='train', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_valid'].values, color='g', bins=20, label='valid', alpha=1, histtype='step')
plt.title('Errors')
plt.legend(loc='best')
#plt.show()

#print predict value for the last point
subplot(122)
plt.hist(non_nan_res['66'].values, bins=50, label='last point')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[-1]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0)*(results['Error_test']<0.1)]

# <codecell>

#print error hists
figure(figsize=(15, 5))
subplot(121)
plt.hist(non_nan_res['Error_test'].values, color='r', bins=20, label='test', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_train'].values, color='b', bins=20, label='train', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_valid'].values, color='g', bins=20, label='valid', alpha=1, histtype='step')
plt.title('Errors')
plt.legend(loc='best')
#plt.show()

#print predict value for the last point
subplot(122)
plt.hist(non_nan_res['66'].values, bins=50, label='last point')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[-1]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0)*(results['Error_valid']<0.1)*(results['Error_train']<0.1)]

# <codecell>

#print error hists
figure(figsize=(15, 5))
subplot(121)
plt.hist(non_nan_res['Error_test'].values, color='r', bins=20, label='test', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_train'].values, color='b', bins=20, label='train', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_valid'].values, color='g', bins=20, label='valid', alpha=1, histtype='step')
plt.title('Errors')
plt.legend(loc='best')
#plt.show()

#print predict value for the last point
subplot(122)
plt.hist(non_nan_res['66'].values, bins=50, label='last point')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[-1]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0)*(results['Error_valid']<0.3)*(results['Error_train']<0.3)]

# <codecell>

#print error hists
figure(figsize=(15, 5))
subplot(121)
plt.hist(non_nan_res['Error_test'].values, color='r', bins=20, label='test', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_train'].values, color='b', bins=20, label='train', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_valid'].values, color='g', bins=20, label='valid', alpha=1, histtype='step')
plt.title('Errors')
plt.legend(loc='best')
#plt.show()

#print predict value for the last point
subplot(122)
plt.hist(non_nan_res['66'].values, bins=50, label='last point')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[-1]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
y_score = (1.0 + non_nan_res['66'].values)/2.0
#y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0)*(results['Error_valid']<0.2)*(results['Error_train']<0.2)]

# <codecell>

#print error hists
figure(figsize=(15, 5))
subplot(121)
plt.hist(non_nan_res['Error_test'].values, color='r', bins=20, label='test', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_train'].values, color='b', bins=20, label='train', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_valid'].values, color='g', bins=20, label='valid', alpha=1, histtype='step')
plt.title('Errors')
plt.legend(loc='best')
#plt.show()

#print predict value for the last point
subplot(122)
plt.hist(non_nan_res['66'].values, bins=50, label='last point')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[-1]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0)*(results['Error_valid']<0.02)*(results['Error_train']<0.02)]

# <codecell>

#print error hists
figure(figsize=(15, 5))
subplot(121)
plt.hist(non_nan_res['Error_test'].values, color='r', bins=20, label='test', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_train'].values, color='b', bins=20, label='train', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_valid'].values, color='g', bins=20, label='valid', alpha=1, histtype='step')
plt.title('Errors')
plt.legend(loc='best')
#plt.show()

#print predict value for the last point
subplot(122)
plt.hist(non_nan_res['66'].values, bins=50, label='last point')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[-1]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

non_nan_res = results[(pd.isnull(results).sum(axis=1)==0)*(results['Error_valid']<=1)*(results['Error_train']<=1)]

# <codecell>

#print error hists
figure(figsize=(15, 5))
subplot(121)
plt.hist(non_nan_res['Error_test'].values, color='r', bins=20, label='test', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_train'].values, color='b', bins=20, label='train', alpha=1, histtype='step')
plt.hist(non_nan_res['Error_valid'].values, color='g', bins=20, label='valid', alpha=1, histtype='step')
plt.title('Errors')
plt.legend(loc='best')
#plt.show()

#print predict value for the last point
subplot(122)
plt.hist(non_nan_res['66'].values, bins=50, label='last point')
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[-1]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[104]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

y_last=[]
for i in non_nan_res['Index']:
    i=int(i)
    cur_serie = df_ts_rolling_sum.xs(i).values
    y_last.append(cur_serie[104-fh]/(1.0*cur_serie.max()))
y_last = np.array(y_last)

# <codecell>

figure(figsize=(15, 10))
#print predict value for the last point
subplot(2,2,1)
values = non_nan_res['66'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Predict values')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,2)
values = non_nan_res['Error_test'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_test')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,3)
values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Relative test error')
plt.legend(loc='best')
#plt.show()

#print predict value for 66th week
subplot(2,2,4)
values = non_nan_res['Error_valid'].values
plt.hist(values[y_last==0], bins=50, label='y_last=0', alpha=1)
plt.hist(values[y_last!=0], bins=50, label='y_last!=0', alpha=1)
plt.title('Error_valid')
plt.legend(loc='best')
#plt.show()

# <codecell>

from sklearn.metrics import roc_curve, auc

y_true = (y_last>0)*1
#y_score = (1.0 + non_nan_res['66'].values)/2.0
y_score = values = non_nan_res['Error_valid'].values/(non_nan_res['66'].values+2.0)
fpr, tpr, _ = roc_curve(y_true, y_score, pos_label=None, sample_weight=None)
roc_auc = auc(fpr, tpr)

figure(figsize=(15, 5))
subplot(1,2,1)
plt.plot(fpr, tpr)
plt.title('ROC curve')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
print 'ROC AUC is ', roc_auc

# <codecell>

test_cols = [str(i) for i in range(54,67)]
all_cols = [str(i) for i in range(0,67)]
for row in range(0,30):
    subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]))
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum.xs(index))

# <codecell>

test_cols = [str(i) for i in range(54,67)]
all_cols = [str(i) for i in range(0,67)]
for row in range(0,30):
    subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]), color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum.xs(index))

# <codecell>

test_cols = [str(i) for i in range(54,67)]
all_cols = [str(i) for i in range(0,67)]
for row in range(0,30):
    subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]), color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum.xs(index), color='r')
    plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
all_cols = [str(i) for i in range(0,67)]
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]), color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum.xs(index), color='r')
    plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
all_cols = [str(i) for i in range(0,67)]
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]), color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    #plt.plot(df_ts_rolling_sum.xs(index), color='r')
    plt.show()

# <codecell>

non_nan_res

# <codecell>

non_nan_res.irow([1])

# <codecell>

test_cols = [str(i) for i in range(54,67)]
all_cols = [str(i) for i in range(0,67)]
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row].values), color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    #plt.plot(df_ts_rolling_sum.xs(index), color='r')
    plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
all_cols = [str(i) for i in range(0,67)]
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]).values, color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    #plt.plot(df_ts_rolling_sum.xs(index), color='r')
    plt.show()

# <codecell>

non_nan_res.irow([1]).values

# <codecell>

non_nan_res.irow([1]).values[0]

# <codecell>

test_cols = [str(i) for i in range(54,67)]
all_cols = [str(i) for i in range(0,67)]
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]).values[0], color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    #plt.plot(df_ts_rolling_sum.xs(index), color='r')
    plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
all_cols = [str(i) for i in range(0,67)]
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]).values[0], color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum.xs(index), color='r')
    plt.show()

# <codecell>

df_ts_rolling_sum

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = [str(i) for i in range(39,105)]
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]).values[0], color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum.xs(index), color='r')
    plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = [str(i) for i in range(39,105)]
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]).values[0], color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum[cols].xs(index), color='r')
    plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(39,105)
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]).values[0], color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum[cols].xs(index), color='r')
    plt.show()

# <codecell>

df_ts_rolling_sum.max()

# <codecell>

df_ts_rolling_sum.max(axis=1)

# <codecell>

df_ts_rolling_sum/df_ts_rolling_sum.max(axis=1)

# <codecell>

df_ts_rolling_sum/df_ts_rolling_sum.max(axis=1).values

# <codecell>

df_ts_rolling_sum.values/df_ts_rolling_sum.max(axis=1).values

# <codecell>

max_values = df_ts_rolling_sum.max(axis=1)
max_values

# <codecell>

max_values = df_ts_rolling_sum.max(axis=1)
column = df_ts_rolling_sum[1]

# <codecell>

df_ts_rolling_sum

# <codecell>

df_ts_rolling_sum.columns

# <codecell>

max_values = df_ts_rolling_sum.max(axis=1)
column = df_ts_rolling_sum[13]

# <codecell>

max_values = df_ts_rolling_sum.max(axis=1)
column = df_ts_rolling_sum[13]
column

# <codecell>

max_values = df_ts_rolling_sum.max(axis=1)
column = df_ts_rolling_sum[13]
a = column/max_values
a

# <codecell>

max_values = df_ts_rolling_sum.max(axis=1)
df_ts_rolling_sum_std = df_ts_rolling_sum.copy()
for col in df_ts_rolling_sum.columns:
    df_ts_rolling_sum_std[col] = df_ts_rolling_sum[col]/max_values
    
df_ts_rolling_sum_std

# <codecell>

max_values = df_ts_rolling_sum.max(axis=1)
df_ts_rolling_sum_std = df_ts_rolling_sum.copy()
for col in df_ts_rolling_sum.columns:
    df_ts_rolling_sum_std[col] = df_ts_rolling_sum[col]/max_values

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(39,105)
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]).values[0], color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='r')
    plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(104-66,105)
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]).values[0], color='b')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='r')
    plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(104-66,105)
for row in range(0,30):
    plt.subplot(1,1,1)
    plt.plot(non_nan_res.irow([row]).values[0], color='b', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='r', label='real')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    plt.show()

# <codecell>

print 5/2

# <codecell>

print 5//2

# <codecell>

print 5%2

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(104-66,105)
a=0
b=30
N=b-a
for row in range(a,b):
    plt.subplot(N%3+1,3,row)
    plt.plot(non_nan_res.irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(104-66,105)
a=0
b=30
N=b-a
for row in range(a,b):
    subplot(N%3+1,3,row)
    plt.plot(non_nan_res.irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(104-66,105)
a=0
b=30
N=b-a
figure(figsize=(15, 50))
for row in range(a,b):
    subplot(N%3+1,3,row)
    plt.plot(non_nan_res.irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

print N

# <codecell>

print N%3

# <codecell>

print N%3.

# <codecell>

print N//3

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(104-66,105)
a=0
b=30
N=b-a
figure(figsize=(15, 50))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res.irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(104-66,105)
a=0
b=30
N=b-a
figure(figsize=(15, 58(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res.irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

test_cols = [str(i) for i in range(54,67)]
cols = range(104-66,105)
a=0
b=30
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res.irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(104-66,105)
a=0
b=30
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=30
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=30
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.plot([param3-fh,param3-fh], [0,1], color='d')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=3
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.plot([param3-fh,param3-fh], [0,1], color='b')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=3
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.plot([param3-fh,param3-fh], [-1,1], color='b')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=3
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.plot([param3-fh,param3-fh], [-1,1], color='bl')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=3
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.plot([param3-fh,param3-fh], [-1,1], color='black')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=100
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.plot([param3-fh,param3-fh], [-1,1], color='black')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=30
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.plot([param3-fh,param3-fh], [-1,1], color='black')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=60
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.plot([param3-fh,param3-fh], [-1,1], color='black')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

# <codecell>

val_cols = [str(i) for i in range(1,67)]
cols = range(105-66,105)
a=0
b=60
N=b-a
figure(figsize=(15, 5*(N//3+1)))
for row in range(a,b):
    subplot(N//3+1,3,row)
    plt.plot(non_nan_res[val_cols].irow([row]).values[0], color='r', label='predict')
    index = int(non_nan_res.irow([row])['Index'].values)
    plt.plot(df_ts_rolling_sum_std[cols].xs(index), color='b', label='real')
    plt.plot([param3-fh,param3-fh], [-1,1], color='black')
    plt.plot([param3-fh-10,param3-fh-10], [-1,1], color='black')
    plt.title('Index is '+str(index))
    plt.legend(loc='best')
    #plt.show()

