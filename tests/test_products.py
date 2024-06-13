# test_products.py

from tests.test_basic import BasicTestCase
from costcalc.extensions import db
from costcalc.models import Product, Material, Labor, ProductMaterial, ProductLabor
from flask import url_for
import json

class TestProduct(BasicTestCase):

    def test_product_management_page(self):
        """测试产品管理页面加载是否正确"""
        response = self.client.get('/product/manage')
        self.assertEqual(response.status_code, 200)
        self.assertIn('产品管理', response.data.decode())

    def test_create_product(self):
        """测试新建产品"""
        with self.client:
            response = self.client.post('/product/new', data={
                'name': 'New Test Product',
                'trans_method': '陆运',
                'trans_dest': '测试地点',
                'trans_cost_kg': 10
            }, follow_redirects=True)
            self.assertIn('Product created', response.data.decode())
            self.assertEqual(response.status_code, 200)

    def test_product_detail(self):
        """测试产品详情页面是否正确显示产品详细信息"""
        # 首先创建一个产品及其相关的材料和劳务
        new_product = Product(
            name='Test Product',
            user_id=1,  # 假设用户ID为1已经存在
            trans_method="陆运",
            trans_dest="测试地点",
            trans_cost_kg=10,
            dev_coef=10,
            fac_coef=5,
            admin_coef=3,
            sale_coef=2,
            finance_coef=1,
            tax_coef=0.5,
            profit_coef=15
        )
        db.session.add(new_product)
        db.session.flush()  # 用 flush 而不是 commit 来获取 new_product 的 ID

        # 添加材料和劳务
        material = Material(name="Material1", spec="Spec1", unit_price=100)
        labor = Labor(name="Labor1", deprec_cost=10, elec_cost=5, labor_cost=50)
        db.session.add(material)
        db.session.add(labor)
        db.session.flush()

        new_product_material = ProductMaterial(product_id=new_product.id, material_id=material.id, net_weight=100, gross_weight=150)
        new_product_labor = ProductLabor(product_id=new_product.id, labor_id=labor.id, process_time=360, capacity=1)
        db.session.add(new_product_material)
        db.session.add(new_product_labor)
        db.session.commit()

        # 请求产品详情页面
        response = self.client.get(url_for('products.detail_product', product_id=new_product.id))
        self.assertEqual(response.status_code, 200)
        data = response.data.decode()
        self.assertIn('Test Product', data)
        self.assertIn('Material1', data)
        self.assertIn('Labor1', data)
        self.assertIn('陆运', data)
        self.assertIn('测试地点', data)
        self.assertIn('100.0', data)  # 材料单价
        self.assertIn('50.0', data)  # 劳务成本
        
    def test_edit_product(self):
        """测试编辑产品"""
        # 首先创建一个产品
        new_product = Product(
            name='Original Product',
            user_id=1,  # 假设用户ID为1已经存在
            trans_method="陆运",
            trans_dest="原始地点",
            trans_cost_kg=5
        )
        db.session.add(new_product)
        db.session.commit()

        # 编辑这个产品
        response = self.client.post(url_for('products.edit_product', product_id=new_product.id), data={
            'name': 'Updated Product',
            'trans_method': '空运',
            'trans_dest': '更新地点',
            'trans_cost_kg': 15
        }, follow_redirects=True)
        self.assertIn('Product updated.', response.data.decode())
        self.assertIn('Updated Product', response.data.decode())
        self.assertIn('空运', response.data.decode())

    def test_delete_product(self):
        """测试删除产品"""
        # 首先创建一个产品
        new_product = Product(
            name='Product to Delete',
            user_id=1,  # 假设用户ID为1已经存在
            trans_method="空运",
            trans_dest="删除地点",
            trans_cost_kg=10
        )
        db.session.add(new_product)
        db.session.commit()

        # 确认产品创建成功
        product_in_db = Product.query.filter_by(name='Product to Delete').first()
        self.assertIsNotNone(product_in_db)

        # 删除这个产品
        response = self.client.delete(url_for('products.delete_product', product_id=new_product.id))
        self.assertEqual(response.status_code, 204)

        # 确认产品已被删除
        deleted_product = Product.query.filter_by(name='Product to Delete').first()
        self.assertIsNone(deleted_product)
        

if __name__ == '__main__':
    unittest.main()
