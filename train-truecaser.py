"""
This script trains the TrueCase System
"""
import nltk
import os
import sys
import argparse
import cPickle
script_path=os.path.dirname(os.path.realpath(__file__))
truecaser_script_dir = os.path.join(script_path,"dependencies","truecaser")
sys.path.insert(1,truecaser_script_dir)
from TrainFunctions import *

def main(input_file, output_file):
    uniDist = nltk.FreqDist()
    backwardBiDist = nltk.FreqDist() 
    forwardBiDist = nltk.FreqDist() 
    trigramDist = nltk.FreqDist() 
    wordCasingLookup = {}
    sentences = []
    for line in input_file:        
        sentences.append(line.strip().decode('utf-8'))

    tokens = [nltk.word_tokenize(sentence) for sentence in sentences]
    updateDistributionsFromSentences(tokens, wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)

    cPickle.dump(uniDist, output_file, protocol=cPickle.HIGHEST_PROTOCOL)
    cPickle.dump(backwardBiDist, output_file, protocol=cPickle.HIGHEST_PROTOCOL)
    cPickle.dump(forwardBiDist, output_file, protocol=cPickle.HIGHEST_PROTOCOL)
    cPickle.dump(trigramDist, output_file, protocol=cPickle.HIGHEST_PROTOCOL)
    cPickle.dump(wordCasingLookup, output_file, protocol=cPickle.HIGHEST_PROTOCOL)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i',
        type=argparse.FileType('r'),
        default=sys.stdin, metavar='PATH',
        help="Input file (default: standard input)")
    parser.add_argument('--output', '-o', type=argparse.FileType('wb'), metavar='PATH',
        help="Output file (binary)")
    args = parser.parse_args()
    main(args.input, args.output)

