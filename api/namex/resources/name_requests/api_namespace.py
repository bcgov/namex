from flask_restx import Namespace

# Register a local namespace for the NR reserve
api = Namespace('nameRequest', description='API for Public Facing Name Requests')
