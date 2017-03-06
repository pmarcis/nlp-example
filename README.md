# NLP Example

This is an example of how to:

* Train neural network-based sentence breaking, tokenisation, tagging and parsing models with the [UDPipe](https://github.com/ufal/udpipe) toolkit. The example shows how to build models for English and Latvian using the default parameters.
* Use pre-trained UDPipe models in python for sentence breaking, tokenisation, tagging and parsing of text documents.
* Use the python library [NLTK](http://www.nltk.org/) for sentence breaking, tokenisation, tagging and parsing of text documents in English using the [Stanford Tagger](http://nlp.stanford.edu/software/tagger.shtml) and [Stanford Parser](http://nlp.stanford.edu/software/lex-parser.shtml).
* Visualise syntactically parsed data in the CONLLU format using [conllu.js](https://github.com/spyysalo/conllu.js).

**Note: The example is meant for learning purposes!** It uses publicly available tools and resources and executes default workflows (which means that the examples will probably lag behind what for each language is state-of-the-art). Also, not all resources have open licenses (e.g., the Latvian syntactically annotated corpus cannot be used in real projects due to its restrictive license).

# Installation

The tools have been tested only on Linux (Ubuntu 16.04) and the installation script is meant only for Linux. That being said, this is what you need to do:

1) You know the drill: `git clone https://github.com/pmarcis/nlp-example.git` and `cd nlp-example`.
2) Next, for UDPipe execute the `set-up-udpipe.sh` script. You may want to go through it though before you do this! The script will (hopefully) install all required dependencies, download relevant data and train UDPipe models for English and Latvian. The script will also install dependencies for the syntactically parsed data visualisation. For more details, see the [script](set-up-udpipe.sh)! The script may take an hour (more or less) to complete.
3) Next, for NLTK execute the `set-up-nltk-with-stanford-tools.sh` script. You may want to go through it though before you do this! The script will (hopefully) install all required python dependencies and download the Stanford Tagger and Stanford Parser. For more details, see the [script](set-up-nltk-with-stanford-tools.sh)!

# Usage

Once installed, you can execute processing of text documents as follows:
```
python process-text-with-udpipe.py -i test_en.txt -o test_en_out.txt -l en
python process-text-with-udpipe.py -i test_lv.txt -o test_lv_out.txt -l lv
python process-text-with-nltk.py -i test_en.txt -o test_en_nltk_out.txt -l en
```

The resulting CONLLU data from the files `test_en_out.txt` and `test_lv_out.txt` can be visualised (for human comprehension of what has happened) in `visualize.html` (i.e., copy the output from the files and paste it in the text box that appears after you click on `edit`). Make sure you have installed all dependencies from `set-up-udpipe.sh`. Otherwise you will be disappointed by the visualisation!

For example purposes, the scripts have been written so that they talk a lot. If you want to use the tools for your own projects, I suggest commenting out everything that writes to standard output or standard error output.

# Lincense

The code here is licensed under the MIT license (i.e., do whatever you like with it), however the dependencies are licensed under various different licenses. Therefore, do not assume that you will get a Holy Grail here!
