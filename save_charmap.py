import os
import pickle
import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--training-data', '-i',
                        default='data/train.txt',
                        dest='training_data',
                        help='Path to training data file (one password per line) (default: data/train.txt)')

    parser.add_argument('--output-dir', '-o',
                        required=True,
                        dest='output_dir',
                        help='Output directory. If directory doesn\'t exist it will be created.')

    parser.add_argument('--save-every', '-s',
                        type=int,
                        default=5000,
                        dest='save_every',
                        help='Save model checkpoints after this many iterations (default: 5000)')

    parser.add_argument('--iters', '-n',
                        type=int,
                        default=200000,
                        dest='iters',
                        help='The number of training iterations (default: 200000)')

    parser.add_argument('--batch-size', '-b',
                        type=int,
                        default=64,
                        dest='batch_size',
                        help='Batch size (default: 64).')
    
    parser.add_argument('--seq-length', '-l',
                        type=int,
                        default=10,
                        dest='seq_length',
                        help='The maximum password length (default: 10)')
    
    parser.add_argument('--layer-dim', '-d',
                        type=int,
                        default=128,
                        dest='layer_dim',
                        help='The hidden layer dimensionality for the generator and discriminator (default: 128)')
    
    parser.add_argument('--critic-iters', '-c',
                        type=int,
                        default=10,
                        dest='critic_iters',
                        help='The number of discriminator weight updates per generator update (default: 10)')
    
    parser.add_argument('--lambda', '-p',
                        type=int,
                        default=10,
                        dest='lamb',
                        help='The gradient penalty lambda hyperparameter (default: 10)')
    
    return parser.parse_args()


def load_dataset(path, max_length):

    chars = set()

    line_count = 0
    with open(path, 'r', encoding='utf8') as f:
        for line in f:
            line = line[:-1]
            line = tuple(line)

            if len(line) > max_length:
                line = line[:max_length]
                continue  # don't include this sample, its too long

            for char in line:
                chars.add(char)

            line_count += 1
            if line_count % 100000 == 0:
                print('Parsed %s lines' % line_count)

    print('Finished parsing %s lines' % line_count)
    print("loaded {} different chars in dataset".format(len(chars)))
    return chars


args = parse_args()

chars = load_dataset(
    path=args.training_data,
    max_length=args.seq_length
)

if not os.path.isdir(args.output_dir):
    os.makedirs(args.output_dir)

# pickle to avoid encoding errors with json
with open(os.path.join(args.output_dir, 'charmap.pickle'), 'wb') as f:
    pickle.dump(chars, f)
