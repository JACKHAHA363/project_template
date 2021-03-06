"""
Main entry
"""
import sys
from absl import flags, logging
from absl import app
import time
import datetime
import traceback
import os
import string
import torch
import random
from settings import *

import train
import test


FLAGS = flags.FLAGS

# Misc
flags.DEFINE_bool('debug', default=False, help='Flag for debug mode')
flags.DEFINE_enum('mode', default='train', enum_values=['train', 'test'],
                  help='choosing between A and B')
flags.DEFINE_string('experiment', default=None, help='Name of experiment')
flags.DEFINE_bool('cuda', default=False, help='Use cuda')


def handler(type, value, tb):
    logging.exception("Uncaught exception: %s", str(value))
    logging.exception("\n".join(traceback.format_exception(type, value, tb)))


def random_string():
    return ''.join(random.sample(string.ascii_lowercase + string.ascii_uppercase, k=10))


def setup_logging_and_exp_folder():
    # Random string if debug
    if FLAGS.debug:
        FLAGS.experiment = "{}_{}".format(FLAGS.mode, random_string())

    # Use time stamp or user specified if not debug
    else:
        ts = time.time()
        FLAGS.experiment = FLAGS.experiment if FLAGS.experiment is not None else \
            "{}_{}".format(FLAGS.mode,
                           datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M'))
    training_folder = os.path.join(EXP_DIR, FLAGS.experiment)

    # Create train folder
    if os.path.exists(training_folder):
        print('{} exists!'.format(training_folder))
        exit(-1)
    else:
        os.makedirs(training_folder, exist_ok=False)

    # set up logging
    if FLAGS.debug:
        logging.get_absl_handler().python_handler.stream = sys.stdout
    else:
        logging.get_absl_handler().use_absl_log_file('absl_logging', training_folder)
    return training_folder


def main(argv):
    del argv
    trainig_folder = setup_logging_and_exp_folder()
    FLAGS.cuda = FLAGS.cuda and torch.cuda.is_available()
    logging.info('Use Cuda: {}'.format(FLAGS.cuda))
    logging.info('Current git SHA: ' + CURR_VERSION)

    # save options
    fpath = os.path.join(trainig_folder, 'flagfile')
    with open(fpath, 'w') as f:
        f.write(FLAGS.flags_into_string())

    if FLAGS.mode == 'train':
        train.run(training_folder=trainig_folder)
    elif FLAGS.mode == 'test':
        test.run(training_folder=trainig_folder)
    else:
        logging.info('Improper Mode {}'.format(FLAGS.mode))
    logging.info('Done')


if __name__ == '__main__':
    app.run(main)
