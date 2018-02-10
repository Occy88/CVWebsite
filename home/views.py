from django.shortcuts import render
from django.http import Http404
from django.template import RequestContext
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import reverse,redirect, get_object_or_404

from home.models import Document,Group
from home.forms import DocumentForm, GroupRegistrationForm

def home(request):
    user=request.user
    context = {'user':user}
    return render(
        request, 'home/templates/home.html', context
    )
def group_detail_files(request,id=None):
    group=get_object_or_404(Group, id=id)
    thief=True
    for u in group.members.all():
        if u==request.user:
            thief=False
    if thief:
        raise Http404
    document=Document.objects.all()
    context = {'group':group,'document':document}
    return render(
        request, 'home/templates/home_groups_specified_files.html', context
    )
def group_detail_files_upload(request,id=None):
    # Handle file upload
    group = get_object_or_404(Group, id=id)
    thief = True
    for u in group.members.all(x):
        if u == request.user:
            thief = False
    if thief:
        raise Http404

    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print(str(form.errors))
        if form.is_valid():
            print("valid")
            instance= form.save(commit=False)
            instance.group=group
            instance.save()

            return redirect(instance.get_absolute_url())
    else:
        form = DocumentForm()

    user=request.user
    context = {'form':form,'user':user,'id':id}
    # Render list page with the documents and the form
    return render( request,'home/templates/home_groups_specified_files_upload.html',context )

def group_detail_file_delete(request,id=None,idf=None):
    instanceF = get_object_or_404(Document, id=idf)
    instanceG = get_object_or_404(Group, id=id)
    thief = True
    for u in instanceG.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404

    instanceF.delete()
    return redirect(instanceG.get_absolute_url())
def group_list(request):

    groups = Group.objects.all()
    user=request.user
    context = {'groups': groups,'user':user}
    return render(
        request, 'home/templates/home_groups.html', context
    )
def group_edit(request,id=None):
    instance=get_object_or_404(Group,id=id)

    thief = True
    for u in instance.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    form= GroupRegistrationForm(request.POST or None,instance=instance)
    if form.is_valid():
        instance=form.save()
        instance.save()
        print(instance.get_absolute_url())
        return redirect(instance.get_absolute_url())

    user = request.user
    return render(request, 'home/templates/home_groups_edit.html', {'form': form, 'user': user})

def group_detail(request,id=None):
    instance=get_object_or_404(Group,id=id)
    thief = True
    for u in instance.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
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