from sklearn.datasets import load_iris
from sklearn import tree


iris = load_iris()
print('iris.data :\n', iris.data)
print('iris.target :\n', iris.target)
clf = tree.DecisionTreeClassifier(max_depth=3)
clf = clf.fit(iris.data, iris.target)
predicted = clf.predict(iris.data)
print('target :\n', predicted)
