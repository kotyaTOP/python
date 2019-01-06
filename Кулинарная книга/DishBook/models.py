from app_config import mydb
from sqlalchemy.dialects.mysql import TIME

class Dish(mydb.Model):
    __tablename__ = 'Dish'

    id_dish = mydb.Column('idDish', mydb.INTEGER, primary_key=True, autoincrement=True)
    dish_name = mydb.Column('DishName', mydb.String(45), nullable=False)
    recipe = mydb.Column('Recipe', mydb.String(400), nullable=False)
    time = mydb.Column('Time', TIME, nullable=False)

class Ingredient(mydb.Model):
    __tablename__ = 'Ingredient'

    id_ingred = mydb.Column('idIngred', mydb.INTEGER, primary_key=True, autoincrement=True)
    ingred_name = mydb.Column('IngredName', mydb.String(45), nullable=False)

class Unit(mydb.Model):
    __tablename__ = 'Unit'

    id_unit = mydb.Column('idUnit', mydb.INTEGER, primary_key=True, autoincrement=True)
    unit_name = mydb.Column('UnitName', mydb.String(45), nullable=False)

class Dish_Ingredient(mydb.Model):
    __tablename__ = 'DishIngred'

    id_dish_ingred = mydb.Column("idDishIngred", mydb.INTEGER, primary_key=True, autoincrement=True)
    id_dish = mydb.Column("idDish", mydb.ForeignKey('Dish.idDish'), nullable=False, index=True)
    id_ingred = mydb.Column("idIngred",mydb.ForeignKey('Ingredient.idIngred'), nullable=False, index=True)
    id_unit = mydb.Column("idUnit", mydb.ForeignKey('Unit.idUnit'), nullable=False, index=True)
    sum = mydb.Column('Sum', mydb.INTEGER, nullable=False)

    dish = mydb.relationship('Dish')
    ingred = mydb.relationship('Ingredient')
    unit = mydb.relationship('Unit')
