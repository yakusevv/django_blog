from django.contrib import admin
from django.urls import path, include

from .views import redirect_blog


urlpatterns = [
    path('', redirect_blog, name='redirect_blog_url'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls'))

]
