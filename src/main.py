##imports

import numpy as np 
import pandas as pd 
import os
import tensorflow as tf





#mask=tf.constant([1,1,1,1])
#result= tf.reduce_sum(tf.multiply(mask,array))

##TEnsorflow checkup
hello = tf.constant('Hello, TensorFlow!') 
sess = tf.Session() 
print(sess.run(hello))
##End tensorflow check