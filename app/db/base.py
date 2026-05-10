from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase): # Все классы, которые наследуются от Base, SQLAlchemy будет воспринимать как ORM-модели.
    pass