from django.test import TestCase
from accounts.models import MyUser , Relationship

class MyUserTestCase(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(
            email="test@example.com",
            username="testuser",
            password="testpassword"
        )
    
    def test_str_representation(self):
        self.assertEqual(str(self.user), "test@example.com")
    
    def test_report_account(self):
        user2 = MyUser.objects.create_user(
            email="test2@example.com",
            username="testuser2",
            password="testpassword"
        )
        reason = "Spam"
        
        self.user.report_account(user2, reason)
        
        report = Report.objects.get(user=self.user, account=user2)
        self.assertEqual(report.reason, reason)

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
