import os
import click
import logging

from flask import Flask, render_template
from flask_wtf.csrf import CSRFError

from costcalc.blueprints.auth import auth_bp
from costcalc.blueprints.products import products_bp
from costcalc.blueprints.resources import resources_bp
from costcalc.extensions import db, login_manager, csrf, bootstrap
from costcalc.settings import config



def create_app(config_name = None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('costcalc')
    app.config.from_object(config[config_name])

    logging.basicConfig(level=logging.INFO)
    app.logger.info(f"Running in {config_name} mode")

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
    @click.argument('counts', nargs=3, type=int, required=False)
    def forge(counts=None):
        if counts is None:
            counts = [5, 5, 10]  # 默认值
        material, labor, product = counts
        
        from costcalc.fakes import fake_users, fake_materials, fake_labors, fake_products
        db.drop_all()
        click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
        
        click.echo(f'Generating users...')
        fake_users()
        click.echo(f'Generating {material * 2} materials...')
        fake_materials(material * 2)
        click.echo(f'Generating {labor} labors...')
        fake_labors(labor)
        click.echo(f'Generating {product} products...')
        fake_products(product)
        click.echo('Done.')


if __name__ == '__main__':
    app = create_app()
    app.run(port=8000)