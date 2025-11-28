# Lightweight runner to start the project without package-mode requirements
import os
import sys
# Ensure the repository root is on sys.path so `src` can be imported
ROOT = os.path.dirname(__file__)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.main import main

if __name__ == '__main__':
    main()
