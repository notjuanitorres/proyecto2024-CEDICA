from src.core import database


def register_commands(app):
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset(app)
