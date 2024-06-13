from tests.test_basic import BasicTestCase
from flask import url_for
from costcalc.models import Material, Labor
from costcalc.extensions import db

class TestMaterial(BasicTestCase):

    def test_material_manage(self):
        """测试管理材料页面的加载"""
        response = self.client.get(url_for('resources.manage_material'))
        self.assertEqual(response.status_code, 200)

    def test_new_material(self):
        """测试创建新材料"""
        response = self.client.post(url_for('resources.new_material'), data={
            'name': 'Polyethylene',
            'spec': 'High Density',
            'unit_price': 1.5
        }, follow_redirects=True)
        self.assertIn('Material created.', response.data.decode())

    def test_edit_material(self):
        """测试编辑材料"""
        # 创建一个材料
        material = Material(name="Polypropylene", spec="Medium Density", unit_price=1.2)
        db.session.add(material)
        db.session.commit()

        # 编辑这个材料
        response = self.client.post(url_for('resources.edit_material', material_id=material.id), data={
            'name': 'Polypropylene',
            'spec': 'High Density',
            'unit_price': 1.3
        }, follow_redirects=True)
        self.assertIn('Material updated.', response.data.decode())

    def test_delete_material(self):
        """测试删除材料"""
        # 创建一个材料
        material = Material(name="PVC", spec="Flexible", unit_price=0.8)
        db.session.add(material)
        db.session.commit()

        # 删除这个材料
        response = self.client.delete(url_for('resources.delete_material', material_id=material.id))
        self.assertEqual(response.status_code, 204)

class TestLabor(BasicTestCase):

    def test_labor_manage(self):
        """测试管理人工页面的加载"""
        response = self.client.get(url_for('resources.manage_labor'))
        self.assertEqual(response.status_code, 200)

    def test_new_labor(self):
        """测试创建新人工"""
        response = self.client.post(url_for('resources.new_labor'), data={
            'name': 'Welding',
            'deprec_cost': 0.2,
            'elec_cost': 0.1,
            'labor_cost': 15.0
        }, follow_redirects=True)
        self.assertIn('Labor created.', response.data.decode())

    def test_edit_labor(self):
        """测试编辑人工"""
        # 创建一个人工
        labor = Labor(name="Casting", deprec_cost=0.1, elec_cost=0.05, labor_cost=10)
        db.session.add(labor)
        db.session.commit()

        # 编辑这个人工
        response = self.client.post(url_for('resources.edit_labor', labor_id=labor.id), data={
            'name': 'Casting',
            'deprec_cost': 0.15,
            'elec_cost': 0.1,
            'labor_cost': 12
        }, follow_redirects=True)
        self.assertIn('Labor updated.', response.data.decode())

    def test_delete_labor(self):
        """测试删除人工"""
        # 创建一个人工
        labor = Labor(name="Painting", deprec_cost=0.2, elec_cost=0.1, labor_cost=20)
        db.session.add(labor)
        db.session.commit()

        # 删除这个人工
        response = self.client.delete(url_for('resources.delete_labor', labor_id=labor.id))
        self.assertEqual(response.status_code, 204)