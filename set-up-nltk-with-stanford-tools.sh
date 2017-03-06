#Install or upgrade NLTK and numpy
pip install --upgrade nltk
pip install --upgrade numpy

mkdir -p dependencies
mkdir -p models
cd dependencies

##Get and prepare the Stanford Log-linear Part-Of-Speech Tagger
wget http://nlp.stanford.edu/software/stanford-postagger-2016-10-31.zip
unzip stanford-postagger-2016-10-31.zip
rm stanford-postagger-2016-10-31.zip

wget http://nlp.stanford.edu/software/stanford-parser-full-2016-10-31.zip
unzip stanford-parser-full-2016-10-31.zip
rm stanford-parser-full-2016-10-31.zip
cd ..
