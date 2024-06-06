from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from costcalc.extensions import db
from costcalc.models import Product, ProductMaterial, ProductLabor
from costcalc.forms import ProductForm, ProductMaterialForm, ProductLaborForm, Material
from costcalc.utils import redirect_back

products_bp = Blueprint('products', __name__)

@products_bp.route('/')
def index():
    return redirect(url_for('.manage_product'))

@products_bp.route('/product/manage')
def manage_product():
    products = Product.query.all()
    products_list = [product.to_dict() for product in products]
    return render_template('products/manage_product.html', products=products_list)

@products_bp.route('/product/<int:product_id>/detail')
def detail_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/detail_product.html', product = product)


@products_bp.route('/product/new', methods=['GET', 'POST'])
def new_product():
    form = ProductForm()
    
    if form.validate_on_submit():
        new_product = Product(
            name=form.name.data,
            user_id = 1, 
            trans_method=form.trans_method.data,
            trans_dest=form.trans_dest.data,
            trans_cost_kg=form.trans_cost_kg.data,
            dev_coef=form.dev_coef.data,
            fac_coef=form.fac_coef.data,
            admin_coef=form.admin_coef.data,
            sale_coef=form.sale_coef.data,
            finance_coef=form.finance_coef.data,
            tax_coef=form.tax_coef.data,
            profit_coef=form.profit_coef.data
        )
        db.session.add(new_product)
        db.session.commit()

        # 处理动态添加的ProductMaterialForms
        for key in request.form:
            if key.startswith('material_choices-') and key.endswith('-material_choices'):
                suffix = key.split('-')[1]
                material_id = request.form.get(f'material_choices-{suffix}-material_choices')
                net_weight = request.form.get(f'material_choices-{suffix}-net_weight')
                gross_weight = request.form.get(f'material_choices-{suffix}-gross_weight')
                qualification_rate = request.form.get(f'material_choices-{suffix}-qualification_rate')
                new_product_material = ProductMaterial(
                    product_id=new_product.id,
                    material_id=material_id,
                    net_weight=net_weight,
                    gross_weight=gross_weight,
                    qualification_rate=qualification_rate
                )
                db.session.add(new_product_material)

        # 处理动态添加的ProductLaborForms
        for key in request.form:
            if key.startswith('labor_choices-') and key.endswith('-labor_choices'):
                suffix = key.split('-')[1]
                labor_id = request.form.get(f'labor_choices-{suffix}-labor_choices')
                process_time = request.form.get(f'labor_choices-{suffix}-process_time')
                capacity = request.form.get(f'labor_choices-{suffix}-capacity')
                qualification_rate = request.form.get(f'labor_choices-{suffix}-qualification_rate')
                new_product_labor = ProductLabor(
                    product_id=new_product.id,
                    labor_id=labor_id,
                    process_time=process_time,
                    capacity=capacity,
                    qualification_rate=qualification_rate
                )
                db.session.add(new_product_labor)

        db.session.commit()
        flash('Product created.', 'success')
        return redirect(url_for('products.detail_product', product_id = new_product.id))
    return render_template('products/new_product.html', form = form)

@products_bp.route('/productmaterial/new')
def new_pmform():
    pmform = ProductMaterialForm(prefix="material_choices-__prefix__-")
    return render_template('products/_pmform.html', form = pmform)

@products_bp.route('/productlabor/new')
def new_plform():
    plform = ProductLaborForm(prefix="labor_choices-__prefix__-")
    return render_template('products/_plform.html', form = plform)

@products_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    pms = ProductMaterial.query.filter_by(product_id=product_id).all()
    pmforms = [ProductMaterialForm(prefix=f'pmform-{i}', obj=pm) for i, pm in enumerate(pms)]

    pls = ProductLabor.query.filter_by(product_id=product_id).all()
    plforms = [ProductLaborForm(prefix=f'plform-{i}', obj=pl) for i, pl in enumerate(pls)]

    if form.validate_on_submit():
        form.populate_obj(product)
        for pmform, pm in zip(pmforms, pms):
            pmform.populate_obj(pm)
        for plform, pl in zip(plforms, pls):
            plform.populate_obj(pl)

        db.session.commit()
        flash('Product updated.', 'success')
        return redirect(url_for('products.detail_product', product_id = product_id))
    
    return render_template('products/edit_product.html', form=form, pmforms=pmforms, plforms=plforms, product=product)

@products_bp.route('/product/<int:product_id>/delete', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    product_materials = ProductMaterial.query.filter_by(product_id=product_id).all()
    product_labors = ProductLabor.query.filter_by(product_id=product_id).all()
    for pm in product_materials:
        db.session.delete(pm)
    for pl in product_labors:
        db.session.delete(pl)
    db.session.delete(product)
    db.session.commit()
    
    flash('Product and its associated materials and labors deleted.', 'success')
    return '', 204