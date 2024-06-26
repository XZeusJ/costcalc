from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from costcalc.extensions import db
from costcalc.models import Material, Labor
from costcalc.forms import MaterialForm, LaborForm
from costcalc.decorators import admin_required
from sqlalchemy.exc import IntegrityError

resources_bp = Blueprint('resources', __name__)

## 材料表CURD
@resources_bp.route('/material/manage')
@admin_required
def manage_material():
    material_form = MaterialForm()
    return render_template('resources/manage_material.html', material_form=material_form)

@resources_bp.route('/material/get')
@admin_required
def get_materials():
    materials = Material.query.all()
    materials_list = [material.to_dict() for material in materials]
    return jsonify(materials_list)

@resources_bp.route('/material/specs')
def material_specs():
    material_name = request.args.get('name')
    materials = Material.query.filter_by(name=material_name).all()
    specs = [{'id': material.id, 'spec': material.spec} for material in materials]
    return jsonify(specs)

from sqlalchemy.exc import IntegrityError

@resources_bp.route('/material/new', methods=['POST'])
def new_material():
    form = MaterialForm()
    if form.validate_on_submit():
        material = Material(user_id=current_user.id)
        form.populate_obj(material)
        try:
            db.session.add(material)
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Material created.', 'material': material.to_dict()})
        except IntegrityError:
            db.session.rollback()
            return jsonify({'status': 'fail', 'message': '这个材料规格已经存在.'}), 409  # 409 Conflict
    return jsonify({'status': 'fail', 'message': 'Validation failed.', 'errors': form.errors}), 400


@resources_bp.route('/material/<int:material_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_material(material_id):
    material = Material.query.get_or_404(material_id)
    form = MaterialForm(obj=material)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(material)
        db.session.commit()
        return jsonify(status="success", message="Material updated successfully", material=material.to_dict())
    return render_template('resources/edit_material_form.html', form=form, material_id=material_id)

@resources_bp.route('/material/<int:material_id>/delete', methods=['DELETE'])
@admin_required
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    return '', 204

## 人工表CURD
@resources_bp.route('/labor/manage')
@admin_required
def manage_labor():
    labor_form = LaborForm()
    return render_template('resources/manage_labor.html', labor_form=labor_form)

@resources_bp.route('/labor/get')
@admin_required
def get_labor():
    labors = Labor.query.all()
    labors_list = [labor.to_dict() for labor in labors]
    return jsonify(labors_list)

@resources_bp.route('/labor/new', methods=['POST'])
def new_labor():
    form = LaborForm()
    if form.validate_on_submit():
        labor = Labor(user_id = current_user.id)
        form.populate_obj(labor)
        db.session.add(labor)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Labor created.', 'labor': labor.to_dict(), 'new_labor': {'id': labor.id, 'name': labor.name}})
    return jsonify({'status': 'fail', 'message': 'Validation failed.', 'errors': form.errors}), 400

@resources_bp.route('/labor/<int:labor_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_labor(labor_id):
    labor = Labor.query.get_or_404(labor_id)
    form = LaborForm(obj=labor)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(labor)
        db.session.commit()
        return jsonify(status="success", message="Labor updated successfully", labor=labor.to_dict())
    return render_template('resources/edit_labor_form.html', form=form, labor_id=labor_id)

@resources_bp.route('/labor/<int:labor_id>/delete', methods=['DELETE'])
@admin_required
def delete_labor(labor_id):
    labor = Labor.query.get_or_404(labor_id)
    db.session.delete(labor)
    db.session.commit()
    return '', 204