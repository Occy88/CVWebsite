from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import reverse

from folders.models import Document
from folders.forms import DocumentForm

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('folders:list'))
    else:
        form = DocumentForm() # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()
    context = {'documents':documents,'form':form}
    # Render list page with the documents and the form
    return render(
        request,'folders/templates/list.html',context
    )

def index(request):
    return render('myapp/index.html')