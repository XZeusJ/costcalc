from flask import Blueprint, render_template, flash, redirect, url_for
from costcalc.extensions import db
from costcalc.models import Product
from costcalc.forms import ProductForm
from costcalc.utils import redirect_back

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def index():
    return redirect(url_for('.manage_product'))

@products_bp.route('/product/manage')
def manage_product():

    product_a = Product.query.filter_by(name='新产品').first()
    price_a = product_a.post_tax_cost

    product_b = Product.query.filter_by(name='二十柱').first()
    price_b = product_b.post_tax_cost

    fstr = f"{product_a.material_cost} - {product_a.labor_cost} - {product_a.trans_cost} <br>\
    Price of 新产品: {price_a}<br>\
    {product_b.material_cost} - {product_b.labor_cost} - {product_b.trans_cost} <br>\
    Price of 二十柱: {price_b}"
    return render_template('products/manage_product.html', fstr = fstr)

@products_bp.route('/product/new', methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    return render_template('products/new_product.html', form = form)

@products_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product():
    form = ProductForm()
    return render_template('products/edit_product.html', form = form)


@products_bp.route('/product/<int:product_id>/delete', methods=['DELETE'])
def delete_product(product_id):
    return redirect_back()