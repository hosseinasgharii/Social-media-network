from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):

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
        verbose_name="Username",
        help_text="Enter a unique username."
    )
    firstname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="First Name",
        help_text="Enter your first name."
    )
    lastname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Last Name",
        help_text="Enter your last name."
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Bio",
        help_text="Enter a short bio about yourself."
    )
    male = 1
    female = 2
    choice_gender = ((male, "male"), (female, "female"))
    gender = models.IntegerField(
        choices=choice_gender,
        blank=True,
        null=True,
        verbose_name="Gender",
        help_text="Select your gender."
    )
    phonenumber = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name="Phone Number",
        help_text="Enter your phone number."
    )
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        help_text="Provide a valid email address."
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name="Date of Birth",
        help_text="Enter your date of birth."
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this user account is active."
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name="Admin",
        help_text="Designates whether this user is an administrator."
    )
    blocked_users = models.ManyToManyField(
        'self',
        symmetrical=False,
        blank=True,
        related_name='blocked_by',
        verbose_name="Blocked Users",
        help_text="Users blocked by this user."
    )
    is_delete = models.BooleanField(
        default=False,
        verbose_name="Deleted",
        help_text="Designates whether this user account is deleted."
    )

    objects = MyUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def report_account(self, user, reason):
        Report.objects.create(user=user, account=self, reason=reason)

    @property
    def is_staff(self):
        return self.is_admin

    def block_user(self, user):
        self.blocked_users.add(user)

    def unblock_user(self, user):
        self.blocked_users.remove(user)

    def is_blocked(self, user):
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
        self.delete()


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
        null=True
    )
    reason = models.TextField(
        max_length=500
    )

    def __str__(self):
        if self.account:
            return f"Report on account: {self.account.username}"
        else:
            return "Invalid report"
