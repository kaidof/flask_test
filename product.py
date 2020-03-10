from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = db.Column(db.String())
    price = db.Column(db.Numeric(8, 3))
    in_stock = db.Column(db.Integer())

    def __init__(self, name, price=0.0):
        self.name = name
        self.price = price
        self.in_stock = 0

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'in_stock': self.in_stock,
        }
