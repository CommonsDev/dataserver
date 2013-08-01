from django.contrib import admin

from .models import Bucket, BucketFile

class InlineBucketFile(admin.TabularInline):
    model = BucketFile

class BucketAdmin(admin.ModelAdmin):
    inlines = [
        InlineBucketFile,
    ]


admin.site.register(Bucket, BucketAdmin)
# admin.site.register(BucketFile, InlineBucketFile)
