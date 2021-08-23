from django.db import models

# Create your models here.
from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=255, primary_key=True)   # первичный ключ чтобы не создавалась id поле
    name = models.CharField(max_length=279, unique=True)

    def __str__(self):
        return self.slug


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=266)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_date', )

    def __str__(self):
        return self.author


class Rating(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='ratings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    grade = models.PositiveIntegerField()

    def __str__(self):
        return self.author


class Like(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.author


class Favorites(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorites')
    name = models.CharField(max_length=50, default='Избранное')

    def __str__(self):
        return self.author
