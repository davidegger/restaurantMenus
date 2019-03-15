from flask import Flask

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurants = session.query(Restaurant).filter_by(id = restaurant_id).one()
    output = ''
    items = session.query(MenuItem).filter_by(restaurant_id=restaurants.id)
    output += "<b>"
    output += restaurants.name
    output += '</b></br>'
    for i in items:
        output += i.name
        output += '</br>'
        output += i.price
        output += '</br>'
        output += i.description
        output += '</br>'
        output += '</br>'
    return output

@app.route('/')
def allMenus():
    restaurants = session.query(Restaurant).all()
    output = ''
    for r in restaurants:
        items = session.query(MenuItem).filter_by(restaurant_id=r.id)
        output += "<b>"
        output += r.name
        output += '</b></br>'
        for i in items:
            output += i.name
            output += '</br>'
            output += i.price
            output += '</br>'
            output += i.description
            output += '</br>'
            output += '</br>'
    return output

# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/newMenuItem')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/editMenuItem/<int:menu_id>/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/deleteMenuItem/<int:menu_id>/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
