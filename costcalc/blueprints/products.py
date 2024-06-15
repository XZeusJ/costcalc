from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user   
from costcalc.extensions import db
from costcalc.models import Product, ProductMaterial, ProductLabor
from costcalc.forms import ProductForm, ProductMaterialForm, ProductLaborForm
from costcalc.decorators import admin_required, sales_required, check_permission



products_bp = Blueprint('products', __name__)


@products_bp.route('/')
@login_required
def index():
    return redirect(url_for('.manage_product'))

@products_bp.route('/product/manage')
@login_required
def manage_product():
    return render_template('products/manage_product.html')

@products_bp.route('/product/get')
@login_required
def get_products():
    if current_user.role == 'admin':
        products = Product.query.all()
    else:
        products = Product.query.filter_by(user_id=current_user.id).all()
    products_list = [product.to_dict() for product in products]
    return jsonify(products_list)

@products_bp.route('/product/<int:product_id>/detail')
@login_required
@check_permission
def detail_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('products/detail_product.html', product=product)

@products_bp.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductForm()
    
    if form.validate_on_submit():
        new_product = Product(user_id = 1)
        form.populate_obj(new_product)
        db.session.add(new_product)
        
        # 处理动态添加的ProductMaterialForms
        for key in request.form:
            if key.startswith('pmform-') and key.endswith('-material_choices'):
                suffix = key.split('-')[1]
                material_form = ProductMaterialForm(prefix=f"pmform-{suffix}-")
                material = ProductMaterial(product_id=new_product.id, material_id = material_form.material_choices.data)
                material_form.populate_obj(material)
                db.session.add(material)

        # 处理动态添加的ProductLaborForms
        for key in request.form:
            if key.startswith('plform-') and key.endswith('-labor_choices'):
                suffix = key.split('-')[1]
                labor_form = ProductLaborForm(prefix=f"plform-{suffix}-")
                labor = ProductLabor(product_id=new_product.id, labor_id = labor_form.labor_choices.data)
                labor_form.populate_obj(labor)
                db.session.add(labor)

        db.session.commit()
        flash('Product created.', 'success')
        return redirect(url_for('products.detail_product', product_id = new_product.id))
    return render_template('products/new_product.html', form = form)

@products_bp.route('/productmaterial/newform')
@login_required
def new_pmform():
    pmform = ProductMaterialForm(prefix="pmform-__prefix__-")
    return render_template('products/_pmform.html', form = pmform)

@products_bp.route('/productlabor/newform')
@login_required
def new_plform():
    plform = ProductLaborForm(prefix="plform-__prefix__-")
    return render_template('products/_plform.html', form = plform)

@products_bp.route('/product/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@check_permission
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if current_user.role != 'admin' and product.user_id != current_user.id:
        flash('You do not have permission to edit this product.', 'danger')
        return redirect(url_for('products.index'))
    form = ProductForm(obj=product)

    pms = ProductMaterial.query.filter_by(product_id=product_id).all()
    pmforms = []
    for i, pm in enumerate(pms):
        pmform = ProductMaterialForm(prefix=f'pmform-{i}', obj=pm)
        pmform.material_name.data = pm.material.name  # 设置材料名称字段的值
        pmform.materialID.data = pm.material.id  # 设置材料ID字段的值用来在edit_product.html中异步删除pm实例
        pmforms.append(pmform)

    pls = ProductLabor.query.filter_by(product_id=product_id).all()
    plforms = []
    for i, pl in enumerate(pls):
        plform = ProductLaborForm(prefix=f'plform-{i}', obj=pl)
        plform.labor_name.data = pl.labor.name
        plform.laborID.data = pl.labor.id
        plforms.append(plform)

    if form.validate_on_submit():
        # 更改旧表单数据
        form.populate_obj(product)
        for pmform, pm in zip(pmforms, pms):
            pmform.populate_obj(pm)
        for plform, pl in zip(plforms, pls):
            plform.populate_obj(pl)

        # 生成新表单数据
        for key in request.form:
            if key.startswith('pmform-') and key.endswith('-material_choices'):
                suffix = key.split('-')[1]
                material_form = ProductMaterialForm(prefix=f"pmform-{suffix}-")
                material = ProductMaterial(product_id=product_id, material_id = material_form.material_choices.data)
                material_form.populate_obj(material)
                db.session.add(material)

        for key in request.form:
            if key.startswith('plform-') and key.endswith('-labor_choices'):
                suffix = key.split('-')[1]
                labor_form = ProductLaborForm(prefix=f"plform-{suffix}-")
                labor = ProductLabor(product_id=product_id, labor_id = labor_form.labor_choices.data)
                labor_form.populate_obj(labor)
                db.session.add(labor)

        db.session.commit()
        flash('Product updated.', 'success')
        return redirect(url_for('products.detail_product', product_id = product_id))
    
    return render_template('products/edit_product.html', form=form, pmforms=pmforms, plforms=plforms, product=product)

@products_bp.route('/product/<int:product_id>/delete', methods=['DELETE'])
@login_required
@check_permission
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if current_user.role != 'admin' and product.user_id != current_user.id:
        flash('You do not have permission to delete this product.', 'danger')
        return redirect(url_for('.index'))
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

@products_bp.route('/product/<int:product_id>/material/<int:material_id>/delete', methods=['DELETE'])
@login_required
@check_permission
def delete_product_material(product_id, material_id):
    product = Product.query.get_or_404(product_id)
    if current_user.role != 'admin' and product.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to delete this material'}), 403

    product_material = ProductMaterial.query.filter_by(product_id=product_id, material_id=material_id).first()
    if not product_material:
        return jsonify({'error': 'ProductMaterial not found'}), 404

    db.session.delete(product_material)
    db.session.commit()
    return jsonify({'message': 'ProductMaterial deleted'}), 200

@products_bp.route('/product/<int:product_id>/labor/<int:labor_id>/delete', methods=['DELETE'])
@login_required
@check_permission
def delete_product_labor(product_id, labor_id):
    product = Product.query.get_or_404(product_id)
    if current_user.role != 'admin' and product.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to delete this material'}), 403


    product_labor = ProductLabor.query.filter_by(product_id=product_id, labor_id=labor_id).first()
    if not product_labor:
        return jsonify({'error': 'ProductLabor not found'}), 404

    db.session.delete(product_labor)
    db.session.commit()
    return jsonify({'message': 'ProductLabor deleted'}), 200

