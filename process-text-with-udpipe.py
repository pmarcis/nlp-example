"""
This script provides an example of how to use the UDPipe toolkit for sentence breaking,
tokenisation, (morphological) tagging and (syntactic) parsing.
"""
import sys
import os
import argparse
import datetime
import ufal.udpipe
import cPickle

script_path=os.path.dirname(os.path.realpath(__file__))
truecaser_script_dir = os.path.join(script_path,"dependencies","truecaser")
sys.path.insert(1,truecaser_script_dir)
from Truecaser import *


#Model implementation from https://github.com/ufal/udpipe/tree/master/bindings/python/examples
class Model:
    def __init__(self, path):
        """Load given model."""
        self.model = ufal.udpipe.Model.load(path)
        if not self.model:
            raise Exception("Cannot load UDPipe model from file '%s'" % path)

    def tokenize(self, text):
        """Tokenize the text and return list of ufal.udpipe.Sentence-s."""
        tokenizer = self.model.newTokenizer(self.model.DEFAULT)
        if not tokenizer:
            raise Exception("The model does not have a tokenizer")
        return self._read(text, tokenizer)

    def read(self, text, format):
        """Load text in the given format (conllu|horizontal|vertical) and return list of ufal.udpipe.Sentence-s."""
        input_format = ufal.udpipe.InputFormat.newInputFormat(format)
        if not input_format:
            raise Exception("Cannot create input format '%s'" % format)
        return self._read(text, input_format)

    def _read(self, text, input_format):
        input_format.setText(text)
        error = ufal.udpipe.ProcessingError()
        sentences = []

        sentence = ufal.udpipe.Sentence()
        while input_format.nextSentence(sentence, error):
            sentences.append(sentence)
            sentence = ufal.udpipe.Sentence()
        if error.occurred():
            raise Exception(error.message)

        return sentences

    def tag(self, sentence):
        """Tag the given ufal.udpipe.Sentence (inplace)."""
        self.model.tag(sentence, self.model.DEFAULT)

    def parse(self, sentence):
        """Parse the given ufal.udpipe.Sentence (inplace)."""
        self.model.parse(sentence, self.model.DEFAULT)

    def write(self, sentences, format):
        """Write given ufal.udpipe.Sentence-s in the required format (conllu|horizontal|vertical)."""

        output_format = ufal.udpipe.OutputFormat.newOutputFormat(format)
        output = ''
        for sentence in sentences:
            output += output_format.writeSentence(sentence)
        output += output_format.finishDocument()

        return output

"""Main method - performs processing of text from a file (handle) and writes the result in a conll format in a file (handle)"""
def main(input_file, output_file, language="en",verbose=True):
    sys.stderr.write("Starting to process text in file {0} at {1}\n".format(input_file.name,str(datetime.datetime.now())))
    text=input_file.read().decode('utf-8')
    if verbose:
        print "============= Raw text: ============="
        print text
    
    script_path=os.path.dirname(os.path.realpath(__file__)) #needed to figure out the path of dependencies when executing from different directories
    
    model_file = os.path.join(script_path,"models",language+".model.output")

    #Read the truecasing model (this is the slowest part in this example and could be removed.
    truecasing_model = os.path.join(script_path,"models","truecasing-model."+language)
    f = open(truecasing_model, 'rb')
    uniDist = cPickle.load(f)
    backwardBiDist = cPickle.load(f)
    forwardBiDist = cPickle.load(f)
    trigramDist = cPickle.load(f)
    wordCasingLookup = cPickle.load(f)
    f.close()

    #Read the UDPipe model
    model = Model(model_file)

    #First, we tokenize the text and split it into sentences.
    sentences = model.tokenize(text)
    
    #Then, we truecase the text (this is a bit ad-hoc).
    for s in sentences:
        tokens = [w.form.lower() for w in s.words ]
        truecased_tokens = getTrueCase(tokens, 'title', wordCasingLookup, uniDist, backwardBiDist, forwardBiDist, trigramDist)
        #We truecase only the first token in a sentence!
        s.words[1].form = truecased_tokens[1]

    #Then, we perform tagging and parsing for each sentence
    for s in sentences:
        model.tag(s) #inplace tagging
        model.parse(s) #inplace parsing
    conllu = model.write(sentences, "conllu")
    #Save the result in the output file
    if verbose:
        print "========= Processed sentences: ========="
        print (conllu)
        sys.stderr.write("... processing completed at {0}\n".format(str(datetime.datetime.now())))
    output_file.write(conllu.encode('utf-8'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i',
        type=argparse.FileType('r'),
        default=sys.stdin, metavar='PATH',
        help="Input file (default: standard input)")
    parser.add_argument('--output', '-o', type=argparse.FileType('w'),
        default=sys.stdout, metavar='PATH',
        help="Output file (default: standard output)")
    parser.add_argument('--language', '-l', type=str, default='en',
        help="Language (default: %(default)s))")
    args = parser.parse_args()
    main(args.input, args.output, args.language)

