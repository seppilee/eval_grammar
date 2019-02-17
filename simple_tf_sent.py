
# -*- coding: utf-8 -*-

from konlpy.tag import Twitter
import numpy as np
import fasttext 
from gensim.models import KeyedVectors
import sentencepiece as spm

import time
import os
import tensorflow as tf
import numpy as np
import Bi_LSTM
import pandas as pd

config = tf.ConfigProto()
config.gpu_options.allow_growth = True


init=tf.global_variables_initializer()


class Word2Vec():
    def __init__(self):
        None

    def tokenize(self, doc):
        #pos_tagger = Twitter()
        #return ['/'.join(t) for t in pos_tagger.pos(doc, norm=True, stem=True)]
        sp = spm.SentencePieceProcessor()
        sp.Load('/home/cuba/project/rncd/Sentimental-Analysis/Bidirectional_LSTM/Senti.model')
        return sp.EncodeAsPieces(doc)

    def read_data(self, filename):
        with open(filename, 'r',encoding='utf-8') as f:
            data = [line.split('\t') for line in f.read().splitlines()]
            data = data[1:]
        return data  

    def Word2vec_model(self, model_name):  
        model = KeyedVectors.load_word2vec_format(model_name)
        return model
    
    def Convert2Vec(self, model_name, doc):  ## Convert corpus into vectors
        word_vec = []
        #model = gensim.models.word2vec.Word2Vec.load(model_name)
        model =  KeyedVectors.load_word2vec_format(model_name)
        for sent in doc:
            sub = []
            for word in sent:
                if(word in model.vocab):
                    sub.append(word)
                else:
                    sub.append(np.random.uniform(-0.25,0.25,300)) ## used for OOV words
            word_vec.append(sub)        
        return np.array(word_vec)
        
    def Zero_padding(self, train_batch_X, Batch_size, Maxseq_length, Vector_size):
        zero_pad = np.zeros((Batch_size, Maxseq_length, Vector_size))
        for i in range(Batch_size):
            zero_pad[i,:np.shape(train_batch_X[i])[0],:np.shape(train_batch_X[i])[1]] = train_batch_X[i]
        return zero_pad
    
    def One_hot(self, data):
        index_dict = {value:index for index,value in enumerate(set(data))}
        result = []
        for value in data:
            one_hot = np.zeros(len(index_dict))
            index = index_dict[value]
            one_hot[index] = 1
            result.append(one_hot)
        return np.array(result)

if __name__ == "__main__":
    wv = Word2Vec()
    test_data = wv.read_data("ratings_test.spm.all.txt")
    train_data = wv.read_data("ratings_train.spm.all.txt")
    
    #tokenizing 
    print("Tokenize Start!\nCould take minutes...")
    test_tokens = [[wv.tokenize(row[1]),int(row[2])] for row in test_data ]
    train_tokens = [[wv.tokenize(row[1]),int(row[2])] for row in train_data ]
    print(test_tokens)
    test_tokens = np.array(test_tokens)
    train_tokens = np.array(train_tokens)
    print("Tokenize Done!")

    train_X = train_tokens[:,0]
    train_Y = train_tokens[:,1]
    test_X = test_tokens[:,0]
    test_Y = test_tokens[:,1]
    #print ("test_Y:", test_Y, "test_X_", test_X)
    test_Y_ = wv.One_hot(test_Y)     #Convert to One-hot
    test_X_ = wv.Convert2Vec("/home/cuba/project/rncd/Sentimental-Analysis/Bidirectional_LSTM/rating_wv_spm.vec",test_X)  ## import word2vec model where you have trained before
    train_Y_ = wv.One_hot(train_Y)    # Convert to One-hot
    train_X_ = wv.Convert2Vec("/home/cuba/project/rncd/Sentimental-Analysis/Bidirectional_LSTM/rating_wv_spm.vec",train_X)  ## import word2vec model where you have trained before
    #print ("test_Y_:", test_Y_, "test_X_", type(test_X_))
    
    # setting for Hyperparameters
    Batch_size = 32
    Total_size = len(train_X)
    Vector_size = 300
    train_seq_length = [len(x) for x in train_X]
    test_seq_length = [len(x) for x in test_X]
    Maxseq_length = max(train_seq_length) ## 95
    print ("[DEBUG]Maxseq_length: ", Maxseq_length)
    learning_rate = 0.001
    lstm_units = 128
    num_class = 2
    training_epochs = 4
    
    X = tf.placeholder(tf.float32, shape = [None, Maxseq_length, Vector_size], name = 'X')
    Y = tf.placeholder(tf.float32, shape = [None, num_class], name = 'Y')
    seq_len = tf.placeholder(tf.int32, shape = [None])
    keep_prob = tf.placeholder(tf.float32, shape = None)

    BiLSTM = Bi_LSTM.Bi_LSTM(lstm_units, num_class, keep_prob)

    with tf.variable_scope("loss", reuse = tf.AUTO_REUSE):
        logits = BiLSTM.logits(X, BiLSTM.W, BiLSTM.b, seq_len)
        loss, optimizer = BiLSTM.model_build(logits, Y, learning_rate)

    prediction = tf.nn.softmax(logits)
    correct_pred = tf.equal(tf.argmax(prediction, 1), tf.argmax(Y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

    init = tf.global_variables_initializer()

    total_batch = int(len(train_X) / Batch_size)
    test_batch = int(len(test_X) / Batch_size)
  
    print("Start training!")
    modelName = "./Bidirectional_LSTM/BiLSTM_model.ckpt"
    saver = tf.train.Saver()

    train_acc = []
    train_loss = []
    test_acc = []
    test_loss = []

    with tf.Session(config = config) as sess:

        start_time = time.time()
        sess.run(init)
        train_writer = tf.summary.FileWriter('./Bidirectional_LSTM', sess.graph)
        merged = BiLSTM.graph_build()
        
        for epoch in range(training_epochs):
            avg_acc, avg_loss = 0. , 0.
            mask = np.random.permutation(len(train_X_))
            train_X_ = train_X_[mask]
            train_Y_ = train_Y_[mask]
            
            for step in range(total_batch):
                train_batch_X = train_X_[step*Batch_size : step*Batch_size+Batch_size]
                train_batch_Y = train_Y_[step*Batch_size : step*Batch_size+Batch_size]
                batch_seq_length = train_seq_length[step*Batch_size : step*Batch_size+Batch_size]
              
                train_batch_X = wv.Zero_padding(train_batch_X, Batch_size, Maxseq_length, Vector_size)
                
                sess.run(optimizer, feed_dict={X: train_batch_X, Y: train_batch_Y, seq_len: batch_seq_length})
                # Compute average loss
                loss_ = sess.run(loss, feed_dict={X: train_batch_X, Y: train_batch_Y, seq_len: batch_seq_length,
                                                  keep_prob : 0.75})
                avg_loss += loss_ / total_batch
                
                acc = sess.run(accuracy , feed_dict={X: train_batch_X, Y: train_batch_Y, seq_len: batch_seq_length,
                                                     keep_prob : 0.75})
                avg_acc += acc / total_batch
                print("epoch : {:02d} step : {:04d} loss = {:.6f} accuracy= {:.6f}".format(epoch+1, step+1, loss_, acc))
       
            summary = sess.run(merged, feed_dict = {BiLSTM.loss : avg_loss, BiLSTM.acc : avg_acc})       
            train_writer.add_summary(summary, epoch)
        
            t_avg_acc, t_avg_loss = 0. , 0.
            print("Test cases, could take few minutes")
            for step in range(test_batch):
                
                test_batch_X = test_X_[step*Batch_size : step*Batch_size+Batch_size]
                test_batch_Y = test_Y_[step*Batch_size : step*Batch_size+Batch_size]
                batch_seq_length = test_seq_length[step*Batch_size : step*Batch_size+Batch_size]
                
                test_batch_X = wv.Zero_padding(test_batch_X, Batch_size, Maxseq_length, Vector_size)
                
                # Compute average loss
                loss2 = sess.run(loss, feed_dict={X: test_batch_X, Y: test_batch_Y, seq_len: batch_seq_length,
                                                  keep_prob : 1.0})
                t_avg_loss += loss2 / test_batch
                
                t_acc = sess.run(accuracy , feed_dict={X: test_batch_X, Y: test_batch_Y, seq_len: batch_seq_length,
                                                       keep_prob : 1.0})
                t_avg_acc += t_acc / test_batch

            print("<Train> Loss = {:.6f} Accuracy = {:.6f}".format(avg_loss, avg_acc))
            print("<Test> Loss = {:.6f} Accuracy = {:.6f}".format(t_avg_loss, t_avg_acc))
            train_loss.append(avg_loss)
            train_acc.append(avg_acc)
            test_loss.append(t_avg_loss)
            test_acc.append(t_avg_acc)
     
            train_writer.close()
            duration = time.time() - start_time
            minute = int(duration / 60)
            second = int(duration) % 60
            print("%dminutes %dseconds" % (minute,second))
            save_path = saver.save(sess, modelName)
            print ('save_path',save_path)

