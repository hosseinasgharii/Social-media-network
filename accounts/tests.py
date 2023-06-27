from django.test import TestCase
from accounts.models import MyUser, Relationship, Report


class MyUserModelTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpassword'
        )

    def test_report_account(self):
        user = MyUser.objects.create_user(
            email='reporter@example.com',
            username='reporter',
            password='reporterpassword'
        )
        reason = 'This user violated the terms of service.'
        self.user.report_account(user, reason)
        self.assertEqual(Report.objects.count(), 1)
        report = Report.objects.first()
        self.assertEqual(report.user, user)
        self.assertEqual(report.account, self.user)
        self.assertEqual(report.reason, reason)

    def test_block_user(self):
        user_to_block = MyUser.objects.create_user(
            email='blocked@example.com',
            username='blockeduser',
            password='blockedpassword'
        )
        self.user.block_user(user_to_block)
        self.assertTrue(self.user.is_blocked(user_to_block))

    def test_unblock_user(self):
        user_to_block = MyUser.objects.create_user(
            email='blocked@example.com',
            username='blockeduser',
            password='blockedpassword'
        )
        self.user.block_user(user_to_block)
        self.assertTrue(self.user.is_blocked(user_to_block))
        self.user.unblock_user(user_to_block)
        self.assertFalse(self.user.is_blocked(user_to_block))


class RelationshipTestCase(TestCase):
    def setUp(self):
        self.user1 = MyUser.objects.create_user(
            email="user1@example.com",
            username="user1",
            password="testpassword"
        )
        self.user2 = MyUser.objects.create_user(
            email="user2@example.com",
            username="user2",
            password="testpassword"
        )
        self.relationship = Relationship.objects.create(
            follower=self.user1,
            following=self.user2
        )

    def test_str_representation(self):
        self.assertEqual(str(self.relationship), "user1 -> user2")
