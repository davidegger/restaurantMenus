from flask import Flask, render_template, request, redirect,url_for, flash, jsonify

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db', check_same_thread=False)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def itemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(MenuItems = [item.serialize])


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html', restaurant = restaurant, items = items)


# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/newMenuItem', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        courseText = request.form['course']
        newItem = MenuItem(name = request.form['name'],
                        restaurant_id = restaurant_id,
                        price = request.form['price'],
                        description = request.form['description'],
                        course = request.form['course'])
        session.add(newItem)
        session.commit()
        flash("Menu Item Added")
        flash(courseText)
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/editMenuItem/<int:menu_id>/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        item = session.query(MenuItem).filter_by(id = menu_id).one()
        item.name = request.form['name']
        item.price = request.form['price']
        item.description = request.form['description']
        item.restaurant_id = restaurant_id
        item.course = request.form['course']
        session.commit()
        flash("Menu Item Edited")
        flash(request.form['course'])
        return redirect(url_for('restaurantMenu', restaurant_id = item.restaurant_id))
    else:
        menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
        return render_template('editMenuItem.html', restaurant_id = restaurant_id,
        menu_id = menu_id, menuItemName = menuItem.name, menuItemPrice = menuItem.price,
        menuItemDescription = menuItem.description, menuItemCourse = menuItem.course)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/deleteMenuItem/<int:menu_id>/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':
        item = session.query(MenuItem).filter_by(id = menu_id).one()
        session.delete(item)
        session.commit()
        flash("Menu Item Deleted")
        return redirect(url_for('menu.html', restaurant_id = restaurant_id))
    else:
        menuItemName = session.query(MenuItem).filter_by(id = menu_id).one()
        return render_template('restaurantMenu.html', restaurant_id = restaurant_id,
        menu_id = menu_id, menuItemName = menuItemName.name)



if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
