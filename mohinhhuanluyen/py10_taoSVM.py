
from py4_docfiledulieu import get_data_train_nhan_tsv,get_data_train_vecto_csv

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split, GridSearchCV



def model_svm():
  data_vecto = get_data_train_vecto_csv("data_train_vecto_VN.csv")
  data_nhan =  get_data_train_nhan_tsv("data_train_nhan.tsv")
  #  param_grid = {
  #               # 'kernel': ['linear', 'poly', 'rbf', 'sigmoid'],
  #               # 'C': [0.1, 1, 10, 100],
  #               # 'gamma': ['scale', 'auto'],
  #               # 'degree': [2, 3, 4],
  #               # 'coef0': [0.0, 0.1, 0.5],
  #               # 'class_weight': [None, 'balanced']
  #               'probability': [True, False],
  #               'shrinking': [True, False],
  #               'decision_function_shape': ['ovo', 'ovr']
  #               }
  X_train, X_test, Y_train, Y_test = train_test_split(data_vecto, data_nhan,test_size=0.2, random_state=42)
  svm_model = SVC(kernel='linear', C=10, gamma='scale', degree=2, class_weight=None, coef0=0.1, probability=False, shrinking=True, decision_function_shape='ovr' )
  # grid_search = GridSearchCV(estimator=svm_model, param_grid=param_grid, cv=5, scoring='accuracy')
  svm_model.fit(X_train, Y_train)

  # print("Best Parameters:", grid_search.best_params_)
  # best_model = grid_search.best_estimator
  return svm_model
