from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from .forms import FileUpload, ResultUpload
from .snippets import upload_scheme, upload_result, save_file, make_report


# Create your views here.
def index(request):
    form = FileUpload()
    form2 = ResultUpload()
    content = {'form': form, 'form2': form2, }
    return render(request, 'ad_management/index.html', content)


def scheme_upload(request):
    if request.method == 'POST':
        form = FileUpload(request.POST, request.FILES)
        if form.is_valid():
            upload_scheme(request.FILES['file'])
    return HttpResponseRedirect(reverse('ad:index'))


@save_file(mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
def result_upload(request):
    if request.method == 'POST':
        form = ResultUpload(request.POST, request.FILES)
        if form.is_valid:
            excel = upload_result(request.FILES['company'], request.FILES['stat'])
            return ('new_company.xlsx', excel)
    #return HttpResponseRedirect(reverse('ad:index'))


@save_file(mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
def report(request):
    excel = make_report()
    return ('report.xlsx', excel)