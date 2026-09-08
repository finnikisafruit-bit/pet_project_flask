from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from db import db_session
from forms import ProductForm
from models import Product

bp = Blueprint("items", __name__)


@bp.route("/")
def home():
    items = db_session.query(Product).all()
    return render_template(
        "home.html",
        title="Карточки объявлений",
        text="Тут будут карточки объявлений с товарами",
        items=items,
    )


@bp.route("/about")
def about():
    return render_template(
        "about.html", title="О компании", text="Нудл дудл компания из Люберец"
    )


@bp.route("/item/<int:item_id>")
def item_page(item_id):
    item = db_session.get(Product, item_id)
    if item is None:
        return "Не найден", 404
    return render_template(
        "item_page.html",
        title="Карточкa товара",
        text="Тут данные конкретного товара",
        item=item,
    )


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add_item():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            price=form.price.data,
            size=form.size.data,
            user_id=current_user.id,
        )
        db_session.add(product)
        db_session.commit()
        flash("Товар добавлен", "success")
        return redirect(url_for("items.home"))
    return render_template("add.html", form=form)


@bp.route("/item/<int:item_id>/delete", methods=["POST"])
@login_required
def delete_item(item_id):
    item = db_session.get(Product, item_id)
    if item is None:
        return "Не найден", 404
    if item.user_id != current_user.id:
        return "Нет доступа", 403
    db_session.delete(item)
    db_session.commit()
    flash("Товар удалён", "success")
    return redirect(url_for("items.my_items"))


@bp.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
@login_required
def edit_item(item_id):
    item = db_session.get(Product, item_id)
    if item is None:
        return "Не найден", 404
    if item.user_id != current_user.id:
        return "Нет доступа", 403

    form = ProductForm(obj=item)
    form.submit.label.text = "Сохранить"

    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.size = form.size.data
        db_session.commit()
        flash("Товар обновлён", "success")
        return redirect(url_for("items.item_page", item_id=item.id))
    return render_template("edit_item.html", form=form, item=item)


@bp.route("/my_items")
@login_required
def my_items():
    items = db_session.query(Product).filter_by(user_id=current_user.id).all()
    return render_template(
        "my_items.html",
        title="Мои товары",
        items=items,
    )
