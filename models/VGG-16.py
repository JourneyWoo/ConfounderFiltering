 #!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: wuzhenglin
"""

import numpy as np
import tensorflow as tf
import scipy
import sys

# make the label of dataset
def change(arr):
    
    
    inti = arr[0]
    
    if inti == 0:
        inti = np.array([1, 0])
    else:
        inti = np.array([0, 1])
    
    inti = inti[np.newaxis, :] 
    
    for i in range(1, arr.shape[0]):
        
        tem = arr[i]
    
        if tem == 0:
            tem = np.array([1, 0])
        else:
            tem = np.array([0, 1])
        
        tem = tem[np.newaxis, :] 
    
        inti = np.append(inti, tem, axis = 0)
        
    return inti
        
        
        
# read the dataset from the tfrecords
def read_and_decode(p):
    


    filename_queue = tf.train.string_input_producer([p]) 
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)   

    features = tf.parse_single_example(serialized_example,
                                       features={
                                               'label': tf.FixedLenFeature([], tf.int64),
                                               'img_raw' : tf.FixedLenFeature([], tf.string),
                                               })  

    image = tf.decode_raw(features['img_raw'], tf.uint8)
    image = tf.reshape(image, [128, 128])
    label = tf.cast(features['label'], tf.int32)
    
    
    
    return image, label

# Begin the CNN building 
def weight_variable(path, select, shape):
    
    if select == 1:
        initial = np.fromfile(path, dtype = np.float32)
        initial = initial.reshape(shape)
        

    else:        
        initial = tf.truncated_normal(shape, stddev = 0.1, dtype = tf.float32)
        
    return tf.Variable(initial)

#unused in this method
def find_max(a):
    a = abs(a)
    index_a = a.argmax(axis = 0)
    
    if a[index_a[0]][0] > a[index_a[1]][1]:
        return index_a[0]
    else:
        return index_a[1]
    
def bias_variable(path, select, shape):
    
    if select == 1:
        initial = np.fromfile(path, dtype = np.float32)
        initial = initial.reshape(shape)
    
    else:        
        initial = tf.constant(0.1, shape = shape, dtype = tf.float32)

    return tf.Variable(initial)


def conv2d(x, W):
    
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')
  



def cnn_model():

    #Control area

    cap_c = sys.argv[1]
    cap_h = sys.argv[2]

    test_c = sys.argv[3]
    test_h = sys.argv[4]
    
    name = sys.argv[5]
    
    pathpath = sys.argv[6]

    #Control area
    
    hc_batch_size = 25
    hc_num = cap_c + cap_h
    
    hc_test_num = test_c + test_h
    
    hc_train = pathpath + name + '_train_healthyordisease.tfrecords'
    hc_test = pathpath + name + '_test_healthyordisease.tfrecords'
      
    hidden = 256
    image_size = 128 
    label_size = 2
    
    hc_epochs = 8
    hc_learning_rate = 0.005




    
    #data set
    hc_im, hc_lab = read_and_decode(hc_train)
    hc_train_img, hc_train_label = tf.train.shuffle_batch([hc_im, hc_lab],
                                            batch_size = hc_batch_size, capacity = hc_num,
                                            min_after_dequeue = 10)

    hc_im_, hc_lab_ = read_and_decode(hc_test)  
    hc_test_img, hc_test_label = tf.train.shuffle_batch([hc_im_, hc_lab_],
                                            batch_size = hc_test_num - 10, capacity = hc_test_num,
                                            min_after_dequeue = 10)
    
  
  
    chc_select = 0 


    print 'Healthy and Disease Section'
    epochs = hc_epochs
    batch_size = hc_batch_size
    learning_rate = hc_learning_rate
    num = hc_num
    num_test = hc_test_num - 10
    
    train_image = hc_train_img
    train_label = hc_train_label
    test_image = hc_test_img
    test_label = hc_test_label
    
            
    #Model Parameter
    x = tf.placeholder(tf.float32, shape = [None, image_size * image_size])
    y = tf.placeholder(tf.float32, shape = [None, label_size])

    weight_balance = tf.constant([0.1])
  
    X_train_ = tf.reshape(x, [-1, image_size, image_size, 1])

    #First layer
    W_conv1 = weight_variable("w1.bin", chc_select, [3, 3, 1, 4])
    b_conv1 = bias_variable("b1.bin", chc_select, [4])

    h_conv1 = tf.nn.relu(conv2d(X_train_, W_conv1) + b_conv1)
    # h_lrn1 = tf.nn.local_response_normalization(h_conv1, alpha=1e-4, beta=0.75, depth_radius=2, bias=2.0)


    #Second layer
    W_conv2 = weight_variable("w2.bin", chc_select, [3, 3, 4, 4])
    b_conv2 = bias_variable("b2.bin", chc_select, [4])

    h_conv2 = tf.nn.relu(conv2d(h_conv1, W_conv2) + b_conv2)
    # h_lrn2 = tf.nn.local_response_normalization(h_conv2, alpha=1e-4, beta=0.75, depth_radius=2, bias=2.0)
    h_pool2 = max_pool_2x2(h_conv2)


    # Third layer
    W_conv5 = weight_variable("w5.bin", chc_select, [3, 3, 4, 8])
    b_conv5 = bias_variable("b5.bin", chc_select, [8])

    h_conv5 = tf.nn.relu(conv2d(h_pool2, W_conv5) + b_conv5)

    # Fourth layer
    W_conv6 = weight_variable("w6.bin", chc_select, [3, 3, 8, 8])
    b_conv6 = bias_variable("b6.bin", chc_select, [8])

    h_conv6 = tf.nn.relu(conv2d(h_conv5, W_conv6) + b_conv6)
    h_pool6 = max_pool_2x2(h_conv6)

    # Fifth layer
    W_conv7 = weight_variable("w7.bin", chc_select, [3, 3, 8, 16])
    b_conv7 = bias_variable("b7.bin", chc_select, [16])

    h_conv7 = tf.nn.relu(conv2d(h_pool6, W_conv7) + b_conv7)


    # 6 layer
    W_conv8 = weight_variable("w9.bin", chc_select, [3, 3, 16, 16])
    b_conv8 = bias_variable("b9.bin", chc_select, [16])

    h_conv8 = tf.nn.relu(conv2d(h_conv7, W_conv8) + b_conv8)


    # 7 layer
    W_conv9 = weight_variable("w10.bin", chc_select, [3, 3, 16, 16])
    b_conv9 = bias_variable("b10.bin", chc_select, [16])

    h_conv9 = tf.nn.relu(conv2d(h_conv8, W_conv9) + b_conv9)
    h_pool9 = max_pool_2x2(h_conv9)

    # 8
    W_conv10 = weight_variable("w11.bin", chc_select, [3, 3, 16, 32])
    b_conv10 = bias_variable("b11.bin", chc_select, [32])

    h_conv10 = tf.nn.relu(conv2d(h_pool9, W_conv10) + b_conv10)


    # 9
    W_conv11 = weight_variable("w12.bin", chc_select, [3, 3, 32, 32])
    b_conv11 = bias_variable("b12.bin", chc_select, [32])

    h_conv11 = tf.nn.relu(conv2d(h_conv10, W_conv11) + b_conv11)


    # 10
    W_conv12 = weight_variable("w13.bin", chc_select, [3, 3, 32, 32])
    b_conv12 = bias_variable("b13.bin", chc_select, [32])

    h_conv12 = tf.nn.relu(conv2d(h_conv11, W_conv12) + b_conv12)
    h_pool12 = max_pool_2x2(h_conv12)

    # 11
    W_conv13 = weight_variable("w14.bin", chc_select, [3, 3, 32, 32])
    b_conv13 = bias_variable("b14.bin", chc_select, [32])

    h_conv13 = tf.nn.relu(conv2d(h_pool12, W_conv13) + b_conv13)


    # 12
    W_conv14 = weight_variable("w15.bin", chc_select, [3, 3, 32, 32])
    b_conv14 = bias_variable("b15.bin", chc_select, [32])

    h_conv14 = tf.nn.relu(conv2d(h_conv13, W_conv14) + b_conv14)


    # 13
    W_conv15 = weight_variable("w16.bin", chc_select, [3, 3, 32, 32])
    b_conv15 = bias_variable("b16.bin", chc_select, [32])

    h_conv15 = tf.nn.relu(conv2d(h_conv14, W_conv15) + b_conv15)
    h_pool15 = max_pool_2x2(h_conv15)

    #Full connect layer 1
    W_fc1 = weight_variable("w3.bin", chc_select, [4 * 4 * 32, hidden])
    b_fc1 = bias_variable("b3.bin", chc_select, [hidden])

    h_pool15_flat = tf.reshape(h_pool15, [-1, 4 * 4 * 32])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool15_flat, W_fc1) + b_fc1)

    #Full connect layer 2
    W_fc3 = weight_variable("w8.bin", chc_select, [hidden, hidden])
    b_fc3 = bias_variable("b8.bin", chc_select, [hidden])

    h_fc3 = tf.nn.relu(tf.matmul(h_fc1, W_fc3) + b_fc3)

    #drop layer
    keep_prob = tf.placeholder(tf.float32)
    h_fc3_drop = tf.nn.dropout(h_fc3, keep_prob)

    #Output_Softmax
    W_fc2 = weight_variable("w4.bin", chc_select, [hidden, label_size])
    b_fc2 = bias_variable("b4.bin", chc_select, [label_size])

    out_feed = tf.add(tf.matmul(h_fc3_drop, W_fc2), b_fc2)
    y_conv = tf.nn.softmax(out_feed)

    #Train
    loss = tf.reduce_mean(tf.nn.weighted_cross_entropy_with_logits(y, out_feed, weight_balance))
    optimize = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss)

    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    #Sess section
    print 'Begin training'
    init_op = tf.global_variables_initializer()

    with tf.Session() as sess:

        sess.run(init_op)

        print 'Build the thread'
        coord = tf.train.Coordinator()

        threads = tf.train.start_queue_runners(coord = coord)
        
    
        #Begin the training process
        step = 1
        
        for ep in range(epochs):
        
            for i in range(num//batch_size):
                
                #train Data
                example, l = sess.run([train_image, train_label])
                example = example.flatten()
                example = example.reshape([batch_size, image_size * image_size])
                ll = change(l)
                feed_dict = {x: example, y: ll, keep_prob: 1.0}
                feed_dict_d = {x: example, y: ll, keep_prob: 0.3}
                
                #test Data
                example_, l_ = sess.run([test_image, test_label])
                example_ = example_.flatten()
                example_ = example_.reshape([num_test, image_size * image_size])
                ll_ = change(l_)
                feed_dict_ = {x: example_, y: ll_, keep_prob: 1.0}
            
                
                             
                sess.run(optimize, feed_dict = feed_dict_d)               
                los, acc = sess.run([loss, accuracy], feed_dict = feed_dict)
                
                if step % 5 == 0:
                    
                    print 'train acc: ', acc
     

                step = step + 1
        
        print 'train is over, the number of steps: ', step        
        print '*******************************************'
        print 'test section'
        
        test_loss, test_acc = sess.run([loss, accuracy], feed_dict = feed_dict_)
        print 'test acc: ', test_acc 
        
                            
       
        coord.request_stop()
        coord.join(threads)

    

if __name__ == '__main__':
    
    cnn_model()
