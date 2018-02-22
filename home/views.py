from django.shortcuts import render
from django.http import Http404, StreamingHttpResponse, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.models import User

from django.shortcuts import reverse, redirect, get_object_or_404
import os, hashlib
from django.core.files import File
from home.models import Document, Group, GroupComment, DocumentComment, Log
from home.forms import DocumentForm, GroupRegistrationForm, GroupCommentForm, DocumentCommentForm


# home page:
def home(request):
    user = request.user
    users = User.objects.all()
    document = Document.objects.all()
    log = Log.objects.all()
    log = reversed(log)
    group = Group.objects.all()

    context = {'user': user, 'document': document, 'log': log, 'users': users, 'group': group}

    return render(
        request, 'home/templates/home.html', context

    )


# My Files page
def ownfiles(request):
    user = request.user
    document = Document.objects.all()
    group = Group.objects.all()

    context = {'user': user, 'document': document, 'group': group}
    return render(
        request, 'home/templates/home_ownfiles.html', context

    )


# reports pages
def reports(request):
    user = request.user
    if not user.is_superuser:
        raise Http404

    log = Log.objects.all()
    log = reversed(log)
    users = User.objects.all()
    context = {'user': user, 'log': log, 'users': users}
    return render(
        request, 'home/templates/home_reports.html', context
    )


def reports_specified(request, id=None):
    user = request.user
    if not user.is_superuser:
        raise Http404
    users = User.objects.all()
    log = Log.objects.all()
    log = reversed(log)
    cuser = get_object_or_404(User, id=id)
    context = {'user': user, 'log': log, 'users': users, 'cuser': cuser}

    return render(
        request, 'home/templates/home_reports_specified.html', context
    )


# Group:
def group_list(request):
    groups = Group.objects.all()

    user = request.user
    context = {'groups': groups, 'user': user}
    return render(
        request, 'home/templates/home_groups.html', context
    )


def group_edit(request, id=None):
    instance = get_object_or_404(Group, id=id)

    thief = True
    for u in instance.members.all():
        if u == request.user:
            for l in instance.isLeader.all():
                if l == request.user:
                    thief = False
    if request.user.is_superuser:
        thief = False
    if thief:
        raise Http404

    form = GroupRegistrationForm(request.POST or None, instance=instance)
    if form.is_valid():
        instance = form.save()
        instance.modifier = request.user.id
        instance.save()
        instance = get_object_or_404(Group, id=id)
        for gc in GroupComment.objects.all():
            if gc.group == instance:
                print("group found")
                for uc in gc.hasRead.all():
                    print("users found")
                    if uc not in instance.members.all():
                        gc.hasRead.remove(uc)
                        print("user removed")
                        gc.save()
        for dc in DocumentComment.objects.all():
            if dc.document.group == instance:
                for uc in dc.hasRead.all():
                    if uc not in instance.members.all():
                        print("user removed")
                        dc.hasRead.remove(uc)
                        dc.save()
        return redirect('home:group_list')

    user = request.user
    return render(request, 'home/templates/home_groups_edit.html', {'form': form, 'user': user})


def group_detail(request, id=None):
    instance = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief = False
    for u in instance.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    for gc in GroupComment.objects.all():
        if gc.group == instance:
            gc.hasRead.add(request.user)
            gc.save()
    comment = GroupComment.objects.all()
    comment = reversed(comment)
    group = instance
    context = {'group': group, 'comment': comment}
    return render(
        request, 'home/templates/home_groups_specified.html', context)


def group_delete(request, id=None):
    instance = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief = False
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
            if not (request.user in instance.members.all()):
                instance.members.add(request.user)
            if not (request.user in instance.isLeader.all()):
                instance.members.add(request.user)
            instance.creator = request.user.id
            instance.modifier = request.user.id
            instance.save()
            return HttpResponseRedirect(reverse('home:group_list'))
    else:
        form = GroupRegistrationForm()
    user = request.user
    return render(request, 'home/templates/home_groups_create.html', {'form': form, 'user': user})


# Group files:

def group_detail_files(request, id=None):
    group = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief = False
    for u in group.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    for dc in DocumentComment.objects.all():
        if dc.document.group == group:
            dc.hasRead.add(request.user)
            dc.save()
    comment = DocumentComment.objects.all()
    comment = reversed(comment)
    document = Document.objects.all()

    context = {'group': group, 'document': document, 'comment': comment}
    return render(
        request, 'home/templates/home_groups_specified_files.html', context
    )


def group_detail_files_download(request, id=None, idf=None):
    group = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief = False
    for u in group.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    # Handle file upload
    doc = get_object_or_404(Document, id=idf)
    path = doc.docfile.path
    print(path)
    if os.path.isfile(path):
        f = open(path, 'rb')
        file = File(f)
        name = doc.filename()
        response = HttpResponse(file, content_type='application')
        response['Content-Disposition'] = 'attachment; filename={}'.format(name)
        return response


def group_detail_files_upload(request, id=None):
    # Handle file upload
    group = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief = False
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
            instance = form.save(commit=False)
            instance.modifier = request.user.id
            instance.creator = request.user.id
            instance.group = group
            instance.save()
            path = instance.docfile.path
            if os.path.isfile(path):
                hasher = hashlib.md5()
                f = open(path, 'rb')
                buf = f.read()
                hasher.update(buf)
                instance.filehash = hasher.hexdigest()
                instance.save()
                for d in Document.objects.all():
                    if d.group == group:
                        if instance.filehash == d.filehash and instance.id != d.id:
                            instance.delete
                            return redirect('home:prompt_duplicate')

            return redirect(instance.get_absolute_url())
    else:
        form = DocumentForm()

    user = request.user
    context = {'form': form, 'user': user, 'id': id}
    # Render list page with the documents and the form
    return render(request, 'home/templates/home_groups_specified_files_upload.html', context)


def group_detail_files_delete(request, id=None, idf=None):
    instanceF = get_object_or_404(Document, id=idf)
    instanceG = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief = False
    for u in instanceG.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    instanceF.modifier = request.user.id
    instanceF.delete()
    return redirect(instanceG.get_absolute_urlf())


# Comments:
def group_detail_comment(request, id=None):
    # Handle file upload
    group = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief = False
    for u in group.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404

    if request.method == 'POST':
        form = GroupCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.group = group
            instance.creator = request.user.username
            instance.save()
            return redirect(group.get_absolute_url())
    else:
        form = GroupCommentForm()

    user = request.user
    context = {'form': form, 'user': user, 'id': id}
    # Render list page with the documents and the form
    return render(request, 'home/templates/home_groups_specified_comment_add.html', context)


def group_detail_files_comment(request, id=None, idf=None):
    # Handle file upload
    group = get_object_or_404(Group, id=id)
    document = get_object_or_404(Document, id=idf)
    thief = True
    if request.user.is_superuser:
        thief = False
    for u in group.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    if request.method == 'POST':
        form = DocumentCommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.document = document
            instance.creator = request.user.username
            instance.document.modifier = request.user.id
            instance.save()
            return redirect(instance.get_absolute_url())
    else:
        form = DocumentCommentForm()

    user = request.user
    context = {'form': form, 'user': user, 'id': id}
    # Render list page with the documents and the form
    return render(request, 'home/templates/home_groups_specified_files_comment_add.html', context)


def group_detail_comment_delete(request, id=None, idc=None):
    instanceC = get_object_or_404(GroupComment, id=idc)
    instance = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief = False
    for u in instance.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    instanceC.group.modifier = request.user.id
    instanceC.delete()

    return redirect(instance.get_absolute_url())


def group_detail_files_comment_delete(request, id=None, idf=None, idc=None):
    instanceC = get_object_or_404(DocumentComment, id=idc)
    instanceF = get_object_or_404(Document, id=idf)
    instanceG = get_object_or_404(Group, id=id)
    thief = True
    if request.user.is_superuser:
        thief = False
    for u in instanceG.members.all():
        if u == request.user:
            thief = False
    if thief:
        raise Http404
    instanceC.document.modifier = request.user.id
    instanceC.delete()
    return redirect(instanceF.get_absolute_url())


# Log
def reports_clear(request):
    user = request.user
    if not user.is_superuser:
        raise Http404

    log = Log.objects.all()
    for l in log:
        l.delete()
    return redirect('home:reports')


def reports_specified_clear(request, id=None):
    user = request.user
    cuser = get_object_or_404(User, id=id)
    if not user.is_superuser:
        raise Http404
    log = Log.objects.all()
    for l in log:
        if l.user == cuser:
            l.delete()
    return redirect('home:reports')


# Duplicate Files
def prompt_duplicate(request):
    return render(request, 'home/templates/home_prompt_duplicate.html')
