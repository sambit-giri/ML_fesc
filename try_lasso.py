import numpy as np
from sklearn.linear_model import LassoCV, Lasso
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

file_ir_a206     = 'CLASH_data/ABELL209/hlsp_clash_hst_ir_a209_cat.txt'
file_acs_ir_a206 = 'CLASH_data/ABELL209/hlsp_clash_hst_acs-ir_a209_cat.txt'

ir_a209     = np.loadtxt(file_ir_a206, skiprows=146)
acs_ir_a209 = np.loadtxt(file_acs_ir_a206, skiprows=146)

stellarity_thres = 0.5
data = np.zeros((1,ir_a209.shape[1]))
for i in xrange(ir_a209.shape[1]):
	if ir_a209[i,7] < stellarity_thres: data = np.vstack((data, ir_a209[i,:]))
data = np.delete(data, 0, 0)

mag_abs_index = np.array([14,20,26,36,38,44,50,56,62,68,74,80,86,92,98,104,110]) - 1
zb_index = 115


X = np.zeros((data.shape[0],1))
for i in xrange(mag_abs_index.shape[0]):
	X = np.hstack((X, data[:,mag_abs_index[i]].reshape(data.shape[0],1)))
X = np.delete(X, 0, 1)
y = data[:,zb_index]

X_train, X_test, y_train, y_test = train_test_split(X, y)

clf = Lasso(alpha=0.1)
clf.fit(X_train,y_train)

y_pred = clf.predict(X_test)

#plt.plot(y_test, y_pred)
acc_score = accuracy_score(np.round(y_test*1000), np.round(y_pred*1000))



