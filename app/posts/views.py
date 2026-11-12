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
from app.posts.models import Post


@post_bp.route("/")
@post_bp.route("")
def all_posts():
    stmt = (
        db.select(Post)
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
    post = db.get_or_404(Post, id)

    return render_template(
        "posts/detail_post.html",
        post=post,
    )


def populate_post(form, post):
    form.populate_obj(post)

    post.posted = form.publish_date.data
    post.is_active = form.enabled.data

    for name in ("publish_date", "enabled", "submit"):
        if name in post.__dict__:
            delattr(post, name)


@post_bp.route("/create", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if form.validate_on_submit():
        author = str(
            session.get("username") or "Anonymous"
        )[:20]

        post = Post(author=author)

        populate_post(form, post)

        db.session.add(post)
        db.session.commit()

        flash(
            "Публікацію успішно створено",
            "success",
        )

        return redirect(
            url_for("posts.detail_post", id=post.id)
        )

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
    post = db.get_or_404(Post, id)

    form = PostForm(obj=post)

    if request.method == "GET":
        form.publish_date.data = post.posted
        form.enabled.data = post.is_active

    if form.validate_on_submit():
        populate_post(form, post)

        db.session.commit()

        flash(
            "Публікацію оновлено",
            "success",
        )

        return redirect(
            url_for("posts.detail_post", id=post.id)
        )

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

        return redirect(
            url_for("posts.all_posts")
        )

    return render_template(
        "posts/delete_confirm.html",
        post=post,
    )
