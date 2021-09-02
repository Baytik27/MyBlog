from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here

# переопределяем класс BaseUserManager , создаем свой класс
class MyUserManager(BaseUserManager):
    use_in_migration = True

    # переопределяем метод
    # создаем обычного user
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)   # проверяет на нормализации email
        user = self.model(email=email)  # инициализация объекта
        user.set_password(password)  # set_password отвечает за хеширование нашего пароля
        user.create_activation_code()  # после активации кода user станет активным
        user.save(using=self._db)  # какую бд он будет использовать внутри скобки
        return user

        # создаем superuser

    def create_superuser(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)  # set_password отвечает за хеширование нашего пароля
        user.is_active = True  # по умолчанию будет активным
        user.is_staff = True  # права супер полюзователя
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractUser):   # переопределяем класс AbstractUser , создаем свой класс
    username = None   # по умолчанию не будет username
    email = models.EmailField(unique=True)  # поле email, будем зарегистрироваться через email
    is_active = models.BooleanField(default=False)   # поле, по умолчанию пользователь буддет не активным
    activation_code = models.CharField(max_length=50, blank=True)  # активационный код чтобы активировать  пользователя

    USERNAME_FIELD = 'email'  # будем зарегистрироваться через email ,ф не username
    REQUIRED_FIELDS = []

    objects = MyUserManager()  # manger будет MyUserManager которую мы переопределили

    def __str__(self):
        return self.email

    # TODO: create activation code
    def create_activation_code(self):   # <- содаем функцию для активации пользователя
        import hashlib  # импортируем hashlib чтобы захешировать активационный код
        string = self.email + str(self.id)
        encode_string = string.encode()
        md5_string = hashlib.md5(encode_string)
        activation_code = md5_string.hexdigest()
        self.activation_code = activation_code  # у каждого пользователя свой актив код
