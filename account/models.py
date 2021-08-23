from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here


class MyUserManager(BaseUserManager):
    use_in_migration = True

    # переопределяем метод

    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)  # инициализация объекта
        user.set_password(password)  # set_password отвечает за хеширование нашего пароля
        user.create_activation_code()
        user.save(using=self._db)  # какую бд он будет использовать внутри скобки
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)  # set_password отвечает за хеширование нашего пароля
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

    # TODO: create activation code

    def create_activation_code(self):
        import hashlib
        string = self.email + str(self.id)
        encode_string = string.encode()
        md5_string = hashlib.md5(encode_string)
        activation_code = md5_string.hexdigest()
        self.activation_code = activation_code  # у каждого пользователя свой актив код
