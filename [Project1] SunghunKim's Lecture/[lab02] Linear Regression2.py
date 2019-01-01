import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

W = tf.Variable(tf.random_normal([1]), name="weight")
b = tf.Variable(tf.random_normal([1]), name="bias")

X = tf.placeholder(tf.float32, shape=[None])
Y = tf.placeholder(tf.float32, shape=[None])

hypothesis = X * W + b
cost = tf.reduce_mean(tf.square(hypothesis - Y))

# minimize
optimizer = tf.train.GradientDescentOptimizer(learning_rate = 0.01)
train = optimizer.minimize(cost)

# Launch the graph in a session
sess = tf.Session()
# Initializes global variables in the graph
sess.run(tf.global_variables_initializer())

#Learning
for step in range(10):
    cost_val, w_val, b_val, _ = sess.run([cost,W,b,train], 
    feed_dict={X:[1, 2, 3, 4, 5],
                Y: [2.1, 3.1, 4.1, 5.1, 6.1]})
    if(step % 20 == 0):
        print(step, cost_val, w_val, b_val)

# Testing our model
print(sess.run(hypothesis, feed_dict={X:[5]}))
print(sess.run(hypothesis, feed_dict={X:[2.5]}))
print(sess.run(hypothesis, feed_dict={X:[1.5, 3.5]}))