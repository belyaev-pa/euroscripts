import openpyxl
from django.conf import settings
from django.db.models import Sum
from .models import *
from django.http import HttpResponse
import time


def save_file(mimetype):
    def saver(func):
        def wrapper(request, *args, **kw):
            result = func(request, *args, **kw)
            if isinstance(result, tuple):
                filename, data = result
                resp = HttpResponse(data, content_type=mimetype)
                resp['Content-Disposition'] = 'attachment; filename=%s' % filename
                return resp
            return result
        return wrapper
    return saver


def upload_scheme(file):
    t = time.time()
    print("start time upload_scheme - {}".format(str(time.time() - t)))
    wb = openpyxl.load_workbook(file)
    first_sheet = wb.sheetnames[0]
    worksheet = wb[first_sheet]
    for row in range(2, worksheet.max_row + 1):
        company_cell = "{}{}".format('A', row)
        request_cell = "{}{}".format('B', row)
        url_cell = "{}{}".format('C', row)
        url_type_cell = "{}{}".format('D', row)
        small_change_cell = "{}{}".format('E', row)
        comment_cell = "{}{}".format('F', row)
        head1_cell = "{}{}".format('G', row)
        head2_cell = "{}{}".format('H', row)
        text_cell = "{}{}".format('I', row)
        company = worksheet[company_cell].value
        request = worksheet[request_cell].value
        url = worksheet[url_cell].value
        url_type = worksheet[url_type_cell].value
        small_change = worksheet[small_change_cell].value
        comment = worksheet[comment_cell].value
        head1 = worksheet[head1_cell].value
        head2 = worksheet[head2_cell].value
        text = worksheet[text_cell].value
        # Если записей будет много необходимо переписать с использованием bulk_create
        url_type_obj, created = PageType.objects.get_or_create(name=url_type)
        url_obj, created = Page.objects.get_or_create(url=url,
                                                      defaults={'page_type': url_type_obj,
                                                                'small_change': small_change,
                                                                'comment': comment, })
        company_obj, created = Company.objects.get_or_create(name=company)
        request_obj, created = Request.objects.get_or_create(name=request, company=company_obj)
        advert_obj, created = Advert.objects.get_or_create(head1=head1, head2=head2,
                                                           defaults={'text': text, })
        ExperimentScheme.objects.get_or_create(request=request_obj,
                                               advert=advert_obj,
                                               page=url_obj,)
    print("end time upload_scheme - {}".format(str(time.time() - t)))


def upload_result(company_file, stat_file):
    t = time.time()
    print("start time upload_result - {}".format(str(time.time() - t)))
    wb = openpyxl.load_workbook(company_file)
    first_sheet = wb.sheetnames[0]
    worksheet = wb[first_sheet]
    company_cell = "{}{}".format('E', 7)
    company = worksheet[company_cell].value
    company_obj = Company.objects.get(name=company)
    experiment_scheme = ExperimentScheme.objects.filter(request__company=company_obj)
    request_list = dict()  # {request: list(head1, head2, url)]
    for row in range(12, worksheet.max_row + 1):
        request_cell = "{}{}".format('I', row)
        head1_cell = "{}{}".format('L', row)
        head2_cell = "{}{}".format('M', row)
        url_cell = "{}{}".format('R', row)
        request = worksheet[request_cell].value
        head1 = worksheet[head1_cell].value
        head2 = worksheet[head2_cell].value
        url = worksheet[url_cell].value
        object_request = experiment_scheme.filter(page__url=url,
                                                  advert__head1=head1,
                                                  advert__head2=head2,
                                                  request__name=request)
        if object_request.exists():
            request_list[request] = [head1, head2, url]
    wb = openpyxl.load_workbook(stat_file)
    first_sheet = wb.sheetnames[0]
    worksheet = wb[first_sheet]
    duration_cell = "{}{}".format('A', 3)
    duration = worksheet[duration_cell].value
    for row in range(6, worksheet.max_row + 1):
        request_cell = "{}{}".format('B', row)
        show_cell = "{}{}".format('C', row)
        click_cell = "{}{}".format('D', row)
        ctr_cell = "{}{}".format('E', row)
        expense_cell = "{}{}".format('F', row)
        depth_cell = "{}{}".format('H', row)
        conversion_cell = "{}{}".format('I', row)
        request = worksheet[request_cell].value
        if request not in request_list.keys():
            continue
        show = worksheet[show_cell].value
        click = worksheet[click_cell].value
        ctr = worksheet[ctr_cell].value
        expense = worksheet[expense_cell].value
        depth = worksheet[depth_cell].value
        conversion = worksheet[conversion_cell].value
        page_obj = Page.objects.get(url=request_list[request][2])
        advert_obj = Advert.objects.get(head1=request_list[request][0],
                                        head2=request_list[request][1])
        request_obj = Request.objects.get(name=request)
        Experiment.objects.create(request=request_obj,
                                  advert=advert_obj,
                                  page=page_obj,
                                  show=show,
                                  click=click,
                                  ctr=ctr,
                                  expense=expense,
                                  depth=depth,
                                  conversion=conversion,
                                  duration=duration, )
    experiment_ended = dict()
    for key, value in request_list.items():
        # phrase_frequency = phrase_with_phrase.aggregate(Sum('frequency'))
        experiment_list = Experiment.objects.filter(page__url=value[2],
                                                    advert__head1=value[0],
                                                    advert__head2=value[1],
                                                    request__name=key)
        if experiment_list.aggregate(Sum('show'))['show__sum'] > settings.CLICK_AMOUNT:
            experiment = ExperimentScheme.objects.get(page__url=value[2],
                                                      advert__head1=value[0],
                                                      advert__head2=value[1],
                                                      request__name=key)
            experiment.completed = True
            experiment.save()
            experiment_ended[key] = value
    wb = openpyxl.load_workbook(company_file)
    first_sheet = wb.sheetnames[0]
    worksheet = wb[first_sheet]
    for row in range(12, worksheet.max_row + 1):
        request_cell = "{}{}".format('I', row)
        head1_cell = "{}{}".format('L', row)
        head2_cell = "{}{}".format('M', row)
        text_cell = "{}{}".format('N', row)
        url_cell = "{}{}".format('R', row)
        request = worksheet[request_cell].value
        head1 = worksheet[head1_cell].value
        head2 = worksheet[head2_cell].value
        url = worksheet[url_cell].value
        if request in experiment_ended.keys():
            if len({head1, head2, url} & set(experiment_ended[request])) == 3:
                next_experiment = ExperimentScheme.objects.filter(page__url=experiment_ended[request][2],
                                                                  advert__head1=experiment_ended[request][0],
                                                                  advert__head2=experiment_ended[request][1],
                                                                  request__name=request,
                                                                  completed=False)
                if next_experiment.exists():
                    next_experiment = next_experiment.first()
                    worksheet[head1_cell].value = next_experiment.advert.head1
                    worksheet[head2_cell].value = next_experiment.advert.head2
                    worksheet[text_cell].value = next_experiment.advert.text
                    worksheet[url_cell].value = next_experiment.page.url
    print("end time upload_result - {}".format(str(time.time() - t)))
    return company_file


def make_report():
    wb = openpyxl.load_workbook('report.xlsx')
    first_sheet = wb.sheetnames[0]
    worksheet = wb[first_sheet]
    t = time.time()
    experiment_list = ExperimentScheme.objects.all().order_by('request__company__name')
    for row, obj in enumerate(experiment_list, 2):
        company_cell = "{}{}".format('A', row)
        request_cell = "{}{}".format('B', row)
        url_type_cell = "{}{}".format('C', row)
        small_change_cell = "{}{}".format('D', row)
        comment_cell = "{}{}".format('E', row)
        url_cell = "{}{}".format('F', row)
        head1_cell = "{}{}".format('G', row)
        head2_cell = "{}{}".format('H', row)
        text_cell = "{}{}".format('I', row)
        complete_cell = "{}{}".format('J', row)
        show_cell = "{}{}".format('K', row)
        click_cell = "{}{}".format('L', row)
        ctr_cell = "{}{}".format('M', row)
        expense_cell = "{}{}".format('N', row)
        depth_cell = "{}{}".format('O', row)
        conversion_cell = "{}{}".format('P', row)
        worksheet[company_cell].value = obj.request.company.name
        worksheet[request_cell].value = obj.request.name
        worksheet[url_type_cell].value = obj.page.page_type.name
        worksheet[small_change_cell].value = obj.page.small_change
        worksheet[comment_cell].value = obj.page.comment
        worksheet[url_cell].value = obj.page.url
        worksheet[head1_cell].value = obj.advert.head1
        worksheet[head2_cell].value = obj.advert.head2
        worksheet[text_cell].value = obj.advert.text
        worksheet[complete_cell].value = obj.completed
        experiment_obj = Experiment.objects.filter(page__url=obj.page.url,
                                                   advert__head1=obj.advert.head1,
                                                   advert__head2=obj.advert.head2,
                                                   request__name=obj.request.name)
        worksheet[show_cell].value = experiment_obj.aggregate(Sum('show'))['show__sum']
        worksheet[click_cell].value = experiment_obj.aggregate(Sum('click'))['click__sum']
        worksheet[ctr_cell].value = experiment_obj.aggregate(Sum('ctr'))['ctr__sum']
        worksheet[expense_cell].value = experiment_obj.aggregate(Sum('expense'))['expense__sum']
        worksheet[depth_cell].value = experiment_obj.aggregate(Sum('depth'))['depth__sum']
        worksheet[conversion_cell].value = experiment_obj.aggregate(Sum('conversion'))['conversion__sum']
        print("next {} iter: {}".format(row, str(time.time() - t)))
    wb.save('report.xlsx')
    return open('report.xlsx', 'rb')
