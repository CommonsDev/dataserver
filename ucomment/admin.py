from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.core.urlresolvers import reverse
from django.template.defaultfilters import escape


from django_comments.models import CommentFlag, Comment
from django_comments.admin import CommentsAdmin


class CommentFlagAdmin(ModelAdmin):
    """
    Admin interface for comments flags
    """
    model = CommentFlag

    def comment_link(self, obj):
        return '<a href="%s">%s</a>' % (reverse("admin:django_comments_comment_change", args=(obj.comment.id,)), obj.comment.id)

    comment_link.allow_tags = True
    comment_link.short_description = "Comment"

    list_display = ('flag', 'user', 'comment', 'comment_link',)

admin.site.register(CommentFlag, CommentFlagAdmin)
