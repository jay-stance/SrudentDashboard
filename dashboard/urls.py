from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("notes", views.notes, name="notes"),
    path("delete_note/<int:pk>", views.delete_note , name="delete-note"),
    path("note_detail/<int:pk>", views.NotesDetailView , name="note-detail"),
    
    path("homework", views.homework, name="homework"),
    path("homework_is_finished/<int:pk>", views.homework_is_finished, name="homework-is-finished"),
    path("delete_homework/<int:pk>", views.delete_homework, name="delete-homework"),
    
    path("youtube", views.youtube, name="youtube"),
    
    path("todo", views.todo, name="todo"),
    path("toggle_todo_check/<int:pk>", views.toggle_todo_check, name="toggle_todo_check"),
    path("delete_todo/<int:pk>", views.delete_todo, name="delete_todo"),
    
    path("book", views.book, name="book"),
    
    path("dictionary", views.dictionary, name="dictionary"),
 
    path("wiki", views.wiki, name="wiki")    
]