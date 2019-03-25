import time
from sklearn.model_selection import cross_val_predict
from sklearn.cross_validation import cross_val_predict
from imblearn.over_sampling import SMOTE
from sklearn import neighbors, metrics
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
df=pd.read_csv('glioma_raw_data_.csv')
dftrans=df.transpose()
dftrans['label']=0
dftrans['label'].iloc[0:18]=1
data=dftrans.iloc[:,0:20531]
label=dftrans['label']
test_percent=0.75
training_data, test_data, training_data_label, test_data_label = \
    train_test_split(data, label, test_size=test_percent, random_state=42)
#################################
######  KNN Classifier
#################################
kvalue=[3,5,10]
for k in kvalue:
    kNN = neighbors.KNeighborsClassifier(n_neighbors=k)
    kNN.fit(training_data, training_data_label)
    predicted = cross_val_predict(kNN, test_data, test_data_label, cv=5)
    print("with k value is:",k ,"the accuragy is :",metrics.accuracy_score(test_data_label, predicted))

###########################
#MLP Classifier part:
###########################
neuron_no= 15
hiddle_layer_no=10
#specifiy mlp's parameters
clf=MLPClassifier(alpha=1e-5,hidden_layer_sizes=(neuron_no,hiddle_layer_no),random_state=20)
clf2=clf.fit(training_data,training_data_label)# training
time.sleep(2)
predicted = cross_val_predict(clf2, test_data, test_data_label, cv=5)
print("the accuragy based on MLP before resampling is :",metrics.accuracy_score(test_data_label, predicted))
############################
# resampling:
############################
sm=SMOTE(ratio='auto',kind='regular')
X_resampled,y_resampled=sm.fit_sample(data,label)

training_data1, test_data1, training_data_label1, test_data_label1 = train_test_split(
    X_resampled, y_resampled,test_size=test_percent, random_state=42)

#################################
######  KNN Classifier
#################################
for k in kvalue:
    kNN = neighbors.KNeighborsClassifier(n_neighbors=k)
    kNN.fit(training_data1, training_data_label1)
    from sklearn.model_selection import cross_val_predict
    predicted = cross_val_predict(kNN, test_data1, test_data_label1, cv=5)
    print("with k value is:",k ,"the accuragy after oversampling is :",metrics.accuracy_score(test_data_label1, predicted))

###########################
#MLP Classifier part:
###########################

clf1=clf.fit(training_data1,training_data_label1)
time.sleep(2)
predicted1 = cross_val_predict(clf1, test_data1, test_data_label1, cv=5)
print("the accuragy based on MLP after oversampling is :",metrics.accuracy_score(test_data_label1, predicted1))
