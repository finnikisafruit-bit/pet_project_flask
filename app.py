from flask import Flask, flash, redirect, render_template, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from config import SECRET_KEY
from db import db_session
from forms import EditProfileForm, LoginForm, RegisterForm, ProductForm
from models import Product, User

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db_session.get(User, int(user_id))


@app.route("/")
def home():
    items = db_session.query(Product).all()
    return render_template(
        "home.html",
        title="Карточки объявлений",
        text="Тут будут карточки объявлений с товарами",
        items=items,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db_session.add(user)
        db_session.commit()
        flash("Регистрация успешна", "success")
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session.query(User).filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("Вы вошли", "success")
            return redirect(url_for("home"))
        return "Неверный логин и пароль", 401
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("Вы вышли", "info")
    return redirect(url_for("home"))


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/profile/edit", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)
        db_session.commit()
        flash("Профиль обновлён", "success")
        return redirect(url_for("profile"))
    return render_template("edit_profile.html", form=form)


@app.route("/about")
def about():
    return render_template(
        "about.html", title="О компании", text="Нудл дудл компания из Люберец"
    )


@app.route("/item/<int:item_id>")
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


@app.route("/add", methods=["GET", "POST"])
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
        return redirect(url_for("home"))
    return render_template("add.html", form=form)


@app.route("/item/<int:item_id>/delete", methods=["POST"])
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
    return redirect(url_for("my_items"))


@app.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
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
        return redirect(url_for("item_page", item_id=item.id))
    return render_template("edit_item.html", form=form, item=item)


@app.route("/my_items")
@login_required
def my_items():
    items = db_session.query(Product).filter_by(user_id=current_user.id).all()
    return render_template(
        "my_items.html",
        title="Мои товары",
        items=items,
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=True)
