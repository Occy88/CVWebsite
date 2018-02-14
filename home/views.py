from django.shortcuts import render
from django.http import Http404,StreamingHttpResponse,HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User

from django.shortcuts import reverse,redirect, get_object_or_404
import os
from django.core.files import File
from home.models import Document, Group, GroupComment, DocumentComment, Log
from home.forms import DocumentForm, GroupRegistrationForm, GroupCommentForm, DocumentCommentForm

#home page:
def home(request):
    user=request.user
    users=User.objects.all()
    document = Document.objects.all()
    log = Log.objects.all()
    context = {'user': user, 'document': document, 'log': log, 'users': users}

    return render(
        request, 'home/templates/home.html', context

    )


#Group:
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
            for l in instance.isLeader.all():
                if l==request.user:
                    thief = False
    if request.user.is_superuser:
        thief=False
    if thief:
        raise Http404

    form= GroupRegistrationForm(request.POST or None,instance=instance)
    if form.is_valid():
        instance=form.save(commit=False)
        instance.modifier = request.user.id
        instance.save()
        print(instance.get_absolute_url())
        return redirect(instance.get_absolute_url())

    user = request.user
    return render(request, 'home/templates/home_groups_edit.html', {'form': form, 'user': user})

def group_detail(request,id=None):
    instance=get_object_or_404(Group,id=id)
    thief = True
    if request.user.is_superuser:
        thief=False
    for u in instance.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    comment=GroupComment.objects.all()
    group=instance
    context = {'group':group,'comment':comment}
    return render(
        request, 'home/templates/home_groups_specified.html', context)
def group_delete(request,id=None):
    instance=get_object_or_404(Group,id=id)
    thief = True
    if request.user.is_superuser:
        thief=False
    for u in instance.members.all():
        if u == request.user:
            for l in instance.isLeader.all():
                if l == request.user:
                    thief = False
    if thief:
        raise Http404
    instance.modifier = request.user.id
    instance.delete()
    return redirect('home:group_list')

def group_register(request):
    if request.method == 'POST':
        form = GroupRegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save()
            instance.creator = request.user.id
            instance.modifier = request.user.id
            instance.save()
            return HttpResponseRedirect(reverse('home:group_list'))
    else:
        form = GroupRegistrationForm()
    user = request.user
    return render(request, 'home/templates/home_groups_create.html', {'form': form,'user':user})
def index(request):
    return render('myapp/index.html')



#Group files:

def group_detail_files(request,id=None):
    group=get_object_or_404(Group, id=id)
    thief=True
    if request.user.is_superuser:
        thief=False
    for u in group.members.all():
        if u==request.user:
            thief=False
    if thief:
        raise Http404
    comment=DocumentComment.objects.all()
    document=Document.objects.all()
    context = {'group':group,'document':document,'comment':comment}
    return render(
        request, 'home/templates/home_groups_specified_files.html', context
    )

def group_detail_files_download(request,id=None,idf=None):
    group=get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief=False
    for u in group.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    # Handle file upload
    doc = get_object_or_404(Document, id=idf)
    path= doc.docfile.path
    if os.path.isfile(path):
        f=open(path,'rb')
        file=File(f)
        name=doc.filename()
        response = HttpResponse(file, content_type = 'application')
        response['Content-Disposition'] = 'attachment; filename={}'.format(name)
        return response

def group_detail_files_upload(request,id=None):
    # Handle file upload
    group = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief=False
    for u in group.members.all():
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

def group_detail_files_delete(request,id=None,idf=None):
    instanceF = get_object_or_404(Document, id=idf)
    instanceG = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief=False
    for u in instanceG.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    instanceF.modifier = request.user.id
    instanceF.delete()
    return redirect(instanceG.get_absolute_urlf())

#Comments:
def group_detail_comment(request,id=None):
    # Handle file upload
    group = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief=False
    for u in group.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404

    if request.method == 'POST':
        form = GroupCommentForm(request.POST)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.group=group
            instance.save()
            return redirect(group.get_absolute_url())
    else:
        form = GroupCommentForm()

    user=request.user
    context = {'form':form,'user':user,'id':id}
    # Render list page with the documents and the form
    return render( request,'home/templates/home_groups_specified_comment_add.html',context )
def group_detail_files_comment(request,id=None,idf=None):
    # Handle file upload
    group = get_object_or_404(Group, id=id)
    document=get_object_or_404(Document,id=idf)
    thief = True
    if request.user.is_superuser:
        thief=False
    for u in group.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    if request.method == 'POST':
        form = DocumentCommentForm(request.POST)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.document = document
            instance.document.modifier = request.user.id
            instance.save()
            return redirect(instance.get_absolute_url())
    else:
        form = DocumentCommentForm()

    user=request.user
    context = {'form':form,'user':user,'id':id}
    # Render list page with the documents and the form
    return render( request,'home/templates/home_groups_specified_files_comment_add.html',context )

def group_detail_comment_delete(request,id=None,idc=None):
    instanceC=get_object_or_404(GroupComment,id=idc)
    instance=get_object_or_404(Group,id=id)
    thief = True
    if request.user.is_superuser:
        thief=False
    for u in instance.members.all():
        if u == request.user:
            thief=False
    if thief:
        raise Http404
    instanceC.group.modifier = request.user.id
    instanceC.delete()

    return redirect(instance.get_absolute_url())

def group_detail_files_comment_delete(request,id=None,idf=None,idc=None):
    instanceC=get_object_or_404(DocumentComment,id=idc)
    instanceF = get_object_or_404(Document, id=idf)
    instanceG = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief=False
    for u in instanceG.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    instanceC.document.modifier = request.user.id
    instanceC.delete()
    return redirect(instanceF.get_absolute_url())

def log_clear(self):
    log= Log.objects.all()
    for l in log:
        l.delete()

    return redirect('home:home')

