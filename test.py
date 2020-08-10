"""
Test
"""
from absl import flags, logging
import time
from typing import Dict
from tensorboardX import SummaryWriter


FLAGS = flags.FLAGS
flags.DEFINE_string('test_msg', default="This is test message",
                   help='test msg')

# DEFINE TRAIN FLAGS

def run(training_folder):
    logging.info(FLAGS.test_msg)

