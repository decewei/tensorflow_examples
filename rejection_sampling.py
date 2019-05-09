import tensorflow as tf
import numpy as np
# everything is based on tensorflow 2.0

# this is important or rejection sample won't work
# I set this here so that all random process keeps the same order but you can
# also set it at rejection_resample function
tf.random.set_seed(2342)


def map2label(sample):
    return tf.cast(tf.math.equal(sample, 2), tf.int32)

np_data = np.array([0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2])
target_dist = [0.5, 0.5]
init_dist = [(np_data.shape[0]-3)/np_data.shape[0], 3/np_data.shape[0]]

dataset = tf.data.Dataset.from_tensor_slices(np_data)
rej = tf.data.experimental.rejection_resample(map2label, target_dist, init_dist, 20)
dataset = dataset.apply(rej)

bucket_counts = [0, 0]
for i in range(100):
    for data in dataset:
        class_id, data_content = data
        bucket_counts[class_id.numpy()] += 1
print("This is your target_dist", target_dist, "This is your initial distribution", init_dist)
print("This is your result counts", bucket_counts,
      "This is your final dist", bucket_counts[0] / np.sum(bucket_counts), bucket_counts[1] / np.sum(bucket_counts))