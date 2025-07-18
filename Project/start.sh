#!/bin/bash
export PORT=${PORT:-5000}
cd server
python3 main.py serve --proto http -p $PORT
