from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
import json

from api_client import fetch_current_schedule
from models import db, PriceSheet, Booking # Importing models

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bus_app.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Suppressing a warning
app.secret_key = os.getenv('FLASK_SECRET_KEY')
db.init_app(app) # Initialize the database with app

def manage_price_lists(new_price_list_data):
    """This function takes as input new price_sheet data, it then checks if price_sheet with same id is already in database.
    If not it adds current price_sheet to database"""
    with app.app_context():
        existing_price_sheet = db.session.get(PriceSheet, new_price_list_data['id'])
        if not existing_price_sheet:
            expires_date = new_price_list_data['expires'].get('date_obj')
            if not expires_date:
                print(f"Warning: Price list {new_price_list_data['id']} has no valid expiry date. Skipping save.")
                return False

            #  Creating new price_sheet 
            new_price_sheet = PriceSheet(
                id=new_price_list_data['id'],
                expires=expires_date,
                data=json.dumps(new_price_list_data['routes'])
            )

            #  Commiting new price_sheet to db
            db.session.add(new_price_sheet)
            db.session.commit()
            # ... (rest of manage_price_lists) ...

# Creating the actual database tables
with app.app_context():
    db.create_all() # This creates the tables if they don't exist


if __name__ == '__main__':
    with app.app_context():
        if not PriceSheet.query.first(): 
            print("Database empty. Attempting initial API fetch...")
            initial_data = fetch_current_schedule()
            if initial_data:
                # Naive datetime object
                expires_naive = initial_data['expires'].get('date_obj')

                if expires_naive:
                    # Making expires_naive timezone-aware by replacing tzinfo with timezone.utc
                    expires_aware = expires_naive.replace(tzinfo=timezone.utc)

                    # Now comparing timezone aware date time objects
                    if datetime.now(timezone.utc) < expires_aware:
                        manage_price_lists(initial_data)
                        print("Initial schedule fetched and saved.")
                    else:
                        print("Initial schedule fetched but it's already expired or invalid.")
                else:
                    print(f"Warning: Initial price list has no valid expiry date. Not saving.")
            else:
                print("Failed to fetch initial schedule from API.")
