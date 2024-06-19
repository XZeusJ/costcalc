from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint

from costcalc.extensions import db, login_manager
from costcalc.constants import (CUSTOMER_TYPE_MAPPING, PAYMENT_TERM_MAPPING, 
                       CUSTOMER_IMPORTANCE_MAPPING, ESTIMATED_PURCHASE_AMOUNT_MAPPING, 
                       REGION_PRICE_MAPPING, CUSTOMER_PROSPECT_MAPPING, 
                       PRODUCT_RISK_MAPPING, TECHNICAL_QUALITY_REQUIREMENT_MAPPING, 
                       CUSTOMIZATION_REQUIREMENT_MAPPING)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)  # "admin" or "sales" or "guest"
    products = db.relationship('Product', back_populates='user') # 定义关系属性
    materials = db.relationship('Material', backref='user', lazy=True)
    labors = db.relationship('Labor', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)

    ## User 一对多 Product
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #定义外键：product表相对于user表为多侧
    user = db.relationship('User', back_populates='products')

    ## Product 多对多 material、labor
    materials = db.relationship('ProductMaterial') #定义关系属性：product表相对于这两张表为一侧
    labors = db.relationship('ProductLabor') #这两张表为中间表，用来构建多对多关系
    
    # 运输费
    trans_method = db.Column(db.String(20),  nullable=True)
    trans_dest = db.Column(db.String(20),  nullable=True)
    trans_cost_kg = db.Column(db.Float, default=1.0)

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
    
    # 新增字段
    customer_type = db.Column(db.Float, nullable=False, default=1.0)
    payment_term = db.Column(db.Float, nullable=False, default=1.0)
    customer_importance = db.Column(db.Float, nullable=False, default=1.0)
    estimated_purchase_amount = db.Column(db.Float, nullable=False, default=1.0)
    region_price = db.Column(db.Float, nullable=False, default=1.0)
    customer_prospect = db.Column(db.Float, nullable=False, default=1.0)
    product_risk = db.Column(db.Float, nullable=False, default=1.0)
    technical_quality_requirement = db.Column(db.Float, nullable=False, default=1.0)
    customization_requirement = db.Column(db.Float, nullable=False, default=1.0)

    @property
    def total_cost(self):
        total_discount = (self.customer_type * self.payment_term * self.customer_importance * 
                          self.estimated_purchase_amount * self.region_price * 
                          self.customer_prospect * self.product_risk * 
                          self.technical_quality_requirement * self.customization_requirement)
        
        return self.post_tax_cost * total_discount
    
    @property # 原材料费
    def material_cost(self):
       return sum(pm.ttl for pm in self.materials)

    @property # 人工费
    def labor_cost(self):
        return sum(pl.ttl for pl in self.labors)

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

    @property
    def materials_dict(self):
        return [
            {
                '材料名称': pm.material.name,
                '材料规格': pm.material.spec,
                '单价/g': pm.material.unit_price,
                '材料净重': pm.net_weight,
                '材料毛边': pm.gross_weight,
                '材料毛重': pm.total_weight,
                '合格率': pm.qualification_rate,
                'TTL(CNY)': round(pm.ttl, 4)
            }
            for pm in self.materials
        ]

    @property
    def labors_dict(self):
        return [
            {
                '工序': pl.labor.name,
                '设备折旧': pl.labor.deprec_cost,
                '电费CNY/H': pl.labor.elec_cost,
                '人工CNY/H': pl.labor.labor_cost,
                '工序工时/秒': pl.process_time,
                '产能/次': pl.capacity,
                '合格率': pl.qualification_rate,
                'TTL(CNY)': round(pl.ttl, 4)
            }
            for pl in self.labors
        ]

    @property
    def trans_dict(self):
        return {
            '运输方式': self.trans_method,
            '目的地': self.trans_dest,
            '运输费/KG': self.trans_cost_kg,
            '运输费/个': round(self.trans_cost, 6),
        }

    @property
    def coef_dict(self):
        return {
            '研发费用': self.dev_coef,
            '厂房费用': self.fac_coef,
            '管理费': self.admin_coef,
            '销售费': self.sale_coef,
            '财务费': self.finance_coef,
            '其他税款': self.tax_coef,
            '利润': self.profit_coef
        }

    @property
    def customization_dict(self):
        return {
            '客户类型': CUSTOMER_TYPE_MAPPING.get(self.customer_type, '未知类型'),
            '支付条款': PAYMENT_TERM_MAPPING.get(self.payment_term, '未知条款'),
            '客户重要性': CUSTOMER_IMPORTANCE_MAPPING.get(self.customer_importance, '未知重要性'),
            '预计采购金额': ESTIMATED_PURCHASE_AMOUNT_MAPPING.get(self.estimated_purchase_amount, '未知金额'),
            '区域价格': REGION_PRICE_MAPPING.get(self.region_price, '未知价格'),
            '客户前景': CUSTOMER_PROSPECT_MAPPING.get(self.customer_prospect, '未知前景'),
            '产品风险': PRODUCT_RISK_MAPPING.get(self.product_risk, '未知风险'),
            '技术及品质要求': TECHNICAL_QUALITY_REQUIREMENT_MAPPING.get(self.technical_quality_requirement, '未知要求'),
            '特殊定制要求': CUSTOMIZATION_REQUIREMENT_MAPPING.get(self.customization_requirement, '未知定制')
        }
    
    @property
    def cost_dict(self):
        return {
            '材料费': round(self.material_cost, 3),
            '人工费': round(self.labor_cost, 3),
            '运输费': round(self.trans_cost, 3),
            '税前': round(self.pre_tax_cost, 6),
            '税后': round(self.post_tax_cost, 6),
            '总成本': round(self.total_cost, 6)
        }

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'user_name': self.user.username if self.user else None,  # 安全地访问用户名
            'trans_method': self.trans_method,
            'trans_dest': self.trans_dest,
            'trans_cost_kg': self.trans_cost_kg,
            'dev_coef': self.dev_coef,
            'fac_coef': self.fac_coef,
            'admin_coef': self.admin_coef,
            'sale_coef': self.sale_coef,
            'finance_coef': self.finance_coef,
            'tax_coef': self.tax_coef,
            'profit_coef': self.profit_coef,
            'material_cost': round(self.material_cost, 1),
            'labor_cost': round(self.labor_cost, 1),
            'trans_cost': round(self.trans_cost, 1),
            'pre_tax_cost': round(self.pre_tax_cost, 1),
            'post_tax_cost': round(self.post_tax_cost, 1),
            'total_cost': round(self.total_cost, 3),
            'materials': [pm.to_dict() for pm in self.materials],
            'labors': [pl.to_dict() for pl in self.labors]
        }


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    spec = db.Column(db.String(20), default = '')
    unit_price = db.Column(db.Float, default = 0.0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 添加用户外键

    __table_args__ = (UniqueConstraint('name', 'spec', name='_name_spec_uc'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.username if self.user else None,  # 安全地访问用户名
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 添加用户外键

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.username if self.user else None,  # 安全地访问用户名
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

    @property
    def total_weight(self):
        return self.net_weight + self.gross_weight

    @property
    def ttl(self):
        return self.total_weight * self.material.unit_price / self.qualification_rate

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'material_id': self.material_id,
            'net_weight': self.net_weight,
            'gross_weight': self.gross_weight,
            'qualification_rate': self.qualification_rate,
            'material': self.material.to_dict() if self.material else None
        }

class ProductLabor(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
    labor_id = db.Column(db.Integer, db.ForeignKey('labor.id'), primary_key=True)
    labor = db.relationship('Labor')

    process_time = db.Column(db.Float, default = 0.0)
    capacity = db.Column(db.Float, default = 1.0)
    qualification_rate = db.Column(db.Float, default = 1.0)

    @property
    def ttl(self):
        sl = self.labor
        return (sl.deprec_cost + sl.elec_cost + sl.labor_cost)* self.process_time /3600/self.capacity/self.qualification_rate

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'labor_id': self.labor_id,
            'process_time': self.process_time,
            'capacity': self.capacity,
            'qualification_rate': self.qualification_rate,
            'labor': self.labor.to_dict() if self.labor else None
        }
