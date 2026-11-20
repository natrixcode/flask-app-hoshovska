from sqlalchemy.orm import joinedload, selectinload
from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app import db
from app.posts import post_bp
from app.posts.forms import PostForm
from app.posts.models import Post, Tag
from app.users.models import User


@post_bp.route("/")
@post_bp.route("")
def all_posts():
    stmt = (
        db.select(Post)
        .options(
            joinedload(Post.user),
            selectinload(Post.tags),
        )
        .where(Post.is_active.is_(True))
        .order_by(Post.posted.desc(), Post.id.desc())
    )

    posts = db.session.scalars(stmt).all()

    return render_template(
        "posts/all_posts.html",
        posts=posts,
    )


@post_bp.route("/<int:id>")
def detail_post(id):
    stmt = (
        db.select(Post)
        .options(
            joinedload(Post.user),
            selectinload(Post.tags),
        )
        .where(Post.id == id)
    )

    post = db.first_or_404(stmt)

    return render_template(
        "posts/detail_post.html",
        post=post,
    )


def populate_post(form, post):
    post.title = form.title.data
    post.content = form.content.data
    post.category = form.category.data
    post.posted = form.publish_date.data
    post.is_active = form.enabled.data
    post.user_id = form.author_id.data


def set_author_choices(form):
    users = db.session.scalars(db.select(User).order_by(User.username)).all()

    form.author_id.choices = [(user.id, user.username) for user in users]


def set_tag_choices(form):
    tags = db.session.scalars(db.select(Tag).order_by(Tag.name)).all()

    form.tag_ids.choices = [(tag.id, tag.name) for tag in tags]


def save_post_tags(form, post):
    selected_ids = form.tag_ids.data or []

    post.tags = db.session.scalars(
        db.select(Tag).where(Tag.id.in_(selected_ids))
    ).all()


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()
    set_author_choices(form)
    set_tag_choices(form)

    if form.validate_on_submit():
        post = Post()

        populate_post(form, post)
        save_post_tags(form, post)

        db.session.add(post)
        db.session.commit()

        flash(
            "Публікацію успішно створено",
            "success",
        )

        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template(
        "posts/add_post.html",
        form=form,
        editing=False,
    )


@post_bp.route(
    "/<int:id>/update",
    methods=["GET", "POST"],
)
def update_post(id):
    stmt = (
        db.select(Post)
        .options(
            joinedload(Post.user),
            selectinload(Post.tags),
        )
        .where(Post.id == id)
    )

    post = db.first_or_404(stmt)

    form = PostForm(obj=post)
    set_author_choices(form)
    set_tag_choices(form)

    if request.method == "GET":
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active
        form.author_id.data = post.user_id
        form.tag_ids.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        populate_post(form, post)
        save_post_tags(form, post)

        db.session.commit()

        flash(
            "Публікацію оновлено",
            "success",
        )

        return redirect(url_for("posts.detail_post", id=post.id))

    return render_template(
        "posts/add_post.html",
        form=form,
        editing=True,
        post=post,
    )


@post_bp.route(
    "/<int:id>/delete",
    methods=["GET", "POST"],
)
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()

        flash(
            "Публікацію видалено",
            "success",
        )

        return redirect(url_for("posts.all_posts"))

    return render_template(
        "posts/delete_confirm.html",
        post=post,
    )
