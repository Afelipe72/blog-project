from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    # metainformation about the modelform
    class Meta:
        model = Comment
        # fields to exclude from the model
        # Exclude the "post" field to prevent users from manually assigning a comment to any post.  
        # This ensures the comment is always linked to the correct post in the view, preventing security risks.  
        exclude = ["post"]
        labels = {
            "user_name" : "Your name",
            "user_email" : "Your e-mail",
            "text" : "Your comment",
        }