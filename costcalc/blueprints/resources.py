from flask import Blueprint, render_template, jsonify, request
from costcalc.extensions import db
from costcalc.models import Material, Labor
from costcalc.forms import MaterialForm, LaborForm

resources_bp = Blueprint('resources', __name__)

## 材料表CURD
@resources_bp.route('/material/manage')
def manage_material():
    materials = Material.query.all()
    materials_list = [material.to_dict() for material in materials]
    form = MaterialForm()
    return render_template('resources/manage_material.html', materials = materials_list, form=form)

@resources_bp.route('/material/new', methods=['POST'])
def new_material():
    form = MaterialForm()
    if form.validate_on_submit():
        material = Material()
        form.populate_obj(material)
        db.session.add(material)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Material created.', 'material': material.to_dict()})
    return jsonify({'status': 'fail', 'message': 'Validation failed.', 'errors': form.errors}), 400


@resources_bp.route('/material/<int:material_id>/edit', methods=['GET', 'POST'])
def edit_material(material_id):
    material = Material.query.get_or_404(material_id)
    form = MaterialForm(obj=material)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(material)
        db.session.commit()
        return jsonify(status="success", message="Material updated successfully", material=material.to_dict())
    return render_template('resources/edit_material_form.html', form=form, material_id=material_id)

@resources_bp.route('/material/<int:material_id>/delete', methods=['DELETE'])
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    return '', 204

## 人工表CURD
@resources_bp.route('/labor/manage')
def manage_labor():
    labors = Labor.query.all()
    labors_list = [labor.to_dict() for labor in labors]
    form = LaborForm()
    return render_template('resources/manage_labor.html', labors=labors_list, form=form)

@resources_bp.route('/labor/new', methods=['POST'])
def new_labor():
    form = LaborForm()
    if form.validate_on_submit():
        labor = Labor()
        form.populate_obj(labor)
        db.session.add(labor)
        db.session.commit()
        return jsonify({'status': 'success', 'message': 'Labor created.', 'labor': labor.to_dict()})
    return jsonify({'status': 'fail', 'message': 'Validation failed.', 'errors': form.errors}), 400

@resources_bp.route('/labor/<int:labor_id>/edit', methods=['GET', 'POST'])
def edit_labor(labor_id):
    labor = Labor.query.get_or_404(labor_id)
    form = LaborForm(obj=labor)
    if request.method == 'POST' and form.validate_on_submit():
        form.populate_obj(labor)
        db.session.commit()
        return jsonify(status="success", message="Labor updated successfully", labor=labor.to_dict())
    return render_template('resources/edit_labor_form.html', form=form, labor_id=labor_id)

@resources_bp.route('/labor/<int:labor_id>/delete', methods=['DELETE'])
def delete_labor(labor_id):
    labor = Labor.query.get_or_404(labor_id)
    db.session.delete(labor)
    db.session.commit()
    return '', 204