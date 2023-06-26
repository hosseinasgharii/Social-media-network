from django.test import TestCase
from posts.models import PostModel, Report, Comment
from accounts.models import MyUser

class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword"
        )
        self.post = PostModel.objects.create(
            user=self.user,
            caption="Test post",
            slug="test-post"
        )
    
    def test_like_post(self):
        user2 = MyUser.objects.create_user(
            email="test2@example.com",
            username="testuser2",
            password="testpassword"
        )
        
        self.post.like_post(user2)
        self.assertTrue(self.post.likes.filter(id=user2.id).exists())

    def test_unlike_post(self):
        user2 = MyUser.objects.create_user(
            email="test2@example.com",
            username="testuser2",
            password="testpassword"
        )
        self.post.likes.add(user2)
        
        self.post.unlike_post(user2)
        self.assertFalse(self.post.likes.filter(id=user2.id).exists())

    def test_has_liked_post(self):
        user2 = MyUser.objects.create_user(
            email="test2@example.com",
            username="testuser2",
            password="testpassword"
        )
        self.post.likes.add(user2)
        
        self.assertTrue(self.post.has_liked_post(user2))
        self.assertFalse(self.post.has_liked_post(self.user))

    def test_report_post(self):
        user2 = MyUser.objects.create_user(
            email="test2@example.com",
            username="testuser2",
            password="testpassword"
        )
        reason = "Inappropriate content"
        
        self.post.report_post(user2, reason)
        
        report = Report.objects.get(user=user2, post=self.post)
        self.assertEqual(report.reason, reason)

class ImageTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword"
        )
        self.post = PostModel.objects.create(
            user=self.user,
            caption="Test post",
            slug="test-post"
        )
        self.image = Image.objects.create(
            name="Test Image",
            alt="Test Image",
            image="test_image.jpg",
            post=self.post
        )
    
    def test_str_representation(self):
        self.assertEqual(str(self.image), "Test Image")

class CommentTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword"
        )
        self.post = PostModel.objects.create(
            user=self.user,
            caption="Test post",
            slug="test-post"
        )
        self.comment = Comment.objects.create(
            comment_text="Test comment",
            user=self.user,
            post=self.post
        )
    
    def test_str_representation(self):
        self.assertEqual(str(self.comment), "comment on test-post")

class ReportTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword"
        )
        self.post = PostModel.objects.create(
            user=self.user,
            caption="Test post",
            slug="test-post"
        )
        self.account = MyUser.objects.create_user(
            email="account@example.com",
            username="testaccount",
            password="testpassword"
        )
        self.report1 = Report.objects.create(
            user=self.user,
            post=self.post,
            reason="Inappropriate content"
        )
        self.report2 = Report.objects.create(
            user=self.user,
            account=self.account,
            reason="Spam"
        )
    