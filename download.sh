#!/bin/bash

mkdir -p data
wget -P data -o names.zip https://www.ssa.gov/oact/babynames/names.zip
touch names.zip
cd data && unzip -f names.zip