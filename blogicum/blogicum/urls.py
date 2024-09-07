from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler403 = "pages.views.handler403"
handler404 = "pages.views.handler404"
handler500 = "pages.views.handler500"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("django.contrib.auth.urls")),
    path("pages/", include("pages.urls", namespace="pages")),
    path("", include("authorization.urls", namespace="authorization")),
    path("", include("blog.urls", namespace="blog")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
