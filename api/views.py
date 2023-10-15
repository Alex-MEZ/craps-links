from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Token, UserSavedLinks
from .forms import URLForm
from .serializers import TokenSerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


@login_required
def shorten_url(request):
    short_code = ""
    user_data, _ = UserSavedLinks.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            serializer = TokenSerializer(data={'full_url': form.cleaned_data['original_url']})
            if serializer.is_valid():
                token, status_code = serializer.save()
                short_code = token.short_url
                
                # Get the current list of string pairs, append the new tuple, and save
                current_links = user_data.get_link_pairs()
                short_url = "%s://%s/%s" % (request.scheme, request.get_host(), short_code)
                current_links.append((form.cleaned_data['original_url'], short_url))
                user_data.set_link_pairs(current_links)
                user_data.save()
    else:
        form = URLForm()

    link_pairs = user_data.get_link_pairs()
    return render(request, 'shorten_form.html', {'link_pairs': link_pairs, 'form': form, 'short_code': short_code})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Новый код
# from django.shortcuts import render
# from django.http import HttpResponse
# from .forms import URLForm
# from .serializers import TokenSerializer
#
# def shorten_url(request):
#     short_code = ""
#
#     if request.method == "POST":
#         form = URLForm(request.POST)
#         if form.is_valid():
#             # Валидируем и сохраняем данные через сериализатор
#             serializer = TokenSerializer(data={'full_url': form.cleaned_data['original_url']})
#             if serializer.is_valid():
#                 token, status_code = serializer.save()
#                 short_code = token.short_url
#             else:
#                 # В случае невалидных данных, обработайте ошибку
#                 return HttpResponse("Ошибка валидации данных", status=400)
#         else:
#             # В случае невалидной формы, обработайте ошибку
#             return HttpResponse("Невалидная форма", status=400)
#     else:
#         form = URLForm()
#
#     return render(request, 'shorten_form.html', {'form': form, 'short_code': short_code})

def redirect_original(request, short_url):
    try:
        token = Token.objects.get(short_url=short_url, is_active=True)
        token.requests_count += 1
        token.save()
        return redirect(token.full_url)
    except Token.DoesNotExist:
        return HttpResponse("Сокращенная URL не найдена!")