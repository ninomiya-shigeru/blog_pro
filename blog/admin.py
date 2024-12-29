from django.contrib import admin
# modelsからBlogPostクラスをインポート
from .models import Message

# Django管理サイトにBlogPostを登録する
admin.site.register(Message)