from django.contrib import admin
# include()関数を使うためincludeを追加
from django.urls import path, include

# プロジェクトのURLパターンを登録するリスト
urlpatterns = [
    # http(s)://ホスト名/以下のパスがadmin/にマッチングした場合
    # admin.site.urlsを呼び出し、Django管理サイトを表示する
    path('admin/', admin.site.urls),

    # http(s)://ホスト名/へのアクセスはbbogappの
    # URLConf(urls.py)を呼び出す
    path('', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
]
