from django.contrib import admin

# Register your models here.

from .models import Project, Issue, Comment, Contributors

admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
admin.site.register(Contributors)