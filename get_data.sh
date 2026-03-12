#!/bin/bash

rm -rf fis.zip && \
rm -rf "MultiplEYE Text Corpus Data and Materials" && \
wget https://pada.psycharchives.org/bitstream/39fbdf3b-2484-4279-83f9-66c4fb8e8f47 -O fis.zip && \
unzip fis.zip && \
rm -rf __MACOSX 


if [ -d languages_data ]; then
  rm -rf languages_data_old
  mv languages_data languages_data_old
fi

mkdir -p languages_data

find "MultiplEYE Text Corpus Data and Materials" \
  -type f \
  -name "multipleye_stimuli_experiment_*" \
  -exec cp {} languages_data/ \;