from datetime import date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Post, Author, Tag
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .forms import CommentForm
from django.views import View

class starting_page(ListView):
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"
    template_name = "blog/index.html"
    def get_queryset(self):
        queryset = super().get_queryset()
        # get the last three posts
        data = queryset[:3]
        return data

# def starting_page(request):
#     # executes that date when it sorts that posts list
#     # compares all those dates to sort the overall array
#     # sorted_posts = sorted(all_posts, key=get_date)
#     # latest_posts = sorted_posts[-3:]

#     # order by the most recent dates and get the three latest posts
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {
#         "posts": latest_posts
#     })

class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    # its passed to the dtl as an object lists
    context_object_name = "all_posts"

# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request, "blog/all-posts.html", {
#         "all_posts": all_posts
#     } )

# we inherit only for view bc we need to handle the comment form submission (post) as well as the post detail (get)
class post_detail(View):

    def is_stored_post(self, request, post_id):
        # check if the post is already a stored post
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later

    model = Post
    template_name = 'blog/post-detail.html'
    # commentform is in the detail view bc its on that page, otherwise it would on a separate view
    # use the slug as a parameter bc the url uses the slug
    # get the detail view in the db
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)

        context = {
        "post": post,
        # all the related tags to this post
        "tags": post.tags.all(),
        "comment_form": CommentForm(),
        # order the comments from bottom to top (more recent)
        "comments": post.comments.all().order_by("-id"),
        "saved_for_later": self.is_stored_post(request, post.id),
        }

        return render(request, "blog/post-detail.html", context)
    
    # get the detail view in the db
    def post(self , request, slug):
        # submitted data from the commentForm
        comment_form = CommentForm(request.POST)
        # get specific post
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            # we can call the .save() bc its a model form
            # save it to the database
            # bc the post is excluded from the form, theres no way to link the comment to a specific post
            comment = comment_form.save(commit=False) # when we hit save it creates a new model instance (commit=False)
            # link the comment to the post (.post is the field from the comment model)
            comment.post = post
            comment.save()
            # reverse to create the url dynamically
            # url name
            # the slug used to reach this page
            # redirect to refresh the page
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        # if the form is invalid then we render the post detail as normal
        post = Post.objects.get(slug=slug)
        
        context = {
        "post": post,
        # all the related tags to this post
        "tags": post.tags.all(),
        "comment_form": CommentForm(),
        # order the comments from bottom to top (more recent)
        "comments": post.comments.all().order_by("-id"),
        "saved_for_later": self.is_stored_post(request, post.id),
        }


        return render(request, "blog/post-detail.html", context)
    
class read_later(View):
    # get the list of posts session
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        #if we dont have stored posts or we have a list with 0 items
        if stored_posts is None or len(stored_posts) == 0:
            # show some info in the read later page
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)
    

    def post(self, request):
        # retrieves the key under "stored_posts" so the list stored posts
        stored_posts = request.session.get("stored_posts")
        
        # create the list inside the session in the case that is empty
        if stored_posts is None:
            stored_posts = []

        # Get the Post ID from the Form Submission
        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
            # save the posts
            # This adds the post ID to the list
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")
