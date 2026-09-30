from datetime import datetime
from app import db

class Income(db.Model):
    __tablename__ = 'incomes'
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String(255), nullable=False, default="Main Paycheck")
    amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)

class Bucket(db.Model):
    __tablename__ = 'buckets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    allocated_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    order = db.Column(db.Integer, default=10) # Used to sort the waterfall
    is_system = db.Column(db.Boolean, default=False) # True for core defaults like 'Groceries'

# --- Existing Grocery Models Below ---
class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(255), nullable=False)
    trip_date = db.Column(db.Date, default=datetime.utcnow)
    items = db.relationship('TripItem', backref='trip', lazy=True, cascade="all, delete-orphan")

    @property
    def total_cost(self):
        return sum(item.price for item in self.items)

class TripItem(db.Model):
    __tablename__ = 'trip_items'
    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    item_name = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2), nullable=False)