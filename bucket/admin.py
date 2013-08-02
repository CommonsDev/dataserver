from django.contrib import admin

from .models import Bucket, BucketFile, BucketFileComment

class InlineBucketFile(admin.TabularInline):
    model = BucketFile

class BucketFileCommentAdmin(admin.ModelAdmin):
    model = BucketFileComment

class BucketAdmin(admin.ModelAdmin):
    inlines = [
        InlineBucketFile,
    ]


admin.site.register(Bucket, BucketAdmin)
admin.site.register(BucketFileComment, BucketFileCommentAdmin)
