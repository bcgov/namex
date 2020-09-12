from flask_restplus import Namespace

# Register a local namespace for the NR reserve
api = Namespace('payments', description='API for Making Payments Using SBC Pay')
