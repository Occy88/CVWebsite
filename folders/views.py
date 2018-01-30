
from .models import Folder, Document
from django.shortcuts import render, get_object_or_404

def folders(request):
    all_folders=Folder.objects.all()
    return render(request, '/folders/templates/index.html', {
        'all_folders':all_folders,
    })

def detail(request,folder_id):
    folder= get_object_or_404(Folder, pk=folder_id)
    return render(request, 'folders/templates/detail.html', {
        'folder':folder,
    })
def favorite(request,folder_id):
    folder = get_object_or_404(Folder, pk=folder_id)
    try:
        selected_document= folder.document_set.get(pk=request.POST['document'])
    except(KeyError,Document.DoesNotExist):
        return render(request,'folders/templates/detail.html',{
            'folder':folder,
            'error_message':"you did not select a valid document",
        })
    else:
        selected_document.is_favorite=True
        selected_document.save()
        return render(request, 'folders/templates/detail.html', {'folder': folder,})


# Create your views here.
