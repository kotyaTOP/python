from app_config import mydb
from models import Dish, Ingredient, Unit, Dish_Ingredient
from wtforms import validators, Form, SubmitField, IntegerField, StringField, FieldList
from wtforms_alchemy import ModelForm
from wtforms_alchemy.fields import QuerySelectField
from wtforms_alchemy.validators import Unique
from wtforms_components.fields import TimeField


class DishForm(ModelForm):
    class Meta:
        model = Dish

    dish_name = StringField('Название блюда', [validators.DataRequired()])
    recipe = StringField('Рецепт', [validators.DataRequired()])
    time = TimeField('Время', [validators.DataRequired()])
    button_save = SubmitField('Сохранить')


class IngredForm(ModelForm):
    class Meta:
        model = Ingredient

    ingred_name = StringField('Название ингредиента', [validators.DataRequired()])
    button_save = SubmitField('Сохранить')


class UnitForm(ModelForm):
    class Meta:
        model = Unit

    unit_name = StringField('Единица измерения', [validators.DataRequired()])
    button_save = SubmitField('Сохранить')


class DishIngredForm(ModelForm):
    class Meta:
        model = Dish_Ingredient

    dish = QuerySelectField('Блюдо',
                            query_factory=lambda: mydb.session.query(Dish).all(),
                            get_pk=lambda g: g.id_dish,
                            get_label=lambda g: "%s" % (g.dish_name))
    # id_dish = IntegerField('Айди блюда', [validators.DataRequired()])
    ingred = QuerySelectField('Ингредиент',
                              query_factory=lambda: mydb.session.query(Ingredient).all(),
                              get_pk=lambda g: g.id_ingred,
                              get_label=lambda g: "%s" % (g.ingred_name))
    unit = QuerySelectField('Единица измерения',
                            query_factory=lambda: mydb.session.query(Unit).all(),
                            get_pk=lambda g: g.id_unit,
                            get_label=lambda g: "%s" % (g.unit_name))
    sum = IntegerField('Количество', [validators.DataRequired()])
    button_save = SubmitField('Сохранить')


class FormSearch(Form):
    dish_name = StringField('Название блюда')
    sum = IntegerField("Количество ингредиентов")
    ingred_names = StringField('Список ингредиентов (через пробел)')
    # ingred = QuerySelectField('Ингредиент',
    #                           query_factory=lambda: mydb.session.query(Ingredient).all(),
    #                           get_pk=lambda g: g.id_ingred,
    #                           get_label=lambda g: "%s" % (g.ingred_name))
    button_search3 = SubmitField('Поиск по ингредиентам')
    button_search1 = SubmitField('Поиск по названию')
    button_search2 = SubmitField('Установить')

    def set_ingred(self, k: int):
        for i in range(k):
            self.ingred = []
            ing_tmp = QuerySelectField('Ингредиент',
                              query_factory=lambda: mydb.session.query(Ingredient).all(),
                              get_pk=lambda g: g.id_ingred,
                              get_label=lambda g: "%s" % (g.ingred_name))
            self.ingred.append(ing_tmp)



# class SearchDishForm(Form):
#     class Meta:
#         model = Ingredient
#     ingred = QuerySelectField('Ингредиент',
#                               query_factory=lambda: mydb.session.query(Ingredient).all(),
#                               get_pk=lambda g: g.id_ingred,
#                               get_label=lambda g: "%s" % (g.ingred_name))
#     button_search1 = SubmitField('Поиск')