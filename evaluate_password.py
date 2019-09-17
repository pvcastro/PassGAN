import tensorflow as tf
import numpy as np
import tflib as lib
import pickle
import fire
import models
import utils
from pathlib import Path


def password_to_id(charmap, password):
    return np.array([[charmap[c] for c in l] for l in password], dtype='int32')


def load_charmap(charmap_path):
    charmap_path = Path(charmap_path)
    return pickle.load(charmap_path.open(mode='rb'), encoding='latin1')


# def run_discriminator(charmap):
#     seq_length = 10
#     batch_size = 1
#     layer_dim = 128
#     lamb = 10
#
#     real_inputs_discrete = tf.placeholder(tf.int32, shape=[batch_size, seq_length])
#     real_inputs = tf.one_hot(real_inputs_discrete, len(charmap))
#     fake_inputs = models.Generator(batch_size, seq_length, layer_dim, len(charmap))
#     fake_inputs_discrete = tf.argmax(fake_inputs, fake_inputs.get_shape().ndims - 1)
#
#     disc_real = models.Discriminator(real_inputs, seq_length, layer_dim, len(charmap))
#     disc_fake = models.Discriminator(fake_inputs, seq_length, layer_dim, len(charmap))
#
#     disc_cost = tf.reduce_mean(disc_fake) - tf.reduce_mean(disc_real)
#     # gen_cost = -tf.reduce_mean(disc_fake)
#
#     # WGAN lipschitz-penalty
#     alpha = tf.random_uniform(
#         shape=[batch_size, 1, 1],
#         minval=0.,
#         maxval=1.
#     )
#
#     differences = fake_inputs - real_inputs
#     interpolates = real_inputs + (alpha * differences)
#     gradients = \
#         tf.gradients(models.Discriminator(interpolates, seq_length, layer_dim, len(charmap)), [interpolates])[
#             0]
#     slopes = tf.sqrt(tf.reduce_sum(tf.square(gradients), reduction_indices=[1, 2]))
#     gradient_penalty = tf.reduce_mean((slopes - 1.) ** 2)
#     disc_cost += lamb * gradient_penalty
#
#     # gen_params = lib.params_with_name('Generator')
#     disc_params = lib.params_with_name('Discriminator')
#
#     # gen_train_op = tf.train.AdamOptimizer(learning_rate=1e-4, beta1=0.5, beta2=0.9).minimize(gen_cost,
#     #                                                                                          var_list=gen_params)
#     disc_train_op = tf.train.AdamOptimizer(learning_rate=1e-4, beta1=0.5, beta2=0.9).minimize(disc_cost,
#                                                                                               var_list=disc_params)
#
#     _disc_cost, _ = session.run(
#         [disc_cost, disc_train_op],
#         feed_dict={real_inputs_discrete: _data}
#     )


def evaluate_password(lms_path, password, max_length, charmap_path=None):
    password += '`' * (max_length - len(password))
    char_pwd = [char for char in password]
    # pwd_array = np.array(char_pwd)
    pwd_array = [tuple(char_pwd)] * 640
    # charmap = load_charmap(charmap_path)
    # pwd_chars_ids = password_to_id(charmap, password)
    # print(pwd_chars_ids)
    # pwd_array = np.empty((1, 20), dtype='int32')
    # pwd_char_ids_array = np.array(pwd_chars_ids)

    with open(Path(lms_path), 'rb') as f:
        true_char_ngram_lms = pickle.load(f, encoding='latin1')

    for i in range(4):
        lm = utils.NgramLanguageModel(i + 1, pwd_array, tokenize=False)
        print('js{}'.format(i + 1), lm.js_with(true_char_ngram_lms[i]))



if __name__ == '__main__': fire.Fire(evaluate_password)
