class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hr.db'  # SQLite for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False