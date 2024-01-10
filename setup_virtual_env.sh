#!/bin/bash

python3 -m venv .venv && source .venv/bin/activate && python -m pip install -U black
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt