import os
import sqlite3
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'travel.db'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Import and register blueprints
    from app.routes.main import main_bp
    from app.routes.planner import planner_bp, api_bp
    from app.routes.budget import budget_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(budget_bp)

    return app

def init_db():
    app = create_app()
    db_path = app.config['DATABASE']
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'schema.sql')
    
    conn = sqlite3.connect(db_path)
    with open(schema_path, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized successfully at", db_path)
