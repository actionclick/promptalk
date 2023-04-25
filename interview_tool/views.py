from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from wordbank_manager.models import StandardPrompt, PromptCategory, UserPrompt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.db.models import Q

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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

def start_interview(request):
    return render(request, 'interview/start.html')

@login_required
def searchPrompt(request):
    if request.method == 'POST':
        transcript = request.POST.get('transcript')

        # remove unimportant words
        relevant_words = remove_stop_words(transcript)
        print(relevant_words)
        words = relevant_words.split()

        # Search for a prompt in the database using the cleaned transcript.
        try:
            prompt = StandardPrompt.objects.filter(hashtags__icontains=transcript).first()
            if prompt:
                response = prompt.text
            else:
                response = ""
        except StandardPrompt.DoesNotExist:
            response = ""
        return JsonResponse({'response': response})
    else:
        return JsonResponse({'error': 'Invalid request method.'})


@login_required
def home_view(request):
    if request.method == 'POST':
        final_transcript = request.POST.get('final_transcript', '')
        matching_prompts = process_speech(final_transcript)
        return render(request, 'home.html', {'matching_prompts': matching_prompts})

    return render(request, 'home.html')

def remove_stop_words(text):
    # Download the stop words corpus
    nltk.download('stopwords')

    # Define the list of stop words to be removed
    stop_words = set(stopwords.words('english'))
    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove the stop words from the text
    filtered_words = [word for word in words if word.lower() not in stop_words]

    # Join the remaining words back into a string
    filtered_text = ' '.join(filtered_words)

    return filtered_text