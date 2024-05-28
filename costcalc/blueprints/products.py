from flask import Blueprint

products_bp = Blueprint('products', __name__)

@products_bp.route('/home')
def hello():
    return 'Welcom to products home hh'