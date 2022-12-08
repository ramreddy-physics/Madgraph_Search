#!/bin/bash
mkdir Events
tar -xvf benchmark_dataset.csv.tar benchmark_dataset.csv
cp -R Hypothesis ../models
cd ..
./bin/mg5_aMC Madgraph_Search/1.txt
mv -f signal_generations/Events/* Madgraph_Search/Events
cd Madgraph_Search
for d in Events/*
do
  cp -f parser.py "$d"
  cp -f network.py "$d"
  cd "$d"
  gunzip -k unweighted_events.lhe.gz
  python3 parser.py
  rm -f unweighted_events.lhe
  python3 network.py
  cd ../..
done
python3 mle.py