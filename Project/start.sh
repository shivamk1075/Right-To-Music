#!/bin/bash
cd client
npm install
npm run build
cd ..
export PORT=${PORT:-5000}
export REACT_BUILD_DIR=client/build
cd server
python3 main.py serve --proto http -p $PORT
