from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from flask_sqlalchemy import SQLAlchemy
from order_item import OrderItem
from sqlalchemy.orm import relationship

db = SQLAlchemy()


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    time = db.Column(db.DateTime(timezone=True))
    # FIXME: Should use relationship ?!
    items = None  # list

    def load_items(self):
        self.items = db.session.query(OrderItem).filter(OrderItem.order_id == self.id).all()
        return self

    def __repr__(self):
        return '<ORDER id {}>'.format(self.id)

    def serialize(self):
        if self.items:
            return {
                'id': str(self.id),
                'time': self.time.replace(microsecond=0).isoformat(),
                'items': [x.serialize() for x in self.items],
                'total_amount': sum(c.amount for c in self.items),
            }
        else:
            return {
                'id': str(self.id),
                'time': self.time.replace(microsecond=0).isoformat(),
                'items': None,
                'total_amount': 0.0,
            }
