
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

noodlehouse = session.query(Restaurant).first()

brat = MenuItem(
            name = "Beef Noodle Soup",
            description = "Taiwanese Beef Noodle Soup with Bok Choy, Cilantro",
            course = "Entree",
            price = "$6.99",
            restaurant = noodlehouse)
session.add(brat)
session.commit()
