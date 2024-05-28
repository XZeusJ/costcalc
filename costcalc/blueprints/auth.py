from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/')
def hello():
    return 'Welcom to CostCalc hh'