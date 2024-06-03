from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, ValidationError, HiddenField, \
    BooleanField, PasswordField, FloatField
from wtforms.validators import DataRequired, Length, Optional

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

class LaborForm(FlaskForm):
    name = StringField('工序', validators=[DataRequired(), Length(1, 20)])
    deprec_cost = FloatField('折旧费用', validators=[DataRequired()])
    elec_cost = FloatField('电费CNY/H', validators=[DataRequired()])
    labor_cost = FloatField('人工费用CNY/H', validators=[DataRequired()])
    submit = SubmitField('提交')

class ProductForm(FlaskForm):
    name = StringField('产品名称', validators=[DataRequired(), Length(1, 20)])
    trans_method = StringField('运输方式', validators=[Optional(), Length(1, 20)])
    trans_dest = StringField('运输目的地', validators=[Optional(), Length(1, 20)])
    trans_cost_kg = FloatField('运输成本/公斤', validators=[Optional()])
    dev_coef = FloatField('开发系数', validators=[Optional()], default=0.0)
    fac_coef = FloatField('工厂系数', validators=[Optional()], default=5.0)
    admin_coef = FloatField('管理系数', validators=[Optional()], default=10.0)
    sale_coef = FloatField('销售系数', validators=[Optional()], default=3.0)
    finance_coef = FloatField('财务系数', validators=[Optional()], default=1.5)
    tax_coef = FloatField('税务系数', validators=[Optional()], default=0.0)
    profit_coef = FloatField('利润系数', validators=[Optional()], default=12.0)
    submit = SubmitField('提交')