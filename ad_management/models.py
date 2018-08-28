from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название компании')

    def __str__(self):
        return '{}'.format(self.name)


class PageType(models.Model):
    name = models.CharField(max_length=256, verbose_name='Тип URL')

    def __str__(self):
        return '{}'.format(self.name)


class Request(models.Model):
    name = models.TextField(verbose_name='Запрос')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания')

    def __str__(self):
        return '{}'.format(self.name)


class Advert(models.Model):
    head1 = models.TextField(verbose_name='Заголовок 1')
    head2 = models.TextField(verbose_name='Заголовок 2')
    text = models.TextField(verbose_name='Текст объявления')

    def __str__(self):
        return '{}'.format(self.head1)


class Page(models.Model):
    url = models.CharField(max_length=500, verbose_name='URL страницы')
    page_type = models.ForeignKey(PageType, on_delete=models.CASCADE, verbose_name='Тип URL')
    small_change = models.TextField(verbose_name='Тип мелкого изменения URL')
    comment = models.TextField(verbose_name='Описание мелк изм URL')

    def __str__(self):
        return '{}'.format(self.url)


class Experiment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name='Запрос')
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, verbose_name='Объявление')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='Страница')
    show = models.IntegerField(verbose_name='Показы', default=0)
    click = models.IntegerField(verbose_name='Клики', default=0)
    ctr = models.FloatField(verbose_name='CTR %', default=0)
    expense = models.FloatField(verbose_name='Расход (руб.)', default=0)
    depth = models.FloatField(verbose_name='Глубина (стр.)', blank=True, null=True)
    conversion = models.FloatField(verbose_name='Конверсия (%)', blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.request.name)


class ExperimentScheme(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, verbose_name='Запрос')
    advert = models.ForeignKey(Advert, on_delete=models.CASCADE, verbose_name='Объявление')
    page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name='Страница')
    completed = models.BooleanField(default=False)
