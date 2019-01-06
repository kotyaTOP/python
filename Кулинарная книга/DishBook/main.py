from flask import render_template, request, redirect, url_for
from models import Dish, Ingredient, Unit, Dish_Ingredient
from app_config import app, mydb
from forms import DishForm, IngredForm, UnitForm, DishIngredForm

@app.route('/')
def menu():
    return render_template('./menu.html')

@app.route('/dish')
def dish():
    dishes = mydb.session.query(Dish).all()
    return render_template('dish.html', dishes=dishes)

@app.route('/ingredient')
def ingredient():
    ingreds = mydb.session.query(Ingredient).all()
    return render_template('ingredient.html', ingred=ingreds)

@app.route('/dish_ingred')
def dish_ingred():
    dish_ingred = mydb.session.query(Dish_Ingredient).all()
    return render_template('dish_ingred.html', dish_ingred=dish_ingred)

@app.route('/unit')
def unit():
    units = mydb.session.query(Unit).all()
    return render_template('unit.html', units=units)

@app.route('/change_dish/<id>/<do>', methods=['GET', 'POST'])
def change_dish(id, do):
    id = int(id)

    if do == "add":
        s = Dish()
    else:
        s = mydb.session.query(Dish).filter(Dish.id_dish == id).one_or_none()

    form = DishForm(request.form, obj=s)

    if do == "delete":
        mydb.session.delete(s)
        mydb.session.flush()
        return redirect(url_for('dish'))

    if form.button_save.data:
        form.populate_obj(s)
        mydb.session.add(s)
        if s.id_dish != id:
            return redirect(url_for('dish', id=s.id_dish))


    return render_template('change_dish.html', form=form)

@app.route('/change_ingred/<id>/<do>', methods=['GET', 'POST'])
def change_ingred(id, do):
    id = int(id)

    if do == "add":
        s = Ingredient()
    else:
        s = mydb.session.query(Ingredient).filter(Ingredient.id_ingred == id).one_or_none()

    form = IngredForm(request.form, obj=s)

    if do == "delete":
        mydb.session.delete(s)
        mydb.session.flush()
        return redirect(url_for('ingredient'))

    if form.button_save.data:
        form.populate_obj(s)
        mydb.session.add(s)
        if s.id_ingred != id:
            return redirect(url_for('ingredient', id=s.id_ingred))


    return render_template('change_ingred.html', form=form)

@app.route('/change_unit/<id>/<do>', methods=['GET', 'POST'])
def change_unit(id, do):
    id = int(id)

    if do == "add":
        s = Unit()
    else:
        s = mydb.session.query(Unit).filter(Unit.id_unit == id).one_or_none()

    form = UnitForm(request.form, obj=s)

    if do == "delete":
        mydb.session.delete(s)
        mydb.session.flush()
        return redirect(url_for('unit'))

    if form.button_save.data:
        form.populate_obj(s)
        mydb.session.add(s)
        if s.id_unit != id:
            return redirect(url_for('unit', id=s.id_unit))


    return render_template('change_unit.html', form=form)

@app.route('/change_dish_ingred/<id>/<do>', methods=['GET', 'POST'])
def change_dish_ingred(id, do):
    id = int(id)

    if do == "add":
        s = Dish_Ingredient()
    else:
        s = mydb.session.query(Dish_Ingredient).filter(Dish_Ingredient.id_dish_ingred == id).one_or_none()

    form = DishIngredForm(request.form, obj=s)

    if do == "delete":
        mydb.session.delete(s)
        mydb.session.flush()
        return redirect(url_for('dish_ingred'))

    if form.button_save.data:
        form.populate_obj(s)
        mydb.session.add(s)
        if s.id_dish_ingred != id:
            return redirect(url_for('dish_ingred', id=s.id_dish_ingred))


    return render_template('change_dish_ingred.html', form=form)


if __name__ == '__main__':
    app.run()

