from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views
from django.conf.urls import handler404, handler500
from django.conf import settings
from django.conf.urls.static import static

handler404 = "posts.views.page_not_found"  # noqa
handler500 = "posts.views.server_error"  # noqa

urlpatterns = [
    # раздел администратора
    path("admin/", admin.site.urls, name='admin'),
    # flatpages
    path("about/", include("django.contrib.flatpages.urls")),
    # регистрация и авторизация
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    # импорт из приложения posts
    path("", include("posts.urls")),
]
# добавим новые пути
urlpatterns += [
    path('about-author/', views.flatpage, {'url': '/about-author/'}, name='about'),
    path('about-tech/', views.flatpage, {'url': '/about-tech/'}, name='abouttech'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)