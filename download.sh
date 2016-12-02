#!/bin/bash

mkdir -p data
wget -P data -o names.zip https://www.ssa.gov/oact/babynames/names.zip
cd data
unzip names.zip