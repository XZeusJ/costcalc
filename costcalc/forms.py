from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError, HiddenField, \
    BooleanField, PasswordField, FloatField, SelectMultipleField, IntegerField
from wtforms.validators import DataRequired, Length, Optional
from costcalc.models import Material, Labor

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class MaterialForm(FlaskForm):
    name = StringField('材料名称', validators=[DataRequired(), Length(1, 20)])
    spec = StringField('材料规格', validators=[Optional(), Length(1, 20)])
    unit_price = FloatField('单价/g', validators=[DataRequired()])
    submit = SubmitField('提交')

class ProductMaterialForm(FlaskForm):
    material_choices = SelectField('选择材料', coerce=int, validators=[DataRequired()])
    material_name = StringField('材料名称', render_kw={'readonly': True})

    materialID = IntegerField('材料id', render_kw={'readonly': True}) #用来传递给edit_product.html

    net_weight = FloatField('材料净重', validators=[Optional()], default=0.0)
    gross_weight = FloatField('材料毛边', validators=[Optional()], default=0.0)
    qualification_rate = FloatField('合格率', validators=[Optional()], default=1.0)

    def __init__(self, *args, **kwargs):
        super(ProductMaterialForm, self).__init__(*args, **kwargs)
        self.material_choices.choices = [(m.id, m.name) for m in Material.query.all()]
        
class LaborForm(FlaskForm):
    name = StringField('工序', validators=[DataRequired(), Length(1, 20)])
    deprec_cost = FloatField('折旧费用', validators=[DataRequired()])
    elec_cost = FloatField('电费CNY/H', validators=[DataRequired()])
    labor_cost = FloatField('人工费用CNY/H', validators=[DataRequired()])
    submit = SubmitField('提交')

class ProductLaborForm(FlaskForm):
    labor_choices = SelectField('选择工序', coerce=int, validators=[DataRequired()])
    labor_name = StringField('工序名称', render_kw={'readonly': True})

    laborID = IntegerField('工序id', render_kw={'readonly': True}) #用来传递给edit_product.html

    process_time = FloatField('工序工时/秒', default = 0.0)
    capacity = FloatField('产能/次', default = 0.0)
    qualification_rate = FloatField('合格率', default = 1.0)

    def __init__(self, *args, **kwargs):
        super(ProductLaborForm, self).__init__(*args, **kwargs)
        self.labor_choices.choices = [(l.id, l.name) for l in Labor.query.all()]


class ProductForm(FlaskForm):
    name = StringField('产品名称', validators=[DataRequired(), Length(1, 20)])

    trans_method = StringField('运输方式', validators=[Optional(), Length(1, 20)])
    trans_dest = StringField('运输目的地', validators=[Optional(), Length(1, 20)])
    trans_cost_kg = FloatField('运输成本/kg', validators=[Optional()], default=1)

    dev_coef = FloatField('开发系数', validators=[Optional()], default=0)
    fac_coef = FloatField('工厂系数', validators=[Optional()], default=5)
    admin_coef = FloatField('管理系数', validators=[Optional()], default=10)
    sale_coef = FloatField('销售系数', validators=[Optional()], default=3)
    finance_coef = FloatField('财务系数', validators=[Optional()], default=1.5)
    tax_coef = FloatField('税务系数', validators=[Optional()], default=0)
    profit_coef = FloatField('利润系数', validators=[Optional()], default=12)

    submit = SubmitField('提交')
