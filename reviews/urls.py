
from django.contrib import admin
from django.urls import path, include
import reviews.views


urlpatterns = [
    path('', reviews.views.index, name='view_reviews_route'),
    path('create/<book_id>', reviews.views.create_review, name='create_review_route'),
    path('details/<review_id>', reviews.views.view_review_details, name='view_review_details_route'),
    path('comment/create/<review_id>', reviews.views.process_create_comment, name='process_create_comment_route')
]
