from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from .forms import * 
from .models import *
from django.http import JsonResponse


# Create your views here.
def set_data_entry(request):
    form = AddressForm()
    context = {
        'form': form,
    }
    return render(request, 'data_entry/input_data.html', context)


def set_pengguna(request):
    list_pengguna = Pengguna.objects.all()
    context = None
    form = PenggunaForm(None)
    email_p = None

    if request.method == "POST":
        form = PenggunaForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.session['email'] = email
            request.session.modified = True
            form.save()
            list_pengguna = Pengguna.objects.all()
            email_p = request.session['email']
            context = {
                'form': form,
                'list_pengguna': list_pengguna,
                'email_p': email_p,
            }
            return render(request, 'data_entry/input_data_1.html', context)
    else:
        context = {
            'form': form,
            'list_pengguna': list_pengguna,
        }
        return render(request, 'data_entry/input_data_1.html', context)


def view_pengguna(request, id):
    try:
        pengguna = Pengguna.objects.get(pk=id)
        return render(request, 'data_entry/pengguna_detail.html', {'user_id': pengguna.id})
    except Pengguna.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
def update_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, id=id)
    form = PenggunaForm(instance=pengguna)
    
    if request.method == 'POST':
        form = PenggunaForm(request.POST, request.FILES, instance=pengguna)
        if form.is_valid():
            form.save()
            return redirect('data_entry:set_pengguna')
    context = {
        'form': form,
        'pengguna': pengguna
    }
    return render(request, 'data_entry/pengguna_update.html', context)

def delete_pengguna(request, id):
    pengguna = get_object_or_404(Pengguna, id=id)
    if request.method == 'POST':
        pengguna.delete()
        return redirect('data_entry:set_pengguna')
    return render(request, 'data_entry/pengguna_delete.html', {'pengguna': pengguna})

def get_pengguna_detail_api(request, user_id):
    try:
        pengguna = Pengguna.objects.get(pk=user_id)
        data = {
            'email': pengguna.email,
            'address_1': pengguna.address_1,
            'address_2': pengguna.address_2,
            'city': pengguna.city,
            'state': pengguna.state,
            'zip_code': pengguna.zip_code,
            'tanggal_join': pengguna.tanggal_join.strftime('%Y-%m-%d'),
            'foto': pengguna.foto.url if pengguna.foto else None
        }
        return JsonResponse(data)
    except Pengguna.DoesNotExist:
        return JsonResponse({'error': 'User not found'},status=404)
    
def set_content(request):
    context = {}
    email = request.session.get('email')
    pengguna = None
    isi_tabel = None

    if request.method == 'POST':
        if 'selected_author' in request.POST:
            # Handle author selection
            selected_email = request.POST.get('selected_author')
            request.session['email'] = selected_email
            return redirect('data_entry:set_content')
        else:
            # Handle content creation
            email = request.session.get('email')
            if email:
                try:
                    pengguna = Pengguna.objects.get(email=email)
                    form = ContentForm(request.POST, request.FILES)
                    if form.is_valid():
                        content = form.save(commit=False)
                        content.author = pengguna
                        content.save()
                        return redirect('data_entry:set_content')
                except Pengguna.DoesNotExist:
                    pass

    # For GET requests or invalid forms
    email = request.session.get('email')
    if email:
        try:
            pengguna = Pengguna.objects.get(email=email)
            isi_tabel = Content.objects.filter(author=pengguna)
        except Pengguna.DoesNotExist:
            pass

    form = ContentForm()
    context = {
        'form': form,
        'email': email,
        'pengguna': pengguna,
        'isi_tabel': isi_tabel,
        'list_pengguna': Pengguna.objects.all(),
    }
    return render(request, 'data_entry/create_content.html', context)

