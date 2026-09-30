from flask import Blueprint

# Initialize the groceries Blueprint
groceries_bp = Blueprint('groceries', __name__)

# Import routes at the bottom to avoid circular dependencies
from app.groceries import routes