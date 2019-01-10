from flask import render_template, request, redirect, url_for
from models import Dish, Ingredient, Unit, Dish_Ingredient
from app_config import app, mydb
from forms import DishForm, IngredForm, UnitForm, DishIngredForm, FormSearch
import json


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
    form = FormSearch(request.args)
    if form.button_search1.data:
        q = mydb.session.query(Ingredient)
        if form.ingred_name.data != '':
            q = q.filter(Ingredient.ingred_name == form.ingred_name.data)
        ingreds = q.all()
    return render_template('ingredient.html', ingred=ingreds, form=form)


@app.route('/dish_ingred')
def dish_ingred():
    dish_ingred = mydb.session.query(Dish_Ingredient).all()
    form = FormSearch(request.args)
    if form.button_search1.data:
        # q = mydb.session.query(Dish_Ingredient)
        dish_name = form.dish_name.data
        ingred_name = form.ingred_name.data
        print(dish_name)
        print(ingred_name)
        if len(dish_name)>0 and len(ingred_name) > 0:
            # q = q.filter(Dish_Ingredient.ingred.ingred_name == ingred_name and Dish_Ingredient.dish.dish_name == dish_name)
            dish = mydb.session.query(Dish).filter(Dish.dish_name == dish_name).all()[0]
            print(dish)
            ingred = mydb.session.query(Ingredient).filter(Ingredient.ingred_name == ingred_name).all()[0]
            dish_ingred = find_dish_ingred(dish=dish, ingred=ingred)
        else:
            if len(dish_name)>0 :
                dish = mydb.session.query(Dish).filter(Dish.dish_name == dish_name).all()[0]
                dish_ingred = find_dish_ingred(dish=dish)
            if len(ingred_name) :
                ingred = mydb.session.query(Ingredient).filter(Ingredient.ingred_name == ingred_name).all()[0]
                dish_ingred = find_dish_ingred(ingred=ingred)
    return render_template('dish_ingred.html', dish_ingred=dish_ingred, form=form)

def find_dish_ingred(dish=None, ingred=None):
    q = mydb.session.query(Dish_Ingredient).all()
    answer = []
    for elem in q:
        if dish is not None and ingred is not None:
            if elem.id_dish == dish.id_dish and elem.id_ingred == ingred.id_ingred:
                answer.append(elem)
        else:
            if dish is not None and elem.id_dish == dish.id_dish:
                answer.append(elem)
            if ingred is not None and elem.id_ingred == ingred.id_ingred:
                answer.append(elem)
    return answer

@app.route('/stat')
def stat():
    form=FormSearch(request.args)
    if form.button_search4.data:
        dish_ingred = mydb.session.query(Dish_Ingredient).all()
        dish = mydb.session.query(Dish).all()
        ingred_dict = get_ingreds_for_dishes(dish, dish_ingred)

        stat_list=set_stat_data(ingred_dict)
        # stat_list = json.dumps(set_stat_data(ingred_dict))

        return render_template('stat.html', form=form, dish=dish, stat_list=stat_list)

    return render_template('stat.html', form=form)

def set_stat_data(ingred_dict : dict):
    stat_dict = {}
    sorted_val = get_sorted(ingred_dict)
    max = len(sorted_val[len(sorted_val) - 1])
    min = len(sorted_val[0])
    print(sorted_val)
    max_list = get_keys_from_value(ingred_dict, max)
    min_list = get_keys_from_value(ingred_dict, min)
    print(max_list)
    for dish in ingred_dict.keys():
        if dish.dish_name not in stat_dict.keys():
            stat_dict[dish.dish_name] = [None, None, None]
        stat_dict[dish.dish_name][0] = len(ingred_dict[dish])
        if dish in max_list:
            stat_dict[dish.dish_name][1] = "<-"
        else:
            stat_dict[dish.dish_name][1] = ' '
        if dish in min_list:
            stat_dict[dish.dish_name][2] = "<-"
        else:
            stat_dict[dish.dish_name][2] = ' '
    return stat_dict

def get_sorted(stat_list: dict):
    return sorted(stat_list.values(), key=len)

def sort_by_len(elem):
    return len(elem)

def get_keys_from_value(input_dict: dict, val):
    keys = []

    for k, v in input_dict.items():
        if len(v) == val:
            keys.append(k)
    return keys

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


    ingreds = []
    if form.button_search3.data:
        for f_ingred in form.ingreds:
            ingred = f_ingred.data
            if ingred not in ingreds:
                ingreds.append(ingred)
        if len(ingreds):
            dish = get_min_dishes(ingreds)
            print(dish)
            dish_id = [elem.id_dish for elem in dish]
            dishes = get_dish_ingred(dish_id)
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

    if form.button_search2_add.data:
        form.ingreds.append_entry()
        return render_template('beauty_dish.html', dish=new_dishes, ingreds=ingreds, form=form)

    if form.button_search2_remove.data:
        form.ingreds.pop_entry()
        return render_template('beauty_dish.html', dish=new_dishes, ingreds=ingreds, form=form)


    return render_template('beauty_dish.html', dish=new_dishes, ingreds=ingreds, form=form)

def get_min_dishes(ingreds : list):
    all_dishes = mydb.session.query(Dish_Ingredient)
    dishes = mydb.session.query(Dish)
    ingreds_dict = get_ingreds_for_dishes(dishes, all_dishes)
    min_dishes = []
    ingreds = [elem.id_ingred for elem in ingreds]
    for dish in ingreds_dict.keys():
        if contains(ingreds_dict[dish], ingreds):
            min_dishes.append(dish.id_dish)
    print('min dishes ')
    print(min_dishes)
    return get_dish_ingred(min_dishes)

def get_ingreds_for_dishes(dishes: list, dishes_ingreds: list):
    ingreds_dict = {}
    for dish in dishes:
        if not ingreds_dict.keys().__contains__(dish):
            ingreds_dict[dish] = []
    for dish in dishes_ingreds:
        ingreds_dict[dish.dish].append(dish.id_ingred)
    return ingreds_dict

def get_dish_ingred(dishes_id: list):
    new_dish_ingreds = []
    dish_ingreds = mydb.session.query(Dish_Ingredient).all()
    print(dish_ingreds)
    for elem in dish_ingreds:
        print(elem)
        print(elem.id_dish)
        print(dishes_id)
        if elem.id_dish in dishes_id:
            new_dish_ingreds.append(elem)
    print(new_dish_ingreds)
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
