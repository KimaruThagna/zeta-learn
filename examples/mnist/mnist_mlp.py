# -*- coding: utf-8 -*-

from ztlearn.utils import *
from ztlearn.dl.models import Sequential
from ztlearn.optimizers import register_opt
from ztlearn.datasets.mnist import fetch_mnist
from ztlearn.dl.layers import Dropout, Dense, BatchNormalization

mnist = fetch_mnist()
train_data, test_data, train_label, test_label = train_test_split(mnist.data,
                                                                  mnist.target.astype('int'),
                                                                  test_size   = 0.33,
                                                                  random_seed = 5,
                                                                  cut_off     = 2000)

# plot samples of training data
plot_tiled_img_samples(train_data[:40], train_label[:40], dataset = 'mnist')

# optimizer definition
opt = register_opt(optimizer_name = 'nestrov', momentum = 0.01, learning_rate = 0.0001)

# model definition
model = Sequential()
model.add(Dense(512, activation = 'relu', input_shape = (784,)))
model.add(Dropout(0.3))
model.add(BatchNormalization())
model.add(Dense(10, activation = 'relu')) # 10 digits classes
model.compile(loss = 'cce', optimizer = opt)

model.summary()

model_epochs = 12
fit_stats = model.fit(train_data,
                      one_hot(train_label),
                      batch_size      = 128,
                      epochs          = model_epochs,
                      validation_data = (test_data, one_hot(test_label)),
                      shuffle_data    = True)

eval_stats = model.evaluate(test_data, one_hot(test_label))

predictions = unhot(model.predict(test_data, True))
print_results(predictions, test_label)
plot_img_results(test_data[:40], test_label[:40], predictions, dataset = 'mnist') # truncate to 40 samples

model_name = model.model_name
plot_metric('loss', model_epochs, fit_stats['train_loss'], fit_stats['valid_loss'], model_name = model_name)
plot_metric('accuracy', model_epochs, fit_stats['train_acc'],  fit_stats['valid_acc'], model_name = model_name)
plot_metric('evaluation',
                          eval_stats['valid_batches'],
                          eval_stats['valid_loss'],
                          eval_stats['valid_acc'],
                          model_name = model_name,
                          legend     = ['loss', 'acc'])
