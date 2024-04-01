from django.shortcuts import render
from django.views import View
from .models import Author, AuthorProfile, Entry, Tag
from django.db.models import Q, Max, Min, Avg, Count


class TrainView(View):
    def get(self, request):
        # Создайте здесь запросы к БД
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem')).values()
        self.answer1 = Author.objects.filter(self_esteem__in=max_self_esteem).values(
            'username')  # Какие авторы имеют самую высокую уровень самооценки(self_esteem)?
        self.answer2 = None  # TODO Какой автор имеет наибольшее количество опубликованных статей?
        self.answer3 = Entry.objects.filter(
            tags__name__in=['Кино', 'Музыка'])  # TODO Какие статьи содержат тег 'Кино' или 'Музыка' ?
        self.answer4 = (
            Author.objects.filter(gender='ж')).count()  # TODO Сколько авторов женского пола зарегистрировано в системе?
        self.answer5 = ((Author.objects.filter(status_rule=True)).count()) / (
            (Author.objects.all()).count())  # TODO Какой процент авторов согласился с правилами при регистрации?
        self.answer6 = AuthorProfile.objects.filter(stage__range=(1, 5))  # TODO Какие авторы имеют стаж от 1 до 5 лет?
        self.answer7 = Author.objects.aggregate(max_age=Max('age'))  # TODO Какой автор имеет наибольший возраст?
        self.answer8 = (Author.objects.filter(
            phone_number__isnull=False)).count()  # TODO Сколько авторов указали свой номер телефона?
        self.answer9 = Author.objects.filter(age__lt=25)  # TODO Какие авторы имеют возраст младше 25 лет?
        self.answer10 = None  # TODO Сколько статей написано каждым автором?

        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}

        return render(request, 'train_db/training_db.html', context=context)

