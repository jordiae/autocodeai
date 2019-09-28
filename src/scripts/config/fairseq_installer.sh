#!/usr/bin/env bash

cd src
git clone https://github.com/pytorch/fairseq
cd fairseq
pip install --editable .