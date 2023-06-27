from django.test import TestCase
from posts.models import PostModel, Report, Comment, Image, SendPost, Like
from accounts.models import MyUser
from django.utils import timezone


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.post = PostModel.objects.create(
            user=self.user,
            caption='Test caption',
            slug='test-post',
            is_active=True
        )

    def test_report_post(self):
        reporter = MyUser.objects.create_user(
            email='reporter@example.com',
            username='reporter',
            password='reporterpassword'
        )
        reason = 'This post violates the community guidelines.'
        self.post.report_post(reporter, reason)
        self.assertEqual(Report.objects.count(), 1)
        report = Report.objects.first()
        self.assertEqual(report.user, reporter)
        self.assertEqual(report.post, self.post)
        self.assertEqual(report.reason, reason)


class ImageModelTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.post = PostModel.objects.create(
            user=self.user,
            caption='Test caption',
            slug='test-post',
            is_active=True
        )
        self.image = Image.objects.create(
            name='Test image',
            alt='Test image',
            image='test-image.jpg',
            post=self.post
        )

    def test_image_creation(self):
        self.assertEqual(Image.objects.count(), 1)
        image = Image.objects.first()
        self.assertEqual(image.name, 'Test image')
        self.assertEqual(image.alt, 'Test image')
        self.assertEqual(image.image, 'test-image.jpg')
        self.assertEqual(image.post, self.post)


class LikeModelTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.post = PostModel.objects.create(
            user=self.user,
            caption='Test caption',
            slug='test-post',
            is_active=True
        )
        self.like = Like.objects.create(
            user=self.user,
            post=self.post
        )

    def test_like_creation(self):
        self.assertEqual(Like.objects.count(), 1)
        like = Like.objects.first()
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )
        self.post = PostModel.objects.create(
            user=self.user,
            caption='Test caption',
            slug='test-post',
            is_active=True
        )
        self.comment = Comment.objects.create(
            comment_text='Test comment',
            user=self.user,
            post=self.post
        )

    def test_comment_creation(self):
        self.assertEqual(Comment.objects.count(), 1)
        comment = Comment.objects.first()
        self.assertEqual(comment.comment_text, 'Test comment')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)


class SendPostModelTestCase(TestCase):
    def setUp(self):
        self.sender = MyUser.objects.create_user(
            email='sender@example.com',
            username='senderuser',
            password='senderpassword'
        )
        self.recipient = MyUser.objects.create_user(
            email='recipient@example.com',
            username='recipientuser',
            password='recipientpassword'
        )
        self.post = PostModel.objects.create(
            user=self.sender,
            caption='Test caption',
            slug='test-post',
            is_active=True
        )
        self.send_post = SendPost.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            post=self.post,
            sent_at=timezone.now()
        )

    def test_send_post_creation(self):
        self.assertEqual(SendPost.objects.count(), 1)
        send_post = SendPost.objects.first()
        self.assertEqual(send_post.sender, self.sender)
        self.assertEqual(send_post.recipient, self.recipient)
        self.assertEqual(send_post.post, self.post)
