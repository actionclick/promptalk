from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from wordbank_manager.models import StandardPrompt, PromptCategory, UserPrompt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.db.models import Q

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def prompt_list_view(request):
    user = request.user
    standard_prompts = StandardPrompt.objects.all()
    user_prompts = UserPrompt.objects.filter(user=user)
    prompt_categories = PromptCategory.objects.filter(user=user)
    context = {
        'standard_prompts': standard_prompts,
        'user_prompts': user_prompts,
        'prompt_categories': prompt_categories,
    }
    return render(request, 'prompt_list.html', context)


@login_required
def home_view(request):
    return render(request, 'home.html')

def start_interview(request):
    return render(request, 'interview/start.html')

def get_prompt_suggestion(request):
    spoken_text = request.GET.get('text')
    hashtags = spoken_text.split('#')[1:]
    if hashtags:
        query = Q(hashtags__icontains=hashtags[0])
        for hashtag in hashtags[1:]:
            query |= Q(hashtags__icontains=hashtag)
        prompt = StandardPrompt.objects.filter(query).first()
        if prompt:
            return JsonResponse(prompt.text, safe=False)
    return JsonResponse('', safe=False)
