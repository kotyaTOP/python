from app_config import mydb
from models import Dish, Ingredient, Unit, Dish_Ingredient
from wtforms import validators, Form, SubmitField, IntegerField, StringField
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

    dish_name = QuerySelectField('Блюдо',
                             query_factory=lambda: mydb.session.query(Dish).all(),
                             get_pk=lambda g: g.id_dish,
                             get_label=lambda g: "%s" % (g.dish_name))

    # id_dish = IntegerField('Айди блюда', [validators.DataRequired()])
    id_ingred = IntegerField('Айди ингредиента', [validators.DataRequired()])
    id_unit = IntegerField('Айди единицы', [validators.DataRequired()])
    sum = IntegerField('Количество', [validators.DataRequired()])
    button_save = SubmitField('Сохранить')

