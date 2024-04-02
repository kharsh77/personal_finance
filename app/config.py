class Configs(object):
    # SQLALCHEMY_DATABASE_URI = "postgresql://cool_user:1234@localhost:5432/cool_db"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@db:5432/postgres"
    # SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgrespw@localhost:55004"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET="SECRET"
