from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# The connection string: postgresql://username:password@host:port/database_name
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:Magic-Christian-Ecumen89@127.0.0.1:5432/gcp_practice'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database connection
db = SQLAlchemy(app)

# --- DATABASE MODELS ---
class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    store_name = db.Column(db.String(255), nullable=False)
    trip_date = db.Column(db.Date, default=datetime.utcnow)
    
    # This creates a virtual relationship to the items
    items = db.relationship('TripItem', backref='trip', lazy=True, cascade="all, delete-orphan")
    
    # Calculates the total cost of all items in this trip dynamically
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

# --- ROUTES ---
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        store = request.form['store_name']
        date_str = request.form['trip_date']
        trip_date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        new_trip = Trip(store_name=store, trip_date=trip_date_obj)
        db.session.add(new_trip)
        db.session.commit()
        return redirect('/')
        
    # Check the URL for '?sort=asc' or '?sort=desc'
    sort_order = request.args.get('sort', 'desc')
    if sort_order == 'asc':
        all_trips = Trip.query.order_by(Trip.trip_date.asc()).all()
    else:
        all_trips = Trip.query.order_by(Trip.trip_date.desc()).all()
        
    return render_template('index.html', trips=all_trips, current_sort=sort_order)

@app.route('/trip/<int:trip_id>', methods=['GET', 'POST'])
def trip_detail(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    
    if request.method == 'POST':
        item_name = request.form['item_name']
        price = request.form['price']
        category = request.form.get('category', '').strip() # Capture the custom tag
        
        new_item = TripItem(trip_id=trip.id, item_name=item_name, price=price, category=category)
        db.session.add(new_item)
        db.session.commit()
        
        return redirect(f'/trip/{trip.id}')
        
    receipt_total = sum(item.price for item in trip.items)
    #Boo Baa
    # NEW: Create a list of unique tags used in this trip (ignoring blanks)
    unique_tags = sorted(list(set(item.category for item in trip.items if item.category)))

    return render_template('trip.html', trip=trip, total=receipt_total, unique_tags=unique_tags)

@app.route('/delete-item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    # 1. Find the item in the database
    item_to_delete = TripItem.query.get_or_404(item_id)
    
    # 2. Remember which trip it belongs to so we can redirect back there
    trip_id = item_to_delete.trip_id
    
    # 3. Delete it and commit to the database
    db.session.delete(item_to_delete)
    db.session.commit()
    
    # 4. Send the user right back to the receipt page
    return redirect(f'/trip/{trip_id}')

@app.route('/edit-item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    # Find the item we want to edit
    item = TripItem.query.get_or_404(item_id)
    
    if request.method == 'POST':
        # Update the database record with the new typed values
        item.item_name = request.form['item_name']
        item.price = request.form['price']
        db.session.commit()
        
        # Send them back to the receipt page
        return redirect(f'/trip/{item.trip_id}')
        
    # If it's a GET request, show them the edit form with the current data
    return render_template('edit-item.html', item=item)

@app.route('/edit-trip/<int:trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if request.method == 'POST':
        trip.store_name = request.form['store_name']
        date_str = request.form['trip_date']
        trip.trip_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        db.session.commit()
        return redirect('/')
    return render_template('edit-trip.html', trip=trip)

@app.route('/delete-trip/<int:trip_id>', methods=['POST'])
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    db.session.delete(trip)
    db.session.commit()
    return redirect('/')

# The server "on switch" belongs at the very bottom
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
