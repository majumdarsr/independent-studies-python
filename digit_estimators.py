"""
This program uses MNIST dataset taken from this website:
http://yann.lecun.com/exdb/mnist/

Handwritten digits are provided as 28 X 28 pixel images, along with their labels.

mnistData_loader loads the data as training data, training labels, test data and test labels.

There are 60,000 training data and and 10,000 test data images. 

The data features are individual pixels of the images. The B/W color labels of the pixels were learned. 

The program compares various scikit-learn estimators and their
learning efficiencies and correctness in predicting handwritten digits.  

Following results were obtained when the entire dataset was tested:

0) 86.0% correct prediction using LinearSVC().

1) 11.0% correct prediction using SVC().

2) 56.0% correct prediction using GaussianNB().
   84.0% correct prediction using BernoulliNB().

3) -2551071524557.0% correct prediction using KMeans(). 

4) 19.0% correct prediction using KMeans() and 14 X 14 images.

5) 96.0% correct prediction using KNeighborsClassifier(). 
 
-Sriparna Majumdar (Summer 2018)
This is part of an independent study @CCSF.
(Supervisor: Prof. Aaron Brick)

"""

# Importing MNIST data

import mnistData_loader as mn

X_train, y_train, X_test, y_test = mn.mnist_array()


# Importing numpy and scikit-learn third party modules.

import numpy as np
from sklearn.svm import *
from sklearn.naive_bayes import *
from sklearn.neighbors import KNeighborsClassifier
from sklearn.decomposition import PCA

# Each classifier / regression model takes [m:n] training data and tests [a:b] test data

	
def Classifier(CLF, m, n, a, b):

    clf = CLF
    clf.fit(X_train[m:n], y_train[m:n])
    Score = clf.score(X_test[a:b], y_test[a:b])

    return Score*100


"""
The following function will use principle component analysis (PCA) for data reduction.
784 dimensions can be reduced to half the size or even less for the program to be more efficient
and give better result.
The reduced data will be used in Kmeans fitting algorithm.

"""
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

pca = PCA(n_components = 196)    # 784 pixels reduced to 14 X 14 pixels data
Xtr_red = pca.fit_transform(X_train)   # reduced training set
Xte_red = pca.fit_transform(X_test)   # reduced test set

def kmeans(Xtr, Xte, yte, m, n, a, b):

    kmeans = KMeans(n_clusters = 10, random_state = 0)   # Digits 0-9 will make 10 clusters or classes.
    kmeans.fit(Xtr[m:n])
    y_pred = kmeans.predict(Xte[a:b])

    Score = (y_pred == yte[a:b])

    return (Score.sum()/len(Score)*100)

"""
Writing the main code. This would let users choose between classifiers, and the data
to use for the classification. m, n are the boundaries of the training array X_train[m:n].
a and b are the boundaries of the test array X_test[a:b].

"""

from os import sys

# Inputting classifier and the data sizes
						
print()
						
nb = input("This program uses MNIST dataset for learning and classification (60000 training and 10000 test images)." + 
					 "\nEach image is supplied at a resolution of 28 X 28 pixels (784 pixels)." +
					 "\n" +
					 "\nPlease choose between 0 - 5 for classifiers. They are LinearSVC(0), NuSVC(1), GaussianNB / BernoulliNB (2)," +
					 "\nKMeans(3), KMeans(uses 14 X 14 pixel images) (4) and KNeighborsClassifier(n_neighbors = 2)(5): ")

print()

print("Choose the boundaries of MNIST training[m:n] and test[a:b] data: ")

try:
    L = input()
    [m, n, a, b] = [int(x) for x in L.split()]

except Exception:
    [m, n, a, b] = [0, 60000, 0, 10000] # Default values

# Formatting output.

print()

if nb == '0':
    CLF = LinearSVC()
    print(f'{round(Classifier(CLF, m, n, a, b))}% correct prediction using LinearSVC().')

elif nb == '1':
    CLF = NuSVC(probability = False, kernel = 'rbf')
    print(f'{round(Classifier(CLF, m, n, a, b))}% correct prediction using NuSVC().') 

elif nb == '2':
    CLF = GaussianNB()
    print(f'{round(Classifier(CLF, m, n, a, b))}% correct prediction using GaussianNB().')
    CLF = BernoulliNB()
    print(f'{round(Classifier(CLF, m, n, a, b))}% correct prediction using BernoulliNB().')

elif nb == '3':
    CLF = KMeans(n_clusters = 10, random_state = 0)
    print(f'{round(kmeans(Xtr = X_train, Xte = X_test, yte = y_test, m, n, a, b))}% correct prediction using KMeans().')        

elif nb == '4':
    print(f'{round(kmeans(Xtr = Xtr_red, Xte = Xte_red, yte = y_test, m, n, a, b))}% correct prediction using KMeans()' +
					"and 14 X 14 images.")

elif nb == '5':
    CLF = KNeighborsClassifier(n_neighbors = 2)
    print(f'{round(Classifier(CLF, m, n, a, b))}% correct prediction using KNeighborsClassifier().')

print()

