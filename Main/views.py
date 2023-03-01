import re
from .forms import EmailForm
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .forms import EntryForm, AuthentificationForm
from .models import Entry


def upload_csv(request):
    data = {}
    if request.method == 'GET':
        return render(request, 'Main/upload/upload.html', data)
    try:
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'Please upload a .csv file')
            return HttpResponseRedirect(reverse('Main:upload_csv'))
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB). " % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("Main:upload_csv"))
        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        # loop over the lines and save them to db via model
        for line in lines:
            fields = line.split(",")
            try:
                status1 = bool(1)
                if fields[8] == 'true':
                    status1 = True
                elif fields[8] == 'false':
                    status1 = False
                if re.fullmatch('[A-Z][a-z]{2}[0-9]{6}', fields[6]):
                    entry = Entry(
                        nume=str(re.sub('[^A-z]', '', str(fields[0]))).capitalize(),
                        prenume=fields[1],
                        facultate=fields[2],
                        specialitate=fields[3],
                        functie=fields[4],
                        email=fields[5],
                        password=fields[6],
                        note=fields[7],
                        status=status1
                    )
                    entry.save()
                else:
                    messages.error(request, "Password don't match for " + fields[0] + " " + fields[1])
            except Exception as e:
                messages.error(request, "Unable to upload file. " + repr(e))
                pass
    except Exception as e:
        messages.error(request, "Unable to upload file. " + repr(e))
    return HttpResponseRedirect(reverse("Main:upload_csv"))


def new_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Main:main')
    else:
        form = EntryForm()
    return render(request, 'Main/entry/new_entry.html', {'form': form})


def edit_entry(request, pk):
    entry = get_object_or_404(Entry, pk=pk)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('Main:main')
    else:
        form = EntryForm(instance=entry)
    return render(request, 'Main/entry/edit_entry.html', {'form': form})


class entrys(ListView):
    table = Entry.objects.all()
    context_object_name = 'table'
    model = Entry
    template_name = 'Main/entry/table.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('by') == '1':
            query = self.request.GET.get('q')
            if not query:
                query = ""

            multiquery = query.split(" ")
            print(query)
            object_list = Entry.objects.filter(
                Q(nume__icontains=query) | Q(prenume__icontains=query) |
                (Q(nume__in=multiquery) & Q(prenume__in=multiquery))
            )
            return object_list
        elif self.request.GET.get('by') == '2':
            query = self.request.GET.get('q')
            if not query:
                query = ""
            print(query)
            object_list = Entry.objects.filter(
                Q(specialitate__icontains=query) | Q(facultate__icontains=query)
            )
            return object_list
        elif self.request.GET.get('by') == '3':
            query = self.request.GET.get('q')
            if not query:
                query = ""
            print(query)
            object_list = Entry.objects.filter(
                Q(email__icontains=query)
            )
            return object_list

        query = self.request.GET.get('q')

        if not query:
            query = ""

        multiquery = query.split(" ")
        print(query)
        object_list = Entry.objects.filter(
            Q(nume__icontains=query) | Q(prenume__icontains=query)
            | Q(specialitate__icontains=query) | Q(facultate__icontains=query) |
            (Q(nume__in=multiquery) & Q(prenume__in=multiquery))
        )
        return object_list


class HomePageView(TemplateView):
    template_name = 'Main/base.html'


def post_share(request, pk):
    # Retrieve post by id
    post = get_object_or_404(Entry, id=pk)
    if request.method == 'POST':
        # Form was submitted
        form = EmailForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # ... send email
    else:
        form = EmailForm()
    return render(request, 'Main/share/share.html', {'post': post,
                                                     'form': form})
