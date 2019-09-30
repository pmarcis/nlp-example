#Install or upgrade NLTK and numpy
pip install --upgrade nltk
pip install --upgrade numpy

mkdir -p dependencies
mkdir -p models
cd dependencies

#Get the source of udpipe (we need it to train models)
git clone https://github.com/ufal/udpipe.git

##Download the syntactically annotated data for Latvian that has been created in the Artificial Intelligence Laboratory of the Institute of Mathematics and Computer Science of the University of Latvia (or in short: www.ailab.lv)
#Be cautios when using it though! The data has a restrictive CC BY NC license! This basically means: not for free! More information: https://github.com/UniversalDependencies/UD_Latvian
git clone https://github.com/UniversalDependencies/UD_Latvian.git
##However, if you need to get just a tagger, there is data for training a tagger that is more open - GPL (https://github.com/PeterisP/LVTagger/blob/master/LICENSE.txt).
#It may require some re-formatting though!

##Download the syntactically annotated data for English. Authors: Universal Dependencies English Web Treebank © 2013-2017 by The Board of Trustees of The Leland Stanford Junior University.
##The English data is licensed under a very open license: CC BY 4.0. More information: https://github.com/UniversalDependencies/UD_English
git clone https://github.com/UniversalDependencies/UD_English.git

##We need to train UDPipe models for Latvian and English using the available data:
#First, compile udpipe
cd udpipe/src
make

#Now, we train the Latvian and English tokenisation, morphological tagging and syntactic (dependency) parsing models.
#The tokeniser is trained using a bidirectional LSTM artificial neural  network architecture that for each character predicts whether there is a token boundary after the character, whether there is a sentence boundary after the character and whether there is no boundary after the character. 
#The tagger models are trained using the averaged perceptron ML methods (Semi-Supervised Training for the Averaged Perceptron POS Tagger, http://aclweb.org/anthology//E/E09/E09-1087.pdf).
#The parser is  a  transition-based,  non-projective  dependency parser that uses a neural net-work classifier for prediction (Straka et al., 2016).
./udpipe --train ../../../models/lv.model.output --heldout=../../UD_Latvian/lv-ud-train.conllu ../../UD_Latvian/lv-ud-dev.conllu --tagger="models=2"
./udpipe --train ../../../models/en.model.output --heldout=../../UD_English/en-ud-train.conllu ../../UD_English/en-ud-dev.conllu --tagger="models=2"
#You can read more about the UDPipe toolkit in the paper by Straka et al. (2016): http://www.lrec-conf.org/proceedings/lrec2016/pdf/873_Paper.pdf .

#Then, we will need to set up python bindings. NOTE! YOU SHOULD SPECIFY HERE THE CORRECT PATH TO THE PYTHON INCLUDE FILES (Python.h)!
cd ../bindings/python
make PYTHON_INCLUDE=/usr/include/python2.7/
#So that you accidentally do not mess up your system, I commented the following line out! But NOTE that you have to make the library visible to python!
#sudo cp -r ufal* /usr/local/lib/python2.7/dist-packages/
#If you use Anaconda, you might need to specify here:
#make PYTHON_INCLUDE=~/anaconda2/include/python2.7/
#sudo cp -r ufal* ~/anaconda2/lib/python2.7/site-packages/
cd ../../..
#Alternatively you could try:
#pip install ufal.udpipe
#... but the versions were incompattible and the trained models failed to load last time I checked.

##We need to train a truecasing model as the UDPipe models seem to missclassify the first words in a sentence rather often due to capitalisation.
git clone https://github.com/nreimers/truecaser.git
wget http://data.statmt.org/wmt17/translation-task/europarl-v8.lv.tgz
tar zxf europarl-v8.lv.tgz
rm europarl-v8.lv.tgz
mv training-monolingual/europarl-v8.lv ./
rmdir training-monolingual
wget http://www.statmt.org/wmt14/training-monolingual-europarl-v7/europarl-v7.en.gz
gunzip europarl-v7.en.gz

cd ..

#download NLTK data (will be necessary for the truecaser)
python -m nltk.downloader -d ~/nltk_data all

python train-truecaser.py -i dependencies/europarl-v8.lv -o models/truecasing-model.lv
python train-truecaser.py -i dependencies/europarl-v7.en -o models/truecasing-model.en


#We will look at the output with a conll data visualisation tool.
cd dependencies
git clone https://github.com/spyysalo/conllu.js.git
git clone https://github.com/spyysalo/annodoc.git
#git clone https://github.com/nlplab/brat.git
cd ..

