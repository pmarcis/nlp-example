"""
This script provides an example of how to use NLTK for sentence breaking,
tokenisation, (morphological) tagging and (syntactic) parsing.
The tagging and parsing are carried out by the Stanford tagger and Stanford Parser.
"""
import sys
import os
import argparse
import datetime
import nltk.data
from nltk.parse.util import *
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tag import StanfordPOSTagger
from nltk.parse.stanford import StanfordDependencyParser
from nltk.stem.porter import PorterStemmer

"""Main method - performs processing of text from a file (handle) and writes the result in a conll format in a file (handle)"""
def main(input_file, output_file, language):
    sys.stderr.write("Starting to process text in file {0} at {1}\n".format(input_file.name,str(datetime.datetime.now())))
    text=input_file.read()
    print "============= Raw text: ============="
    print text
    
    script_path=os.path.dirname(os.path.realpath(__file__)) #needed to figure out the path of dependencies when executing from different directories
    
    #this example is only for English (as ... NLTK has no models for Latvian)
    if language=="en":
        #First, we perform sentence breaking.
        sentences = sent_tokenize(text.strip(), language='english')
        print "============= Sentences: ============"
        print sentences
        #Then, we perform tokenization.
        tokens = [word_tokenize(s, language='english') for s in sentences]
        print "============== Tokens: =============="
        print tokens
        #In some cases (e.g., for indexing and search related tasks) it may be enough to perform stemming of the text.
        #This is, however, not needed nor for tagging, nor for parsing. It is included only as an example.
        stemmer = PorterStemmer(mode='NLTK_EXTENSIONS')
        stemmed_data = [[stemmer.stem(t) for t in s] for s in tokens]
        print "========== Stemmed tokens: =========="
        print stemmed_data
        #Then, we execute the Stanford log linear (maximum entropy-based) part-of-speech tagger
        tagger_jar = os.path.join(script_path,"dependencies","stanford-postagger-2016-10-31","stanford-postagger.jar")
        tagger_model = os.path.join(script_path,"dependencies","stanford-postagger-2016-10-31","models","english-bidirectional-distsim.tagger") 
        pos_tagger = StanfordPOSTagger(tagger_model, tagger_jar, encoding='utf8')
        tagged_data = [pos_tagger.tag(s) for s in tokens]
        print "========= Tagged sentences: ========="
        print tagged_data
        #When the data is tagged, we perform syntactic parsing using the Stanford parser.
        parser_jar = os.path.join(script_path,"dependencies","stanford-parser-full-2016-10-31","stanford-parser.jar")
        parser_model = os.path.join(script_path,"dependencies","stanford-parser-full-2016-10-31","stanford-parser-3.7.0-models.jar")
        parser=StanfordDependencyParser(model_path="edu/stanford/nlp/models/lexparser/englishFactored.ser.gz", path_to_models_jar=parser_model, path_to_jar=parser_jar)
        parsed_data = parser.tagged_parse_sents(tagged_data)
        #Finally, we print the result to the output file.
        #Note that the Stanford parser deleted all punctuation marks and the data also lacks lemmas.
        #There is a way to get them back - create a class that inherits from StanfordDependencyParser and add "-outputFormatOptions includePunctuationDependencies" to the cmd that executes the parser.
        #... or use the Stanford Neural Dependency Parser instead!
        #For the example, I did not want to overly complicate the code.
        print "========= Parsed sentences: ========="
        for parsed_sentence in parsed_data:
            for dependency_graph in parsed_sentence:
                output_file.write(dependency_graph.to_conll(10))
                print dependency_graph.to_conll(10)
            output_file.write("\n")

    sys.stderr.write("... processing completed at {0}\n".format(str(datetime.datetime.now())))

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
