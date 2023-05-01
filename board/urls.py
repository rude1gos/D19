from django.urls import path
# Импортируем созданное нами представление
from .views import PostList, PostDetail, PostCreate, PostUpdate, ReplyAdd

urlpatterns = [
   path('', PostList.as_view(), name='news_list'),
   path('<int:pk>', PostDetail.as_view(), name='news_detail'),
   path('create/', PostCreate.as_view(), name='news_create'),
   path('<int:pk>/update', PostUpdate.as_view(), name='news_update'),
   path('<int:pk>/reply/add', ReplyAdd.as_view(), name='reply_add'),
]