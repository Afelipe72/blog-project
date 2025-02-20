from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

# if a request reaches january then execute views.index
urlpatterns = [
    # path("", views.index, name="index"),
    # path("<int:post_id>", views.post, name="individual_post"),
    # instructor
    path("", views.starting_page.as_view(), name="starting_page"),
    path("posts", views.AllPostsView.as_view(), name="posts-page"),
    path("posts/<slug:slug>", views.post_detail.as_view(), name="post-detail-page"),
    path("read-later", views.read_later.as_view(), name="read-later"),
    # path("<int:month>", views.monthly_challenge_by_number),
    # path("<str:post_title>", views.post, name="post") # name its the identifier (name urls)
    # path("<str:month>", views.monthly_challenge, name="month-challenge")
    
    # settings.MEDIA_URL: Defines where the files should be reachable, settings.MEDIA_ROOT: where the files are stored
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)