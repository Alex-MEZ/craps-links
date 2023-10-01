from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Token
from .forms import URLForm
from .serializers import TokenSerializer

def shorten_url(request):
    short_code = ""
    if request.method == "POST":
        form = URLForm(request.POST)
        if form.is_valid():
            serializer = TokenSerializer(data={'full_url': form.cleaned_data['original_url']})
            if serializer.is_valid():
                token, status_code = serializer.save()
                short_code = token.short_url
    else:
        form = URLForm()

    return render(request, 'shorten_form.html', {'form': form, 'short_code': short_code})


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