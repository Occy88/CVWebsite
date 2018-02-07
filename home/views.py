from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import reverse,redirect, get_object_or_404

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
    user=request.user


    context = {'documents':documents,'form':form,'user':user}
    # Render list page with the documents and the form
    return render( request,'home/templates/home.html',context )

def group_list(request):
    groups = Group.objects.all()
    user=request.user
    context = {'groups': groups,'user':user}
    return render(
        request, 'home/templates/home_groups.html', context
    )
def group_edit(request,id=None):
    instance=get_object_or_404(Group,id=id)
    form= GroupRegistrationForm(request.POST or None,instance=instance)
    if form.is_valid():
        instance=form.save()
        instance.save()

        return redirect('home:group_list')

    user = request.user
    return render(request, 'home/templates/home_groups_edit.html', {'form': form, 'user': user})

def group_detail(request,id=None):
    instance=get_object_or_404(Group,id=id)
    context = {'id':id,'name': instance.name, 'members': instance.members}
    return render(
        request, 'home/templates/home_groups_specified.html', context)
def group_delete(request,id=None):
    instance=get_object_or_404(Group,id=id)
    instance.delete()
    return redirect('home:group_list')

def group_register(request):
    if request.method == 'POST':
        form = GroupRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse('home:group_list'))
    else:
        form = GroupRegistrationForm()
    user = request.user
    return render(request, 'home/templates/home_groups_create.html', {'form': form,'user':user})
def index(request):
    return render('myapp/index.html')