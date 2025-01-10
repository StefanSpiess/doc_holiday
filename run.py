from app import create_app, db
from app.models import Address, SalaryHistory

app = create_app()

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("Initialized the database!")