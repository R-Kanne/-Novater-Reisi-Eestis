from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy() # Initializing the SQLAlchemy extension

class PriceSheet(db.Model):
    __tablename__ = 'price_sheets' # Explicit table name
    id = db.Column(db.String, primary_key=True) # The ID from the API response
    expires = db.Column(db.DateTime, nullable=False)
    timestamp_fetched = db.Column(db.DateTime, default=datetime.now(timezone.utc)) # When data was fetched
    data = db.Column(db.Text, nullable=False) # Store the whole JSON 'routes' part as text

    # Relationship to Booking (one PriceSheet can have many Bookings)
    bookings = db.relationship('Booking', backref='price_list', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings' # Explicit table name
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    from_city = db.Column(db.String(100), nullable=False)
    to_city = db.Column(db.String(100), nullable=False)
    route_api_id = db.Column(db.String, nullable=False)
    schedule_api_id = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    booking_time = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    # Foreign key relationship to PriceSheet
    price_sheet_id = db.Column(db.String, db.ForeignKey('price_sheets.id'), nullable=False)