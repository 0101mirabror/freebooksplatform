
"""DJANGO"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

"""DJANGO REST FRAMEWORK IMPORTS"""
 
from rest_framework import routers
from bookhiveapp.apiviews import BookModelViewSet, BookModelDetailView, UserModelViewSet

'''
DJANGO REST FRAMEWORK:[begin]
'''
# books
router1 = routers.DefaultRouter()
router1.register(r'books', BookModelViewSet)
# users
router2 = routers.DefaultRouter()
router2.register(r'users', UserModelViewSet)
'''
DJANGO REST FRAMEWORK:[end]'''


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bookhiveapp.urls', namespace='books')),
    path('account/', include('accounts.urls', namespace='account')),
    path('accounts/', include('allauth.urls')),
    # djangorestframework url routes
    path('api/', include(router1.urls)),
    path('api-users/', include(router2.urls)),
    path('api/books/detail/<int:pk>/', BookModelDetailView.as_view(), name='book-detail'),
    path('api-auth/', include('rest_framework.urls'))

]



urlpatterns += [
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += [
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)