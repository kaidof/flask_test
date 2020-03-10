from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class OrderItem(db.Model):
    __tablename__ = 'order_item'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(UUID(as_uuid=True), default=uuid4, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer())
    price = db.Column(db.Numeric(8, 3))
    amount = db.Column(db.Numeric(8, 3), default=0.0)

    def __repr__(self):
        return '<ORDER_ITEM id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'amount': self.amount,
        }
