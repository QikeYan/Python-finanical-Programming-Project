from imblearn.over_sampling import SMOTE
from sklearn import neighbors, metrics
from sklearn.cross_validation import cross_val_score
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.neural_network import MLPClassifier

df=pd.read_csv('breast_rpkm_normalization_data_.csv')
dftrans=df.transpose()
dftrans['label']=0
dftrans['label'].iloc[775:875]=1
data=dftrans.iloc[:,0:25103]
label=dftrans['label']
test_percent=0.4
#################################
######  KNN Classifier
#################################
training_data, test_data, training_data_label, test_data_label = train_test_split(data, label,
                                                test_size=test_percent, random_state=42)
kvalue=[3,5,10]
for k in kvalue:
    kNN = neighbors.KNeighborsClassifier(n_neighbors=k)
    kNN.fit(training_data, training_data_label)
    predicted = cross_val_predict(kNN, test_data, test_data_label, cv=5)
    print("with k value is:",k ,"the accuragy is :",metrics.accuracy_score(test_data_label, predicted))
#########################
# resampling:
#########################
sm=SMOTE(ratio='auto',kind='regular')
X_resampled,y_resampled=sm.fit_sample(data,label)

training_data1, test_data1, training_data_label1, test_data_label1 = train_test_split(
    X_resampled, y_resampled,test_size=test_percent, random_state=42)

for k in kvalue:
    kNN = neighbors.KNeighborsClassifier(n_neighbors=k)
    kNN.fit(training_data1, training_data_label1)
    from sklearn.model_selection import cross_val_predict
    predicted = cross_val_predict(kNN, test_data1, test_data_label1, cv=5)
    print("with k value is:",k ,"the accuragy after oversampling is :",metrics.accuracy_score(test_data_label1, predicted))

########################
##MLP Classifier part:
########################
neuron_no= 15
hiddle_layer_no=10
#specifiy mlp's parameters
clf=MLPClassifier(alpha=1e-5,hidden_layer_sizes=(neuron_no,hiddle_layer_no),random_state=20)
clf1=clf.fit(training_data,training_data_label)# training
clf2=clf.fit(training_data1,training_data_label1)
predicted1 = cross_val_predict(clf1, test_data, test_data_label, cv=5)
print("the accuragy based on MLP before resampling is :",metrics.accuracy_score(test_data_label, predicted1))

predicted2 = cross_val_predict(clf2, test_data1, test_data_label1, cv=5)
print("the accuragy based on MLP after oversampling is :",metrics.accuracy_score(test_data_label1, predicted2))


