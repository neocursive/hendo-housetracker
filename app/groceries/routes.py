from flask import render_template, request, redirect
from datetime import datetime
from app import db
from app.models import Trip, TripItem
from app.groceries import groceries_bp

@groceries_bp.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        store = request.form['store_name']
        date_str = request.form['trip_date']
        trip_date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()

        new_trip = Trip(store_name=store, trip_date=trip_date_obj)
        db.session.add(new_trip)
        db.session.commit()
        return redirect('/groceries/')

    sort_order = request.args.get('sort', 'desc')
    if sort_order == 'asc':
        all_trips = Trip.query.order_by(Trip.trip_date.asc()).all()
    else:
        all_trips = Trip.query.order_by(Trip.trip_date.desc()).all()

    return render_template('index.html', trips=all_trips, current_sort=sort_order)

@groceries_bp.route('/trip/<int:trip_id>', methods=['GET', 'POST'])
def trip_detail(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    if request.method == 'POST':
        item_name = request.form['item_name']
        price = request.form['price']
        category = request.form.get('category', '').strip()

        new_item = TripItem(trip_id=trip.id, item_name=item_name, price=price, category=category)
        db.session.add(new_item)
        db.session.commit()

        return redirect(f'/groceries/trip/{trip.id}')

    receipt_total = sum(item.price for item in trip.items)
    unique_tags = sorted(list(set(item.category for item in trip.items if item.category)))

    return render_template('trip.html', trip=trip, total=receipt_total, unique_tags=unique_tags)

@groceries_bp.route('/delete-item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    item_to_delete = TripItem.query.get_or_404(item_id)
    trip_id = item_to_delete.trip_id
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(f'/groceries/trip/{trip_id}')

@groceries_bp.route('/edit-item/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    item = TripItem.query.get_or_404(item_id)
    if request.method == 'POST':
        item.item_name = request.form['item_name']
        item.price = request.form['price']
        item.category = request.form.get('category', '').strip()
        db.session.commit()
        return redirect(f'/groceries/trip/{item.trip_id}')

    return render_template('edit-item.html', item=item)

@groceries_bp.route('/edit-trip/<int:trip_id>', methods=['GET', 'POST'])
def edit_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if request.method == 'POST':
        trip.store_name = request.form['store_name']
        date_str = request.form['trip_date']
        trip.trip_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        db.session.commit()
        return redirect('/groceries/')
    return render_template('edit-trip.html', trip=trip)

@groceries_bp.route('/delete-trip/<int:trip_id>', methods=['POST'])
def delete_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    db.session.delete(trip)
    db.session.commit()
    return redirect('/groceries/')
