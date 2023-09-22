import pandas as pd
from imblearn.under_sampling import NearMiss
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

#---------------Preprocess Data------------------------------------------------
dataset = pd.read_csv('Strokesdataset_Harvard.csv')
dataset = dataset.drop('id',axis = 1)
DataPrep = dataset.dropna()
Cols = ['gender','ever_married','work_type','Residence_type','smoking_status']
Columns = ['gender','age','hypertension','heart_disease','ever_married','work_type','Residence_type','avg_glucose_level','bmi''smoking_status','stroke']
DataPrep[Cols] = DataPrep[Cols].astype('category')
for Columns in Cols:
   DataPrep[Columns] = DataPrep[Columns].cat.codes
   
DataPrep = pd.DataFrame(scaler.fit_transform(DataPrep), columns=DataPrep.columns)

X = DataPrep.drop('stroke',axis = 1)
Y = DataPrep['stroke'] # select only the stroke

nm = NearMiss()
X_res, Y_res =nm.fit_resample(X,Y)

x1_train, x1_test, y1_train, y1_test = train_test_split(X_res,Y_res, test_size=0.2,random_state =1234, stratify= Y_res)
x2_train, x2_test, y2_train, y2_test = train_test_split(X_res,Y_res, test_size=0.2,random_state =1234, stratify= Y_res)
x3_train, x3_test, y3_train, y3_test = train_test_split(X_res,Y_res, test_size=0.2,random_state =2135, stratify= Y_res)

dtree = DecisionTreeClassifier(random_state = 1234)
dtree.fit(x1_train, y1_train)
y_dtree_predict = dtree.predict(x1_test)

rfc = RandomForestClassifier(n_estimators= 200,random_state = 1234)
rfc.fit(x2_train, y2_train)
y_rfc_predict = rfc.predict(x2_test)

lr = LogisticRegression()
lr.fit(x3_train, y3_train)
y_lr_predict = lr.predict(x3_test)

cr_dtree = classification_report(y1_test, y_dtree_predict)
cr_rfc = classification_report(y2_test, y_rfc_predict)
cr_lr = classification_report(y3_test, y_lr_predict)

cm_dtree = confusion_matrix(y1_test, y_dtree_predict)
cm_rfc = confusion_matrix(y2_test, y_rfc_predict)
cm_lr = confusion_matrix(y3_test, y_lr_predict)

#print(classification_report(y1_test, y_dtree_predict))
#print(classification_report(y2_test, y_rfc_predict))
#print(classification_report(y3_test, y_lr_predict))
#print("----------------------------------------------------------------------------------------")
#new_data = pd.DataFrame([[0.5,0.7916666666666665,0.0,0.0,1.0,0.5,1.0,0.23584985595661753,0.18315018315018317,0.0]],
#        columns=['gender','age','hypertension','heart_disease','ever_married','work_type','Residence_type','avg_glucose_level','bmi','smoking_status' ])
#print(dtree.predict(new_data))
#print(rfc.predict(new_data))
#print(lr.predict(new_data))

#print("'gender','age','hypertension','heart_disease','ever_married','work_type',")
#print("'Residence_type','avg_glucose_level','bmi','smoking_status'")
#print(lr.coef_)
#print(dtree.feature_importances_)
#print(rfc.feature_importances_)
