"""
Train
"""
from absl import flags, logging
import time
from typing import Dict
from tensorboardX import SummaryWriter


FLAGS = flags.FLAGS
flags.DEFINE_string('train_msg', default="This is training message",
                   help='train msg')

# DEFINE TRAIN FLAGS

def run(training_folder):
    logging.info(FLAGS.train_msg)

