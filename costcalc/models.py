from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from costcalc.extensions import db, login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    products = db.relationship('Product', back_populates='user') # 定义关系属性

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):

    ## 定义只和该product相关的参数
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    ## 定义product和user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #定义外键：product表相对于user表为多侧
    user = db.relationship('User', back_populates='products')

    ## material、labor表的关系
    materials = db.relationship('ProductMaterial') #定义关系属性：product表相对于这两张表为一侧
    labors = db.relationship('ProductLabor') #这两张表为中间表，用来构建多对多关系
    
    # 运输费
    trans_method = db.Column(db.String(20),  nullable=True)
    trans_dest = db.Column(db.String(20),  nullable=True)
    trans_cost_kg = db.Column(db.Float, default=0.0)

    # 模具费、打样上机费
    # mold = db.Column(db.Float, default=0.0)
    # typing = db.Column(db.Float, default=0.0)

    # 项目系数
    dev_coef = db.Column(db.Float, default=0.0)
    fac_coef = db.Column(db.Float, default=5.0)
    admin_coef = db.Column(db.Float, default=10.0)
    sale_coef = db.Column(db.Float, default=3.0)
    finance_coef = db.Column(db.Float, default=1.5)
    tax_coef = db.Column(db.Float, default=0.0)
    profit_coef = db.Column(db.Float, default=12.0)
    
    @property # 原材料费
    def material_cost(self):
        cost = 0
        for pm in self.materials:
            m = pm.material
            cost += m.unit_price * (pm.net_weight+pm.gross_weight) / pm.qualification_rate
        print
        return cost
    
    @property # 人工费
    def labor_cost(self):
        cost = 0
        for pl in self.labors:
            l = pl.labor
            cost += (l.deprec_cost+l.elec_cost+l.labor_cost)*pl.process_time/3600/pl.capacity/pl.qualification_rate
        return cost

    @property # 运输费
    def trans_cost(self):
        total_net_weight = sum(pm.net_weight for pm in self.materials)
        cost = total_net_weight/1000/self.trans_cost_kg
        return cost
    
    @property # 未税价
    def pre_tax_cost(self):
        cost = self.material_cost + self.labor_cost + self.trans_cost
        coef = self.dev_coef + self.fac_coef + self.admin_coef + self.sale_coef + self.finance_coef + self.tax_coef + self.profit_coef
        return cost/((100-coef)/100)

    @property # 含税价
    def post_tax_cost(self):
        return self.pre_tax_cost*1.13


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    spec = db.Column(db.String(20))
    unit_price = db.Column(db.Float, default = 0.0)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'spec': self.spec,
            'unit_price': self.unit_price
        }

class Labor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    deprec_cost = db.Column(db.Float, default = 0.0)
    elec_cost = db.Column(db.Float, default = 0.0)
    labor_cost = db.Column(db.Float, default = 0.0)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'deprec_cost': self.deprec_cost,
            'elec_cost': self.elec_cost,
            'labor_cost': self.labor_cost
        }

class ProductMaterial(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('material.id'), primary_key=True)
    material = db.relationship('Material') #这两行是多对一关系的写法

    net_weight = db.Column(db.Float, default = 0.0)
    gross_weight = db.Column(db.Float, default = 0.0)
    qualification_rate = db.Column(db.Float, default = 1.0)

class ProductLabor(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    labor_id = db.Column(db.Integer, db.ForeignKey('labor.id'), primary_key=True)
    labor = db.relationship('Labor')

    process_time = db.Column(db.Float, default = 0.0)
    capacity = db.Column(db.Float, default = 0.0)
    qualification_rate = db.Column(db.Float, default = 1.0)
