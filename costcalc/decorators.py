from flask import abort, request, jsonify, redirect, url_for, flash
from flask_login import current_user
from functools import wraps
from costcalc.models import Product

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            flash('You do not have permission to access this resource.', 'danger')
            return redirect(url_for('products.index'))
        return f(*args, **kwargs)
    return decorated_function

def sales_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != 'sales':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

def check_permission(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        product_id = kwargs.get('product_id')
        product = Product.query.get_or_404(product_id)
        if current_user.role != 'admin' and product.user_id != current_user.id:
            if request.path.endswith('/delete'):
                return jsonify({'error': 'You do not have permission'}), 403
            flash('You do not have permission to access this resource.', 'danger')
            return redirect(url_for('products.index'))
        return f(*args, **kwargs)
    return decorated_function