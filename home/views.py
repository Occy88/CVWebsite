from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from home.models import Document
from home.forms import DocumentForm

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

def index(request):
    return render('myapp/index.html')