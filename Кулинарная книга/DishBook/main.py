from flask import render_template, request, redirect, url_for
from models import Dish, Ingredient, Unit, Dish_Ingredient
from app_config import app, mydb
from forms import DishForm, IngredForm, UnitForm, DishIngredForm, FormSearch


@app.route('/')
def menu():
    return render_template('./menu.html')


@app.route('/dish')
def dish():
    dishes = mydb.session.query(Dish).all()
    form = FormSearch(request.args)
    if form.button_search1.data:
        q = mydb.session.query(Dish)
        if form.dish_name.data != '':
            q = q.filter(Dish.dish_name == form.dish_name.data)
        dishes = q.all()

    return render_template('dish.html', dishes=dishes, form=form)


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

# @app.route('/search_dish')
# def search_dish():
#     form = SearchDishForm(request.args)
#     dishes = mydb.session.query(Dish_Ingredient).all()
#     if form.button_search1.data:
#         print(form.ingred.data)
#             # q = mydb.session.query(Dish_Ingredient)
#             # if form.ingred.data != '':
#             #     ingreds_id = [int(elem) for elem in form.ingred_names.data.split(sep=',')]
#             #
#             #     print(ingreds_id)
#             #
#             #     q = get_min_dishes(ingreds_id)
#             # dish = q
#             # dish_id = [elem.id_dish for elem in dish]
#             # dishes = get_dish_ingred(dish_id)
#         dishes_id = []
#         new_dishes = []
#         ingreds = {}
#         for dish in dishes:
#             if not dishes_id.__contains__(dish.id_dish):
#                 new_dishes.append(dish)
#                 dishes_id.append(dish.id_dish)
#             if not ingreds.keys().__contains__(dish.id_dish):
#                 ingreds[dish.id_dish] = []
#             ingreds[dish.id_dish].append(
#                 str(dish.ingred.ingred_name) + ' - ' + str(dish.sum) + str(dish.unit.unit_name))
#
#         return render_template('beauty_dish.html', dish=new_dishes, ingreds=ingreds, form=form)


@app.route('/beauty_dish')
def beauty_dish():
    form = FormSearch(request.args)
    dishes = mydb.session.query(Dish_Ingredient).all()

    if form.button_search1.data:
        q = mydb.session.query(Dish)
        if form.dish_name.data != '':
            q = q.filter(Dish.dish_name == form.dish_name.data)
        dish = q.all()
        dish_id = [elem.id_dish for elem in dish]
        dishes = get_dish_ingred(dish_id)

    if form.button_search2.data:
        if form.sum.data is not None:
            s = form.sum.data
            # sum = [i for i in range(s)]
            form.set_ingred(int(s))
            print(form.ingred)
            return render_template('beauty_dish.html', form=form)

    if form.button_search3.data:
        print(form.ingred.data)
        # q = mydb.session.query(Dish_Ingredient)
        # if form.ingred_names.data != '':
        #     ingreds_id = [int(elem) for elem in form.ingred_names.data.split(sep=',')]
        #
        #     print(ingreds_id)
        #
        #     q = get_min_dishes(ingreds_id)
        # dish = q
        # dish_id = [elem.id_dish for elem in dish]
        # dishes = get_dish_ingred(dish_id)
    dishes_id = []
    new_dishes = []
    ingreds = {}
    for dish in dishes:
        if not dishes_id.__contains__(dish.id_dish):
            new_dishes.append(dish)
            dishes_id.append(dish.id_dish)
        if not ingreds.keys().__contains__(dish.id_dish):
            ingreds[dish.id_dish] = []
        ingreds[dish.id_dish].append(str(dish.ingred.ingred_name) + ' - ' + str(dish.sum) + str(dish.unit.unit_name))

    return render_template('beauty_dish.html', dish=new_dishes, ingreds=ingreds, form=form)

def get_min_dishes(max_ingreds_id : list):
    all_dishes = mydb.session.query(Dish_Ingredient)
    dishes = mydb.session.query(Dish)
    ingreds_dict = {}
    for dish in dishes:
        if not ingreds_dict.keys().__contains__(dish.id_dish):
            ingreds_dict[dish.id_dish] = []
    print(all_dishes)
    for dish in all_dishes:
        ingreds_dict[dish.id_dish].append(dish.id_ingred)
    min_dishes = []
    for dish_id in ingreds_dict.keys():
        if contains(ingreds_dict[dish_id], max_ingreds_id):
            min_dishes.append(dish_id)
    print(min_dishes)
    return get_dish_ingred(min_dishes)

def get_dish_ingred(dishes_id: list):
    new_dish_ingreds = []
    dish_ingreds = mydb.session.query(Dish_Ingredient).all()
    for elem in dish_ingreds:
        if dishes_id.__contains__(elem.id_dish):
            new_dish_ingreds.append(elem)
    return new_dish_ingreds

def contains(minlist: list, list: list):
    for elem in minlist:
        if not elem in list:
            return False
    return True

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

@app.route('/search_dish')
def search_dish():
    form = FormSearch(request.form)
    if form.button_search3.data:
        return beauty_dish()
    return redirect(url_for('search_dish', form=form))


if __name__ == '__main__':
    metadata = mydb.metadata
    metadata.create_all(mydb.engine)
    app.run()
