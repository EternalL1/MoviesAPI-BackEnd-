from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import MaxValueValidator, MinValueValidator

class UserManager(BaseUserManager):
    def create_user(self, email, phoneNumber, fullName, password=None):
        if not email and not phoneNumber:
            raise ValueError('Users must have either an email address or phone number')
        user = self.model(email=email, phoneNumber=phoneNumber, fullName=fullName)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phoneNumber, fullName, password=None):
        user = self.create_user(email=email, phoneNumber=phoneNumber, fullName=fullName, password=password)
        user.role = 'admin'
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )

    email = models.EmailField(unique=True, null=True, blank=True)
    phoneNumber = models.CharField(max_length=13, unique=True, null=True, blank=True)
    fullName = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phoneNumber', 'fullName']

    def __str__(self):
        return self.email if self.email else self.phoneNumber

    def has_perm(self, perm, obj=None):
        return self.role == 'admin'

    def has_module_perms(self, app_label):
        return self.role == 'admin'

    @property
    def is_staff(self):
        return self.role == 'admin'


class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.DurationField()
    video_url = models.URLField() 
    poster_image = models.URLField(null=True, blank=True)
    main_cast = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    average_rating = models.FloatField(default=0, validators=[MaxValueValidator(10)])

    def __str__(self):
        return self.title

    def get_formatted_release_date(self):
        return self.release_date.strftime('%B %d, %Y')

    def get_duration_in_hours(self):
        total_seconds = self.duration.total_seconds()
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"
    
    def update_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            avg = sum(review.rating for review in reviews) / len(reviews)
            self.average_rating = round(avg, 1)
            self.save()



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    review_text = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.fullName} - {self.movie.title} ({self.rating} Stars)"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.movie.update_average_rating() 