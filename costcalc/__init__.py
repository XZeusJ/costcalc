import os

import sys
import os

# print("Python version:", sys.version)
# print("sys.path:", sys.path)
# print("FLASK_APP:", os.getenv('FLASK_APP'))
# print("FLASK_ENV:", os.getenv('FLASK_ENV'))

# 获取项目根目录
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 将项目根目录添加到sys.path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import click
from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from costcalc.blueprints.auth import auth_bp
from costcalc.blueprints.products import products_bp
from costcalc.blueprints.resources import resources_bp
from costcalc.extensions import db, login_manager, csrf, bootstrap
from costcalc.models import User, Product, Material, Labor, ProductMaterial, ProductLabor
from costcalc.settings import config



def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('costcalc')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    register_commands(app)
    return app

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    bootstrap.init_app(app)

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(resources_bp)

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error.html', description=e.description, code=e.code), 400
    
    @app.errorhandler(404)
    def page_not_found(e):
        app.logger.debug(f"404 error occurred: {e}")
        return render_template('error.html', description=e.description, code=e.code), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', description='Internal Server Error', code='500'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('error.html', description=e.description, code=e.code), 400

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')

    @app.cli.command()
    def forge():
        user = User(username='testuser', password_hash='hashedpassword')
        db.session.add(user)
        db.session.commit()

        material_dqj = Material(name='丁晴胶', unit_price=0.022)
        material_bmc = Material(name='BMC', unit_price=0.025)
        labor_my = Labor(name='模压', deprec_cost = 7, elec_cost=21, labor_cost=30)
        labor_bz = Labor(name='包装', deprec_cost = 1, elec_cost=1, labor_cost=25)

        db.session.add_all([material_dqj, material_bmc, labor_my, labor_bz])
        db.session.commit()

        product_a = Product(name='新产品', user_id=user.id, trans_cost_kg=1)
        db.session.add(product_a)
        db.session.commit()

        product_material_dqj = ProductMaterial(product_id=product_a.id, material_id=material_dqj.id, net_weight=23, gross_weight=8,qualification_rate=0.95)
        product_material_bmc = ProductMaterial(product_id=product_a.id, material_id=material_bmc.id, net_weight=3, gross_weight=1,qualification_rate=0.98)
        product_labor_my = ProductLabor(product_id=product_a.id, labor_id=labor_my.id, process_time=120,capacity=4,qualification_rate=0.95)
        product_labor_bz = ProductLabor(product_id=product_a.id, labor_id=labor_bz.id, process_time=5,capacity=1,qualification_rate=1)

        db.session.add_all([product_material_dqj, product_material_bmc, product_labor_my, product_labor_bz])
        db.session.commit()

        product_b = Product(name='二十柱', user_id=user.id, trans_cost_kg=1)
        db.session.add(product_b)
        db.session.commit()

        product_material_bmc_b = ProductMaterial(product_id=product_b.id, material_id=material_bmc.id, net_weight=4, gross_weight=3,qualification_rate=0.98)
        product_labor_my_b = ProductLabor(product_id=product_b.id, labor_id=labor_my.id, process_time=360,capacity=4,qualification_rate=0.98)

        db.session.add_all([product_material_bmc_b, product_labor_my_b])
        db.session.commit()


    # @app.cli.command()
    # @click.option('--message', default=300, help='Quantity of messages, default is 300.')
    # def forge(message):
    #     """Generate fake data."""
    #     import random
    #     from sqlalchemy.exc import IntegrityError

    #     from faker import Faker

    #     fake = Faker()

    #     click.echo('Initializing the database...')
    #     db.drop_all()
    #     db.create_all()

    #     click.echo('Forging the data...')
    #     admin = User(nickname='Grey Li', email='admin@helloflask.com')
    #     admin.set_password('helloflask')
    #     db.session.add(admin)
    #     db.session.commit()

    #     click.echo('Generating users...')
    #     for i in range(50):
    #         user = User(nickname=fake.name(),
    #                     bio=fake.sentence(),
    #                     github=fake.url(),
    #                     website=fake.url(),
    #                     email=fake.email()
    #                     )
    #         db.session.add(user)
    #         try:
    #             db.session.commit()
    #         except IntegrityError:
    #             db.session.rollback()

    #     click.echo('Generating messages...')
    #     for i in range(message):
    #         message = Message(
    #             author=User.query.get(random.randint(1, User.query.count())),
    #             body=fake.sentence(),
    #             timestamp=fake.date_time_between('-30d', '-2d'),
    #         )
    #         db.session.add(message)

    #     db.session.commit()
    #     click.echo('Done.')

if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)