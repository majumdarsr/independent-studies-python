"""
This is the MNIST data loader.
The data files were downloaded from http://yann.lecun.com/exdb/mnist/

Four files are available on this site: 

train-images-idx3-ubyte.gz:  training set images (9912422 bytes) 
train-labels-idx1-ubyte.gz:  training set labels (28881 bytes) 
t10k-images-idx3-ubyte.gz:   test set images (1648877 bytes) 
t10k-labels-idx1-ubyte.gz:   test set labels (4542 bytes) 

Training dataset contains 60000 images (28 X 28 pixels) and labels. 
Test dataset contains 10000 images (28 X 28 pixels) and labels.

-Sriparna Majumdar
This is part of an independent study carried out @CCSF.
Supervisor: Prof. Aaron Brick.

"""

# loading third party modules

import gzip
import numpy as np

# The following function is reading unicode data as bytes object

def load_data(file):
 
    f = gzip.open(file, 'rb')
    
    data = f.read()  # reading data
    
    f.close()

    return data   
  
# The following function converts bytes data into 2D / 1D numpy array of floats.

def mnist_array():
   
    train_data = load_data('train-images-idx3-ubyte.gz')
    train_label = load_data('train-labels-idx1-ubyte.gz')
    test_data = load_data('t10k-images-idx3-ubyte.gz')
    test_label = load_data('t10k-labels-idx1-ubyte.gz')
    
    mylist = [train_data, train_label, test_data, test_label]
    
# casting byte data as numpy array of floats.

    for n in range (4):

        mylist[n] = [float(x) for x in list(mylist[n])] # Casting byte -> integer -> float
        
        if n % 2:
            header_text = len(mylist[n]) % 10000 # 60016 or 10008 long datasets contained 16/8 characters long headers.
            mylist[n] = np.array(mylist[n][header_text:])   # Casting labels / targets as numpy array
        
        else:
            header_text = len(mylist[n]) % 784 # ((60000 * 784) + 16) training or ((10000 * 784) + 8) test datasets with headers.
            mylist[n] = np.array(mylist[n][header_text:])
            mylist[n] = np.reshape(mylist[n], (len(mylist[n])//784, 784)) # Casting image data as 2D array of 784 pixels / features

    return mylist


"""
# THIS ONE IS FOR VISUALIZING THE MNIST DATA
# WRITTEN BY AARON

trd, trl, ted, tel = mnist_array()

# print an example image

def BW(n):
 if n>150:
  return '*'
 elif n>50:
  return '.'
 else:
  return ' '

import random
index = random.randint(0,len(ted))
print('INDEX: ', tel[index])
for row in range(28):
 print(' '.join([BW(n) for n in ted[index][28*row:28*row+28]]))

"""
