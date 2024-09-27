from src.core import database


def register_commands(app):
    @app.cli.command(name="reset-db")
    def reset_db():
        database.reset(app)

    @app.cli.command(name="seed-db")
    def seed_db():
        from src.core.seeds import seed_accounts
        seed_accounts()
