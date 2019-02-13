'''
该代码运行在tensorflow Eager Execution 模式下
'''
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

def tfencode(data , path):

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


def _parse_example(example_proto):

    #定义一个特征字典，该字典的键名必须与tfrecord文件的键名一致，字典的值类型必须与tfrecord文件一致
    features = {'x':tf.FixedLenFeature([] , tf.string) ,
                'y':tf.FixedLenFeature([] , tf.int64)}

    #利用tf.parse_single_example读取tfrecord文件，返回一个与特征字典一致的tensor字典
    parse_example = tf.parse_single_example(example_proto , features = features)

    #对x进行解码。在生成tfrecord文件时，通常我们会将x编码为二进制文件，因此在这里需要采用tf.decode_raw函数解码。在这里需要
    #注意的是，解码的数据格式必须与编码的数据格式相同，否则会出现错误
    x = tf.decode_raw(parse_example['x'] , tf.float32)
    x = tf.reshape(x , shape = [125])
    y = parse_example['y']
    return x , y


def tfdecode(path):
    dataset = tf.data.TFRecordDataset([path])
    dataset = dataset.map(_parse_example)
    dataset = dataset.repeat(1)
    # dataset = dataset.shuffle(10000)
    dataset = dataset.batch(1)

    iterator = dataset.make_one_shot_iterator()
    num = 0
    dat = []
    try:
        while(1):
            x , y = iterator.get_next()
            dat.append(np.array(x[0]))
            num += 1
    except:
        print(num)

        fig , ax = plt.subplots(3 , 4)
        for i in range(3):
            for j in range(4):
                ax[i][j].plot(dat[i * 3 + j])

        plt.show()













