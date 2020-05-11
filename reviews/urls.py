
from django.contrib import admin
from django.urls import path, include
import reviews.views


urlpatterns = [
    path('', reviews.views.index, name='view_reviews_route'),
    path('create', reviews.views.create_review, name='create_review_route')
]
