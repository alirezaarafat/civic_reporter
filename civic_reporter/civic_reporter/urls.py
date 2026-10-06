from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # App1_accounts -> registration, login, token refresh, current-user
    path("api/auth/", include("accounts.urls")),

    # App2_reports -> Area / Category (Report endpoints added later)
    path("api/reports/", include("reports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
