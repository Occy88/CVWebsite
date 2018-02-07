from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import reverse,redirect

from home.models import Document,Group
from home.forms import DocumentForm, GroupRegistrationForm

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('home:list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    user=User.objects.all()
    cu=request.user

    context = {'documents':documents,'form':form,'user':user,'cu':cu}
    # Render list page with the documents and the form
    return render(
        request,'home/templates/home.html',context
    )

def grouplist(request):
    groups = Group.objects.all()

    context = {'groups': groups}
    return render(
        request, 'home/templates/home_groups.html', context
    )

def groupregister(request):
    if request.method == 'POST':
        form = GroupRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('home:group_list'))
    else:
        form = GroupRegistrationForm()
    return render(request, 'home/templates/home_groups_create.html', {'form': form})
def index(request):
    return render('myapp/index.html')