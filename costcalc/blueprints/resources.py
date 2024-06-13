from flask import Blueprint, render_template, flash, redirect, url_for
from costcalc.extensions import db
from costcalc.models import Material, Labor
from costcalc.forms import MaterialForm, LaborForm

resources_bp = Blueprint('resources', __name__)

## 材料表CURD
@resources_bp.route('/material/manage')
def manage_material():
    materials = Material.query.all()
    materials_list = [material.to_dict() for material in materials]
    return render_template('resources/manage_material.html', materials = materials_list)

@resources_bp.route('/material/new', methods=['GET', 'POST'])
def new_material():
    form = MaterialForm()
    if form.validate_on_submit():
        material = Material()
        form.populate_obj(material)
        db.session.add(material)
        db.session.commit()
        flash('Material created.', 'success')
        return redirect(url_for('resources.manage_material'))
    return render_template('resources/new_material.html', form = form)

@resources_bp.route('/material/<int:material_id>/edit', methods=['GET', 'POST'])
def edit_material(material_id):
    material = Material.query.get_or_404(material_id)
    form = MaterialForm(obj=material)
    if form.validate_on_submit():
        form.populate_obj(material)
        db.session.add(material)
        db.session.commit()
        flash('Material updated.', 'success')
        return redirect(url_for('resources.manage_material'))
    return render_template('resources/edit_material.html', form = form)


@resources_bp.route('/material/<int:material_id>/delete', methods=['DELETE'])
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash('Material deleted.', 'success')
    return '', 204

## 人工表CURD
@resources_bp.route('/labor/manage')
def manage_labor():
    labors = Labor.query.all()
    labors_list = [labor.to_dict() for labor in labors]
    return render_template('resources/manage_labor.html', labors = labors_list)
 
@resources_bp.route('/labor/new', methods=['GET', 'POST'])
def new_labor():
    form = LaborForm()
    if form.validate_on_submit():
        labor = Labor()
        form.populate_obj(labor)
        db.session.add(labor)
        db.session.commit()
        flash('Labor created.', 'success')
        return redirect(url_for('resources.manage_labor'))
    return render_template('resources/new_labor.html', form = form)

@resources_bp.route('/labor/<int:labor_id>/edit', methods=['GET', 'POST'])
def edit_labor(labor_id):
    labor = Labor.query.get_or_404(labor_id)
    form = LaborForm(obj=labor)
    if form.validate_on_submit():
        form.populate_obj(labor)
        db.session.add(labor)
        db.session.commit()
        flash('Labor updated.', 'success')
        return redirect(url_for('resources.manage_labor'))
    return render_template('resources/edit_labor.html', form = form)


@resources_bp.route('/labor/<int:labor_id>/delete', methods=['DELETE'])
def delete_labor(labor_id):
    labor = Labor.query.get_or_404(labor_id)
    db.session.delete(labor)
    db.session.commit()
    flash('Labor deleted.', 'success')
    return '', 204