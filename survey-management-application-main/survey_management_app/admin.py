from django.contrib import admin
from .models import User, Surveys, Accessable, Answer

admin.site.register(User)
admin.site.register(Surveys)
admin.site.register(Accessable)
admin.site.register(Answer)