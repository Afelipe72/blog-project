from django.contrib import admin

from .models import Post, Author, Tag, Comment

class PostAdmin(admin.ModelAdmin):
    list_filter = ("author", "tags", "date")
    # values to display in the columns
    # values are the names in the model
    list_display = ("title", "date", "author")
    # prepopulate slug field
    prepopulated_fields = {"slug":("title",)}

# how the comments are displayed in the administration
class CommentAdmin(admin.ModelAdmin):
    list_display = ("user_name", "post")

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
# Register the admins too 
admin.site.register(Comment, CommentAdmin)