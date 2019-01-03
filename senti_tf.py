import tensorflow as tf
from neural_network import NeuralNetwork
from data_manager import DataManager
import datetime, time, os

def main():

# create variale scope
    with tf.variable_scope("NN", reuse = tf.AUTO_REUSE):
        dm = DataManager(data_dir='data',
                 stopwords_file='',
                 sequence_len=100,
                 test_size=0.2,
                 val_samples=10,
                 n_samples=None,
                 random_state=None)
        nn = NeuralNetwork(hidden_size=[75],
                        vocab_size=dm.vocab_size,
                        embedding_size=300,
                        max_length=dm.sequence_len,
                        learning_rate=0.01,
                        n_classes=2,
                        random_state=None)

    # Prepare summaries
    summaries_dir = '{0}/{1}'.format("logs",
                                     datetime.datetime.now().strftime('%d_%b_%Y-%H_%M_%S'))
    train_writer = tf.summary.FileWriter(summaries_dir + '/train')
    validation_writer = tf.summary.FileWriter(summaries_dir + '/validation')
    # Prepare model directory
    model_name = str(int(time.time()))
    model_dir = '{0}/{1}'.format("checkpoint", model_name)
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    # Train model
    init = tf.global_variables_initializer()
    sess = tf.Session()
    sess.run(init)
    saver = tf.train.Saver()
    x_val, y_val, val_seq_len = dm.get_val_data()
    train_writer.add_graph(nn.input.graph)

    for i in range(10):
        # Perform training step
        x_train, y_train, train_seq_len = dm.next_batch(10)
        #print (x_train.shape, y_train.shape, train_seq_len)
        #(10, 23) (10, 2) [10  6  7  5  7  8  4  5 11  6]
        train_loss, _, summary = sess.run([nn.loss, nn.train_step, nn.merged],
                                          feed_dict={nn.input: x_train,
                                                     nn.target: y_train,
                                                     nn.seq_len: train_seq_len,
                                                     nn.dropout_keep_prob: 0.5})
        train_writer.add_summary(summary, i)  # Write train summary for step i (TensorBoard visualization)
        print('{0}/{1} train loss: {2:.4f}'.format(i + 1, "10 epoch", train_loss))


        # Check validation performance
        if (i + 1) % 10 == 0:
            val_loss, accuracy, summary = sess.run([nn.loss, nn.accuracy, nn.merged],
                                                   feed_dict={nn.input: x_val,
                                                              nn.target: y_val,
                                                              nn.seq_len: val_seq_len,
                                                              nn.dropout_keep_prob: 1})
            validation_writer.add_summary(summary, i)  # Write validation summary for step i (TensorBoard visualization)
            print('   validation loss: {0:.4f} (accuracy {1:.4f})'.format(val_loss, accuracy))

    # Save model
    checkpoint_file = '{}/model.ckpt'.format(model_dir)
    save_path = saver.save(sess, checkpoint_file)
    print('Model saved in: {0}'.format(model_dir))

#10/10 epoch train loss: 0.7901
if __name__ == '__main__':
    main()
