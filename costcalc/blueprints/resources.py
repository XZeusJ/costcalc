from flask import Blueprint, render_template, flash, redirect, url_for
from costcalc.extensions import db
from costcalc.models import Material, Labor
from costcalc.forms import MaterialForm, LaborForm
from costcalc.utils import redirect_back

resources_bp = Blueprint('resources', __name__)

# @resources_bp.route('/resources')
# def home():
#     materials = Material.query.all()
#     materials_list = [material.to_dict() for material in materials]
#     return render_template('resources/home.html', materials = materials_list)

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
        name = form.name.data
        spec = form.spec.data
        unit_price = form.unit_price.data
        material = Material(name = name, spec = spec, unit_price = unit_price)
        db.session.add(material)
        db.session.commit()
        flash('Material created.', 'success')
        return redirect(url_for('resources.manage_material'))
    return render_template('resources/new_material.html', form = form)

@resources_bp.route('/material/<int:material_id>/edit', methods=['GET', 'POST'])
def edit_material(material_id):
    form = MaterialForm()
    material = Material.query.get_or_404(material_id)
    if form.validate_on_submit():
        material.name = form.name.data
        material.spec = form.spec.data
        material.unit_price = form.unit_price.data
        db.session.add(material)
        db.session.commit()
        flash('Material updated.', 'success')
        return redirect(url_for('resources.manage_material'))
    form.name.data = material.name
    form.spec.data = material.spec
    form.unit_price.data = material.unit_price
    return render_template('resources/edit_material.html', form = form)


@resources_bp.route('/material/<int:material_id>/delete', methods=['DELETE'])
def delete_material(material_id):
    material = Material.query.get_or_404(material_id)
    db.session.delete(material)
    db.session.commit()
    flash('Material deleted.', 'success')
    return '', 204
    # return redirect_back()

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
        name = form.name.data
        deprec_cost = form.deprec_cost.data
        elec_cost = form.elec_cost.data
        labor_cost = form.labor_cost.data
        labor = Labor(name=name, deprec_cost=deprec_cost, elec_cost=elec_cost, labor_cost=labor_cost)
        db.session.add(labor)
        db.session.commit()
        flash('Labor created.', 'success')
        return redirect(url_for('resources.manage_labor'))
    return render_template('resources/new_labor.html', form = form)

@resources_bp.route('/labor/<int:labor_id>/edit', methods=['GET', 'POST'])
def edit_labor(labor_id):
    form = LaborForm()
    labor = Labor.query.get_or_404(labor_id)
    if form.validate_on_submit():
        labor.name = form.name.data
        labor.deprec_cost = form.deprec_cost.data
        labor.elec_cost = form.elec_cost.data
        labor.labor_cost = form.labor_cost.data
        db.session.add(labor)
        db.session.commit()
        flash('Labor updated.', 'success')
        return redirect(url_for('resources.manage_labor'))
    form.name.data = labor.name
    form.deprec_cost.data = labor.deprec_cost
    form.elec_cost.data = labor.elec_cost
    form.labor_cost.data = labor.labor_cost
    return render_template('resources/edit_labor.html', form = form)


@resources_bp.route('/labor/<int:labor_id>/delete', methods=['DELETE'])
def delete_labor(labor_id):
    labor = Labor.query.get_or_404(labor_id)
    db.session.delete(labor)
    db.session.commit()
    flash('Labor deleted.', 'success')
    return '', 204