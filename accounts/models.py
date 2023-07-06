from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            username=username
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Username"
        )
    firstname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="First Name"
        )
    lastname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Last Name"
        )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Bio"
        )
    male = 1
    female = 2
    choice_gender = ((male, "male"), (female, "female"))
    gender = models.IntegerField(
        choices=choice_gender,
        blank=True,
        null=True,
        verbose_name="Gender"
        )
    phonenumber = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name="Phone Number"
        )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        help_text="Provide a valid email address"
        )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date of Birth"
        )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active"
        )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="Admin"
        )
    blocked_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='blocked_by',
        verbose_name="Blocked Users"
    )
    is_delete = models.BooleanField(
        default=False,
        verbose_name="Deleted"
        )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def report_account(self, user, reason):
        Report.objects.create(user=user, account=self, reason=reason)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def block_user(self, user):
        """
        Blocks another user.
        """
        self.blocked_users.add(user)

    def unblock_user(self, user):
        """
        Unblocks a blocked user.
        """
        self.blocked_users.remove(user)

    def is_blocked(self, user):
        """
        Checks if the user is blocked.
        """
        return self.blocked_users.filter(id=user.id).exists()

    def follower_count(self):
        return self.following_relation.count()

    def following_count(self):
        return self.follower_relation.count()

    def get_followers(self):
        return self.following_relation.all()

    def get_following(self):
        return self.follower_relation.all()

    def post_count(self):
        return self.show_post.count()

    def posts(self):
        return self.show_post.all()

    def delete_account(self):
        self.is_deleted = True
        self.save()


class Relationship(models.Model):
    follower = models.ForeignKey(
        MyUser,
        related_name='follower_relation',
        related_query_name='follower_relation',
        on_delete=models.CASCADE,
        verbose_name="Follower"
        )
    following = models.ForeignKey(
        MyUser,
        related_name='following_relation',
        related_query_name='following_relation',
        on_delete=models.CASCADE,
        verbose_name="Following"
        )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created at"
        )

    def __str__(self):
        return f'{self.follower.username} -> {self.following.username}'


class Report(models.Model):
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="reporter_user"
        )
    account = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='reported_accounts',
        blank=True,
        null=True)
    reason = models.TextField(
        max_length=500
        )

    def __str__(self):
        if self.account:
            return f"Report on account: {self.account.username}"
        else:
            return "Invalid report"
