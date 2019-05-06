from django.contrib import admin
from django.urls import path, include

from blog import views as blog_views
from .views import redirect_blog


urlpatterns = [

    path('', redirect_blog, name='redirect_blog_url'),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', blog_views.signup, name='signup'),
    path('account/account_activation_sent/', blog_views.account_activation_sent, name='account_activation_sent'),
    path('account/activate/<str:uidb64>/<str:token>/', blog_views.activate, name='activate'),


]
