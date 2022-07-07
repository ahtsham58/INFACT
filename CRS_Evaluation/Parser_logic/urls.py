from django.urls import path
from .views import ratings, error,home, question, feedback, confirmation, terms

urlpatterns = [path('', home),
               path('index.html',home),
               path('ratings.html', ratings),
               path('error.html', error),
               path('questionnaire.html',question),
               path('feedback.html',feedback),
               path('confirmation.html',feedback),
               path('terms.html',terms)
               ]
