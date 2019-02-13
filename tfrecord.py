import tensorflow as tf
import numpy as np
import os

def tfencord(data , path):
    data = np.array(data , dtype=np.float32)
    writer = tf.python_io.TFRecordWriter(path)
    for i in data:
        x = i
        y = 0

        #将数据list化
        feat_list_x = tf.train.BytesList(value = [x.tobytes()])
        feat_list_y = tf.train.Int64List(value = [y])

        #创建Feature
        feat_x = tf.train.Feature(bytes_list = feat_list_x)
        feat_y = tf.train.Feature(int64_list = feat_list_y)

        #生成Features
        feats = {'x':feat_x , 'y':feat_y}
        feats = tf.train.Features(feature = feats)

        example = tf.train.Example(features = feats)
        writer.write(example.SerializeToString())




# def tfencord(data , path):
#
#     data = np.array(data , dtype = np.float32)
#     writer = tf.python_io.TFRecordWriter(path)
#     for i in range(len(data)):
#         label_value = 0
#         dat_value = data[i]
#         raw_dat = tf.train.Feature(bytes_list=tf.train.BytesList(value=[dat_value.tobytes()]))
#         raw_label = tf.train.Feature(int64_list=tf.train.Int64List(value=[label_value]))
#
#         feature = {'y': raw_label, 'x': raw_dat}
#         example = tf.train.Example(features=tf.train.Features(feature=feature))
#
#
#         writer.write(example.SerializeToString())
#

# def _parse_example(example_proto):
#
#     features = {'x': tf.FixedLenFeature([] , tf.string) ,
#                 'y' : tf.FixedLenFeature([] , tf.int64)}
#
#     parse_features = tf.parse_single_example(example_proto , features = features)
#
#     x = tf.decode_raw(parse_features['x'] , tf.float32)
#
#     x = tf.reshape(x , shape = [125])
#
#     y = parse_features['y']
#
#     return x , y
#
#
# def train_input_fn(params):
#
#     train_tfrecord_path = ['/home/wty/桌面/test.tfrecords']
#
#     dataset = tf.data.TFRecordDataset(train_tfrecord_path)
#     dataset = dataset.map(_parse_example)
#     dataset = dataset.repeat(1)
#     # dataset = dataset.shuffle(10000)
#     dataset = dataset.batch(1)
#
#
#     iterator = dataset.make_one_shot_iterator()
#
#
#     labels = []
#     num = 0
#     from collections import Counter
#     try:
#         while(1):
#             x, y = iterator.get_next()
#             print(x)
#             num += 1
#     except:
#         labels = np.reshape(labels , [-1])
#
#         print(Counter(labels))
#         print('num is : ' , num)
#
#
#










