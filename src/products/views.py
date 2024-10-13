import mimetypes
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, HttpResponseBadRequest
from .models import Product, ProductAttachment
from .forms import ProductFrom, ProductUpdateFrom, ProductAttachmentInlineFormSet


# Create your views here.
@login_required()
def product_create_view(request):
    context = {}
    form = ProductFrom(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        return redirect(obj.get_manage_url())
    context['form'] = form
    return render(request, 'products/create.html', context)

def produt_list_view(request):
    obj_qs = Product.objects.all()
    context = {"obj_list": obj_qs}
    return render(request, 'products/list.html', context)

def product_manage_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_manager = False
    if request.user.is_authenticated:
        is_manager = obj.user == request.user
    context = {"object": obj}
    if not is_manager:
        return HttpResponseBadRequest()
    
    if request.method == "POST" and "delete-product" in request.POST:
        obj.delete()
        return redirect(reverse('products:list'))
    
    form = ProductUpdateFrom(request.POST or None, request.FILES or None, instance=obj)
    formset = ProductAttachmentInlineFormSet(request.POST or None, request.FILES or None,queryset=attachments)
    if form.is_valid() and formset.is_valid():
        instance = form.save(commit=False)
        instance.save()
        formset.save(commit=False)
        for _form in formset:
            is_delete = _form.cleaned_data.get("DELETE")
            try:
                attachment_obj = _form.save(commit=False)
            except:
                attachment_obj = None
            if is_delete:
                if attachment_obj is not None:
                    if attachment_obj.pk:
                        attachment_obj.delete()
            else:
                if attachment_obj is not None:
                    attachment_obj.product  = instance
                    attachment_obj.save()
        formset.save()
        return redirect(obj.get_manage_url())
    context['form'] = form
    context['formset'] = formset
    return render(request, 'products/manage.html', context)

def product_detail_view(request, handle=None):
    obj = get_object_or_404(Product, handle=handle)
    attachments = ProductAttachment.objects.filter(product=obj)
    is_owner = False
    is_manager = False
    if request.user.is_authenticated:
        is_owner = request.user.purchase_set.all().filter(product=obj, completed=True).exists()
        is_manager = obj.user == request.user
    context = {"object":obj,"is_owner": is_owner,"is_manager":is_manager, "attachments": attachments}
    return render(request, 'products/detail.html', context)

def product_attachment_download_view(request, handle=None, pk=None):
    attachment = get_object_or_404(ProductAttachment, product__handle=handle, pk=pk)
    # attachment = ProductAttachment.objects.all().first()
    can_download = attachment.is_free or False
    if request.user.is_authenticated:
        can_download = True # check ownweship
    if can_download is False:
        return HttpResponseBadRequest()
    file = attachment.file.open(mode='rb') # cdn -> S3 object storage
    filename = attachment.file.name
    content_type, _ = mimetypes.guess_type(filename)
    response = FileResponse(file)
    response['Content-Type'] = content_type or 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename={filename}'
    return response
