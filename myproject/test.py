#Unit test for flask application
import unittest
from flask_app import app, db, users, post

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        #the basedir lines could be added like the original db
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.app = app.test_client()
        db.create_all()
        pass

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    #login function test function
    def login(self, username, password):
        return self.app.post('/sign', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    #create account test function
    def create(self,email,username,password):
        return self.app.post('/create', data=dict(
            email=email,
            username=username,
            password=password
        ), follow_redirects=True)

    #reset password test function
    def password(self,email,username,password):
        return self.app.post('/password', data=dict(
            email=email,
            username=username,
            password=password
        ), follow_redirects=True)

    #logout test function
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    #add post test function
    def addpost(self,subject,title,description):
        return self.app.post('/addNew', data=dict(
            subject=subject,
            title = title,
            description = description,
        ), follow_redirects=True)

    #testing for authentificaion
    def test_account(self):
        rv = self.login('robin', '123456')
        self.assertEqual(rv.status_code, 200)
        rv = self.create('emeraldhu@icloud.com','robin','123')
        self.assertEqual(rv.status_code, 200)
        rv = self.create('emeraldhu@icloud.com','robin','123456')
        self.assertEqual(rv.status_code, 200)
        rv = self.create('emeraldhu@icloud.com','robin','123456')
        self.assertEqual(rv.status_code, 200)
        rv = self.create('emeraldhu@id.com','robin','123456')
        self.assertEqual(rv.status_code, 200)
        rv = self.login('robin', '123')
        self.assertEqual(rv.status_code, 200)
        rv = self.login('rob', '123456')
        self.assertEqual(rv.status_code, 200)
        rv = self.login('robin',123456)
        self.assertEqual(rv.status_code, 200)
        rv = self.logout()
        self.assertEqual(rv.status_code, 200)

    #authentification database test
    def test_db(self):
        user = users.User(
            email="emerldhu@ic.com",
            username="leoleo",
            password="123455"
        )
        db.session.add(user)
        db.session.commit()
        u_id = users.User.query.filter(users.User.username=="leoleo").first()
        assert u_id is not None

        u_id = users.User.query.filter(users.User.username=="leoleo").first()
        db.session.delete(u_id)
        db.session.commit()
        u_id = users.User.query.filter(users.User.username=="leoleo").first()
        assert u_id is None

    #testing for posting
    def test_post(self):
        rv = self.addpost('MOVIES', 'chicago','description here..')
        self.assertEqual(rv.status_code, 200)

    #posting database test
    def test_dbpost(self):
        user = users.User(
            email="emerldhu@ic.com",
            username="leoleo",
            password="123455"
        )
        db.session.add(user)
        db.session.commit()
        u_id = users.User.query.filter(users.User.username == "leoleo").first()

        p = post.Post(
            subject='MOVIES',
            title='test',
            description='test description',
            ownerId=u_id.id
        )
        db.session.add(p)
        db.session.commit()
        p_id = post.Post.query.filter(post.Post.title == "test").first()
        assert p_id is not None

        p_id = post.Post.query.filter(post.Post.title == "test").first()
        db.session.delete(p_id)
        db.session.commit()
        p_id = post.Post.query.filter(post.Post.title == "test").first()
        assert p_id is None

if __name__ == '__main__':
    unittest.main()