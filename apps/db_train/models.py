from datetime import datetime

from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


class Author(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+79\d{9}$',
        message="Телефонный номер должен быть формата: '+79123456789'."
    )

    username = models.SlugField(verbose_name='имя авторского аккаунта',
                                help_text="Введите username, не длиннее 50 символов. Использовать нужно английский алфавит, разделять фразы нужно символом '-'",
                                unique=True)
    email = models.EmailField(verbose_name='email',
                              help_text="Адрес почты в формате *@*.*",
                              unique=True)
    first_name = models.CharField(max_length=100,
                                  verbose_name='Имя',
                                  help_text="Ограничение - не более 100 символов",
                                  null=True,
                                  blank=True
                                  )
    last_name = models.CharField(max_length=100,
                                 verbose_name='Фамилия',
                                 help_text="Ограничение - не более 100 символов",
                                 null=True,
                                 blank=True
                                 )
    middle_name = models.CharField(max_length=100,
                                   verbose_name='Отчество',
                                   help_text="Ограничение - не более 100 символов",
                                   null=True,
                                   blank=True
                                   )
    gender = models.CharField(max_length=1,
                              choices=[('ж', 'женский'), ('м', 'мужской')],
                              verbose_name='Пол',
                              help_text="Выберите пол",
                              null=True,
                              blank=True
                              )
    self_esteem = models.DecimalField(max_digits=2,
                                      decimal_places=1,
                                      verbose_name='уровень самооценки',
                                      validators=[MinValueValidator(0, "Диапазон [0.0, 5.0]"),
                                                  MaxValueValidator(5, "Диапазон [0.0, 5.0]")],
                                      help_text="Введите уровень вашей самооценки, только честно! Градация от 0 до 5, где 0 - 'я молодец', 5 - 'я умница'",
                                      null=True,
                                      blank=True
                                      )
    phone_number = models.CharField(max_length=12,
                                    verbose_name='номер телефона',
                                    validators=[phone_regex],
                                    help_text="Введите номер телефона через '+7' без пробелов в формате +79123456789 ",
                                    null=True,
                                    blank=True,
                                    unique=True
                                    )
    city = models.CharField(max_length=100,
                            verbose_name='город',
                            help_text="Введите название города",
                            null=True,
                            blank=True
                            )
    bio = models.TextField(verbose_name='биография',
                           help_text="Напишите здесь немного о себе...",
                           null=True,
                           blank=True
                           )
    age = models.IntegerField(null=True,
                              editable=False,
                              verbose_name='возраст')
    date_birth = models.DateField(verbose_name='дата рождения',
                                  help_text="Посланцев из будущего не регистрируем!",
                                  null=True,
                                  blank=True
                                  )
    status_rule = models.BooleanField(verbose_name='согласие с правилами',
                                      help_text="А ты их читал? Потом не жалуйся и не говори, что тебя не предупреждали...")
    image = models.ImageField(upload_to='foto_profile',
                              verbose_name='фото профиля',
                              help_text="Фото в профиль, можно не своё! Ну или хоть какое-то. Ладно можно без фото",
                              null=True,
                              blank=True
                              )
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='дата и время создания записи в БД')
    update_at = models.DateTimeField(auto_now=True, verbose_name='дата и время обновления записи в БД')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        initials = None  # Инициалы
        if self.first_name and self.middle_name:
            initials = f"{self.first_name.upper()[0]}.{self.middle_name.upper()[0]}."
        return f"{self.username} ({self.last_name} {initials})"

    def save(self, *args, **kwargs):
        if self.date_birth:  # Если известен день рождения
            today = datetime.today()  # Определяем текущие параметры даты
            # Определяем добавку, был ли уже день рождения в этом году? Если не был, то 1, если был, то 0
            additional_year = (today.month, today.day) < (self.date_birth.month, self.date_birth.day)
            self.age = today.year - self.date_birth.year - additional_year  # Перезаписываем значение
        super().save(*args, **kwargs)


class AuthorProfile(models.Model):
    author = models.OneToOneField('Author', on_delete=models.CASCADE)
    stage = models.IntegerField(default=0,
                                blank=True,
                                verbose_name="Стаж",
                                help_text="Стаж в годах")

    def __str__(self):
        return f'Автор {self.author.last_name} {self.author.first_name[0]}.{self.author.middle_name[0]}. Стаж: {self.stage} лет.'


class Entry(models.Model):
    text = models.TextField(verbose_name="Текст статьи",
                            )
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name='entries')
    tags = models.ManyToManyField("Tag", related_name='entries')

    def __str__(self):
        return f'{self.author.username} - {self.text[0:25]}'


class Tag(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Название",
                            )

    def __str__(self):
        return f'#{self.name}'
