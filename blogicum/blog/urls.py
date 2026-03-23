from django.urls import path

from . import views

app_name = 'blog'
handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('category/<slug:category_slug>/', views.CategoryListView.as_view(),
         name='category_posts'),

    path('profile/edit/', views.UserUpdateView.as_view(),
         name='edit_profile'),
    path('profile/<str:username>/', views.ProfileListView.as_view(),
         name='profile'),

    path('posts/<int:pk>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('posts/create/', views.PostCreateView.as_view(), name='create_post'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(),
         name='delete_post'),

    path('posts/<int:pk>/comment/', views.add_comment,
         name='add_comment'),
    path('posts/<int:pk>/edit_comment/<int:comment_pk>/',
         views.CommentUpdateView.as_view(), name='edit_comment'),
    path('posts/<int:pk>/delete_comment/<int:comment_pk>/',
         views.CommentDeleteView.as_view(), name='delete_comment'),
]
