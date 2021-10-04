from typing import Text
from django.core import exceptions
from django.core.checks import messages
from django.forms.forms import Form
from django.http import request
from django.shortcuts import redirect, render
from youtubesearchpython.search import Search
from .forms import *
from django.contrib import messages
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
# from django.views import generic

# Create your views here.
def home(request):
    return render(request,"dashboard/home.html")

@login_required
def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
            notes = Notes(user=request.user, title=request
                          .POST['title'], description = request.POST['description'])
            notes.save()
        messages.success(request, f"Note successfully added by { request.user.username }")
    else:
        form = NotesForm()
    notes = Notes.objects.filter(user=request.user)
    context = {"notes": notes, "form": form}
    return render(request,"dashboard/notes.html", context)

@login_required
def delete_note(request, pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")

@login_required
def NotesDetailView(request, pk=None):
    note = Notes.objects.get(id=pk)
    context = {"note": note}
    return render(request, "dashboard/notes_detail.html", context)

@login_required
def homework(request):
    if request.method == "POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finsihed = request.POST['is_finished']
                if finsihed == 'on':
                    finsihed = True
                else:
                    finsihed = False
            except:
                finsihed = False
                print("ERROR!!!!!....................")
            homework = Homework.objects.create(user=request.user, subject=request.POST['subject'], 
                                               title=request.POST['title'], description=request.POST['description'],
                                               due=request.POST['due'], is_finished=finsihed)
            homework.save()
            messages.success(request, f'Successfully added homework by {request.user.username}')
    form = HomeworkForm()
    homeworks = Homework.objects.filter(user=request.user)
    if len(homeworks) >= 1:
        no_homework = False
    else:
        no_homework = True
    if len(homeworks.filter(is_finished=False)) > 0:
        homework_done = False
    else:
        homework_done = True
    
    context = {"homeworks": homeworks, 
               "no_homework":no_homework, 
               "homework_done":homework_done,
               "form": form
               }
    return render(request, "dashboard/homework.html", context)

@login_required
def homework_is_finished(request, pk=None):
    homework = Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect("homework")

@login_required
def delete_homework(request, pk=None):    
    Homework.objects.get(id=pk).delete()
    return redirect("homework")

def youtube(request):
    if request.method == "POST":
        form = DashBoardForm(request.POST)
        text = request.POST['text']
        video = VideosSearch(text, limit=15)
        result_list = []
        for result in video.result()['result']:
            result_dict = {
                'input': text,
                'title': result['title'],
                'duration': result['duration'],
                'thumbnail': result['thumbnails'][0]['url'],
                'channel': result['channel']['name'],
                'link': result['link'],
                'views': result['viewCount'],
                'published': result['publishedTime']
            }
            desc = ''
            if result['descriptionSnippet']:
                for sentence in result['descriptionSnippet']:
                    desc += sentence['text']
            result_dict['description'] = desc
            result_list.append(result_dict)
        context = {
            'form': form,
            'results': result_list
        }
        return render(request, 'dashboard/youtube.html', context)
    form = DashBoardForm()
    context = {"form": form}
    return render(request, 'dashboard/youtube.html', context)

@login_required
def todo(request):
    form = TodoForm()
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            try:
                is_finished = request.POST['is_finished']
                if is_finished == 'on':
                    is_finished = True
                else:
                    is_finished = False
            except:
                is_finished = False
            todo = Todo.objects.create(user=request.user, title=request.POST['title'], is_finished=is_finished)
            todo.save()
            messages.success(request, f'Todo sucessfully created by {request.user.username} ')
    todos = Todo.objects.all()
    context = {'form': form, 'todos': todos}
    return render(request, "dashboard/todo.html", context)

@login_required
def toggle_todo_check(request, pk=None):
    todo = Todo.objects.get(id=pk)
    if todo.is_finished:
        todo.is_finished = False
    else:
        todo.is_finished = True
        
    todo.save()
    return redirect('/todo')

@login_required
def delete_todo(request, pk=None):
    Todo.objects.get(id=pk).delete()
    return redirect('/todo')

def book(request):
    if request.method == "POST":
        form = DashBoardForm(request.POST)
        text = request.POST['text']
        url = 'https://www.googleapis.com/books/v1/volumes?q=' + text
        r = requests.get(url)
        answer = r.json()
        result_list = []
        for i in range(10):            
            result_dict = {
                'title': answer['items'][i]['volumeInfo']['title'],
                'subtitle': answer['items'][i]['volumeInfo'].get('subtitle'),
                'description': answer['items'][i]['volumeInfo'].get('description'),
                'count': answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories': answer['items'][i]['volumeInfo'].get('categories'),
                'rating': answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail': answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview': answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
        context = {
            'form': form,
            'results': result_list
        }
        return render(request, 'dashboard/books.html', context)
    form = DashBoardForm()
    context = {"form": form}
    return render(request, 'dashboard/books.html', context)

def dictionary(request):
    if request.method == "POST":
        form = DashBoardForm(request.POST)
        text = request.POST['text']
        url = 'https://api.dictionaryapi.dev/api/v2/entries/en_US/' + text
        r = requests.get(url)
        answer = r.json()
        print(answer)
        try:
            phonetics = answer[0]["phonetics"][0]["text"]
            audio = answer[0]["phonetics"][0]["audio"]
            definition = answer[0]["meanings"][0]["definitions"][0]["definition"]
            example = answer[0]["meanings"][0]["definitions"][0]["example"]
            synonyms = answer[0]["meanings"][0]["definitions"][0]["synonyms"]
            context = {
                "form": form,
                "input": text,
                "phonetics": phonetics,
                "audio": audio,
                "definition": definition,
                "example": example,
                "synonyms": synonyms
            }
        except:
            print("---------------------")
            context = {
                "form": form
            }
        return render(request, "dashboard/dictionary.html" , context)
    else: 
        form = DashBoardForm()
        context = {"form": form}
        return render(request, "dashboard/dictionary.html" , context)
    
def wiki(request):
    if request.method == "POST":
        input = request.POST['text']
        form = DashBoardForm(request.POST)
        search = wikipedia.page(input)
        context = {
            "form": form,
            "title": search.title,
            "link": search.url,
            "details": search.summary
        }
        return render(request, "dashboard/wiki.html", context )
    else:
        form = DashBoardForm()
        context = {
            "form": form
        }
        return render(request, "dashboard/wiki.html", context )
    
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f'Accounnt created for {username}')
            return redirect("login")
    else:
        form = UserRegistrationForm()
    context = {
        "form": form
    }
    return render(request, "dashboard/register.html", context )

@login_required
def profile(request):
    homework = Homework.objects.filter(is_finished=False, user=request.user)
    todos = Todo.objects.filter(is_finished=False, user=request.user)
    if len(homework) == 0:
        homework_done = True
    else:
        homework_done = False
    if len(todos) == 0:
        todos_done = True
    else:
        todos_done = False
        
    context = {
        "homework": homework,
        "todos": todos,
        "homework_done": homework_done,
        "todos_done": todos_done
    }
    return render(request, "dashboard/profile.html", context )
