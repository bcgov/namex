from flask_cors import cross_origin
from flask_restx import Namespace

# Register a local namespace for the NR reserve
api = Namespace('nameAnalysis', description='API for Analysing BC Names', decorators=[cross_origin()])
