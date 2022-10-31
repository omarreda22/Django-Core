from django.urls import path
from .views import ( 
	post_model_list_view,
	retrieve_view,
	create_blog,
	edit_blog,
	delete_blog,
	delete_quickly,
	)

app_name = 'blog'

urlpatterns = [
	path('', post_model_list_view, name="post_model_list_view"),
	path('retrieve/<str:name>/', retrieve_view, name="retrieve_view"),
	path('create/', create_blog, name="create_blog"),
	path('<str:name>/edit/', edit_blog, name="edit_blog"),
	path('<str:name>/delete/', delete_blog, name="delete_blog"),
	path('<str:name>/delete_quickly', delete_quickly, name="delete_quickly"),
]