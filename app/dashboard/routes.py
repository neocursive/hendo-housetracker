from flask import render_template, request, redirect, url_for
from app import db
from app.models import Income, Bucket
from app.dashboard import dashboard_bp

@dashboard_bp.route('/')
def index():
    # 1. Fetch or Create Default Income
    income = Income.query.first()
    if not income:
        income = Income(source="Main Paycheck", amount=0.00)
        db.session.add(income)
        db.session.commit()

    # 2. Fetch or Create Default Buckets
    buckets = Bucket.query.order_by(Bucket.order).all()
    if not buckets:
        default_buckets = [
            Bucket(name="Bill Pay", allocated_amount=0, order=1, is_system=True),
            Bucket(name="Groceries", allocated_amount=0, order=2, is_system=True),
            Bucket(name="Debt Repayment", allocated_amount=0, order=3, is_system=True)
        ]
        db.session.add_all(default_buckets)
        db.session.commit()
        buckets = Bucket.query.order_by(Bucket.order).all()

    # 3. Calculate the Discretionary Leftover
    total_allocated = sum(b.allocated_amount for b in buckets)
    discretionary = income.amount - total_allocated

    return render_template('dashboard.html',
                           income=income,
                           buckets=buckets,
                           discretionary=discretionary)

@dashboard_bp.route('/update-income', methods=['POST'])
def update_income():
    income = Income.query.first()
    income.amount = float(request.form['amount'])
    db.session.commit()
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/update-bucket/<int:id>', methods=['POST'])
def update_bucket(id):
    bucket = Bucket.query.get_or_404(id)
    bucket.allocated_amount = float(request.form['allocated_amount'])
    db.session.commit()
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/add-bucket', methods=['POST'])
def add_bucket():
    name = request.form['name']
    amount = float(request.form['allocated_amount'])
    # Place new buckets at the end of the waterfall
    new_order = Bucket.query.count() + 1
    new_bucket = Bucket(name=name, allocated_amount=amount, order=new_order, is_system=False)
    db.session.add(new_bucket)
    db.session.commit()
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/delete-bucket/<int:id>', methods=['POST'])
def delete_bucket(id):
    bucket = Bucket.query.get_or_404(id)
    if not bucket.is_system: # Protect system buckets from deletion
        db.session.delete(bucket)
        db.session.commit()
    return redirect(url_for('dashboard.index'))
