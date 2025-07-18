#!/bin/bash
export PORT=${PORT:-5000}
python3 -c "import os; os.environ['PORT'] = str($PORT); exec(open('main.py').read())"
