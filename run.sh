#!/bin/sh

python3 -m venv venv
source venv/bin/activate
pip install numpy pypng

python3 red_gradient.py
