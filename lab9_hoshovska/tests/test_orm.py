import unittest

from sqlalchemy import create_engine, select
from sqlalchemy.orm import (
    Session,
    joinedload,
    selectinload,
)
from sqlalchemy.pool import StaticPool

from app import db
from app.posts.models import Post, Tag
from app.users.models import User


class ORMRelationshipTests(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )

        db.Model.metadata.create_all(self.engine)

        self.session = Session(self.engine)

    def tearDown(self):
        self.session.close()
        db.Model.metadata.drop_all(self.engine)
        self.engine.dispose()

    def create_sample_data(self):
        user = User(username="TestUser")

        python_tag = Tag(name="Python")
        flask_tag = Tag(name="Flask")

        post = Post(
            title="Тестова публікація",
            content="Перевірка ORM-зв'язків.",
            category="tech",
            user=user,
            tags=[python_tag, flask_tag],
        )

        self.session.add(post)
        self.session.commit()

        return user, post, python_tag, flask_tag

    def test_create_post(self):
        _, post, _, _ = self.create_sample_data()

        saved = self.session.get(Post, post.id)

        self.assertIsNotNone(saved)
        self.assertEqual(
            saved.title,
            "Тестова публікація",
        )

    def test_one_to_many_relationship(self):
        user, post, _, _ = self.create_sample_data()

        self.assertEqual(post.user.id, user.id)
        self.assertIn(post, user.posts)

    def test_many_to_many_relationship(self):
        _, post, python_tag, flask_tag = (
            self.create_sample_data()
        )

        self.assertEqual(len(post.tags), 2)
        self.assertIn(python_tag, post.tags)
        self.assertIn(flask_tag, post.tags)
        self.assertIn(post, python_tag.posts)

    def test_eager_loading(self):
        self.create_sample_data()

        self.session.expunge_all()

        stmt = (
            select(Post)
            .options(
                joinedload(Post.user),
                selectinload(Post.tags),
            )
        )

        post = self.session.scalars(stmt).first()

        self.assertEqual(
            post.user.username,
            "TestUser",
        )
        self.assertEqual(len(post.tags), 2)

    def test_update_post(self):
        _, post, _, _ = self.create_sample_data()

        post.title = "Оновлена публікація"
        self.session.commit()

        saved = self.session.get(Post, post.id)

        self.assertEqual(
            saved.title,
            "Оновлена публікація",
        )

    def test_delete_post(self):
        _, post, _, _ = self.create_sample_data()

        post_id = post.id

        self.session.delete(post)
        self.session.commit()

        self.assertIsNone(
            self.session.get(Post, post_id)
        )


if __name__ == "__main__":
    unittest.main()
