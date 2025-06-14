from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
from datetime import datetime, timezone
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
            
            # Querying all price sheets, ordered by their fetch timestamp (oldest first)
            all_price_sheets = PriceSheet.query.order_by(PriceSheet.timestamp_fetched.asc()).all()

            if len(all_price_sheets) > 15:
                sheets_to_delete = all_price_sheets[:-15] # This slices the list to get everything but the last 15 price_sheets

                # 4. Delete the identified old price_sheets
                for sheet in sheets_to_delete:
                    db.session.delete(sheet)
                
                # 5. Commiting to database
                db.session.commit()
                print(f"Deleted {len(sheets_to_delete)} old price sheets to maintain limit of 15.")

            print(f"Price list {new_price_list_data['id']} saved successfully.")
            return True # Indicate that a new price sheet was added

        print(f"Price list {new_price_list_data['id']} already exists. Skipping save.")
        return False # Indicate that no new price sheet was added

def get_unique_departure_and_arrival_cities(routes_data):
    """Takes as input a price_sheet and returns two lists of unique valid arrival and departure cities as per api"""
    departure_cities = set()
    arrival_cities = set()

    for route in routes_data:
        departure_cities.add(route['from']['name'])
        arrival_cities.add(route['to']['name'])
    
    # Convert sets to sorted lists
    sorted_departure_cities = sorted(list(departure_cities))
    sorted_arrival_cities = sorted(list(arrival_cities))
    
    return sorted_departure_cities, sorted_arrival_cities # Return as a tuple

def get_current_routes_data():
    """
    Fetches the latest valid price sheet routes data.
    Prioritizes fetching from the database cache if a non-expired sheet exists,
    otherwise fetches from the external API and saves it to the database.

    Returns:
        list: A list of route dictionaries, or an empty list if data cannot be fetched.
    """
    with app.app_context(): 

        valid_price_sheet_db = PriceSheet.query.filter(
            PriceSheet.expires > datetime.now(timezone.utc)
        ).order_by(PriceSheet.timestamp_fetched.desc()).first()

        if valid_price_sheet_db:
            print(f"Using cached price list: {valid_price_sheet_db.id} (expires: {valid_price_sheet_db.expires.isoformat()})")
            return json.loads(valid_price_sheet_db.data)
        else:
            print("No valid price list in DB or all expired. Fetching from API...")
            api_data = fetch_current_schedule() # Calling api_client function

            if api_data:
                # Ensuring api_data has the 'date_obj' key for the actual datetime object
                expires_naive = api_data['expires'].get('date_obj')

                if expires_naive:
                    # Making the expiry datetime timezone-aware
                    expires_aware = expires_naive.replace(tzinfo=timezone.utc)

                    # Checking if the newly fetched data is already expired
                    if datetime.now(timezone.utc) < expires_aware:
                        # Saving the new data to the database
                        manage_price_lists(api_data)
                        # Return just the 'routes' part of the API response
                        return api_data.get('routes', [])
                    else:
                        flash("Fetched price list is already expired. Cannot display current data.", "warning")
                        print("API fetch: Fetched price list is already expired. Not saving.")
                        return [] # Returning empty if new data is already expired
                else:
                    flash("API response missing expiry date for new data.", "error")
                    print("API fetch: Response missing expiry date for new data.")
                    return []
            else:
                flash("Failed to fetch current schedule from API.", "error")
                print("API fetch: Failed to fetch current schedule.")
                return [] # Returning empty if API fetch failed

# Creating the actual database tables
with app.app_context():
    db.create_all() # This creates the tables if they don't exist

@app.route('/', methods=['GET','POST'])
def index():
    """Main page"""
    all_routes = get_current_routes_data() # Getting current routes data

    departure_cities, arrival_cities = get_unique_departure_and_arrival_cities(all_routes) # getting valid cities

    return render_template( 
        'index.html',
        routes=all_routes, # Pass all routes to display
        request=request, # Keep for future form handling
        departure_cities=departure_cities,
        arrival_cities=arrival_cities
    )

@app.route('/bookings', methods=['GET','POST'])
def book_route():
    """Route that displays booking information"""
    return render_template('bookings.html')
    


if __name__ == '__main__':
    app.run(debug=True)
