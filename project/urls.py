from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

# from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('sign', views.sign, name='sign'),
    path('submit', views.submit, name='submit'),
    path('log', views.log, name='log'),
    path('logout', views.logout, name='logout'),
    path('adm', views.adm, name='adm'),
    path('abt', views.abt, name='abt'),
    path('order/<int:id>', views.order, name='order'),
    path('pro', views.pro, name='pro'),
    path('index', views.index, name='index'),
    path('dash', views.dash, name='dash'),
    path('add', views.add, name='add'),
    path('view', views.view, name='view'),
    path('delete1/<int:id>', views.delete_product, name='delete1'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('mng/<int:id>/', views.mng, name='mng'),
    path('cart/<int:id>', views.cart, name='cart'),
    path('bag', views.bag, name='bag'),
    path('placeorder', views.placeorder, name='placeorder'),
    path('page', views.page, name='page'),
    path('wish/<int:id>', views.wish, name='wish'),
    path('showwishlist', views.showwish, name='showwishlist'),
    path('delete/<int:id>', views.delete_cart_item, name='delete'),
    path('delete2/<int:id>', views.delete2, name='delete2'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
