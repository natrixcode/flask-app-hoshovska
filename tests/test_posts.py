import unittest
from datetime import datetime
from app import create_app, db
from app.posts.models import Post

class PostTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def add_post(self, title='Тестовий пост', active=True):
        post = Post(title=title, content='Текст тестової публікації', category='news', is_active=active, posted=datetime(2026, 11, 10))
        db.session.add(post)
        db.session.commit()
        return post.id

    def form_data(self, title='Новий пост', enabled=True):
        data = {'title': title, 'content': 'Тестовий текст', 'category': 'tech', 'publish_date': '2026-11-10T12:00'}
        if enabled:
            data['enabled'] = 'y'
        return data

    def test_create_post(self):
        r = self.client.post('/post/create', data=self.form_data(), follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(db.session.scalar(db.select(db.func.count(Post.id))), 1)
        self.assertEqual(db.session.scalar(db.select(Post)).author, 'Anonymous')

    def test_list_posts(self):
        self.add_post('Видимий')
        self.add_post('Прихований', False)
        r = self.client.get('/post')
        self.assertIn('Видимий'.encode(), r.data)
        self.assertNotIn('Прихований'.encode(), r.data)

    def test_detail_post(self):
        post_id = self.add_post()
        r = self.client.get(f'/post/{post_id}')
        self.assertEqual(r.status_code, 200)
        self.assertIn('Тестовий пост'.encode(), r.data)

    def test_update_post(self):
        post_id = self.add_post()
        r = self.client.post(f'/post/{post_id}/update', data=self.form_data('Змінений заголовок'), follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(db.session.get(Post, post_id).title, 'Змінений заголовок')

    def test_delete_post(self):
        post_id = self.add_post()
        r = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIsNone(db.session.get(Post, post_id))

    def test_not_found(self):
        r = self.client.get('/post/99999')
        self.assertEqual(r.status_code, 404)

    def test_validation(self):
        r = self.client.post('/post/create', data=self.form_data(title=''))
        self.assertEqual(r.status_code, 200)
        self.assertEqual(db.session.scalar(db.select(db.func.count(Post.id))), 0)

    def test_session_author(self):
        with self.client.session_transaction() as sess:
            sess['username'] = 'Natalia'
        self.client.post('/post/create', data=self.form_data())
        self.assertEqual(db.session.scalar(db.select(Post)).author, 'Natalia')

if __name__ == '__main__':
    unittest.main()
