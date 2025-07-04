from flask_restx import Namespace

# Register a local namespace for the NR reserve
api = Namespace('Payments', description='API for making payments using SBC Pay')
