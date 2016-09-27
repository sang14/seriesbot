from django.conf.urls import patterns, include, url
from django.contrib import admin
from chatbot101.views import MyChatBotView,index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'anotherbot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',index),
    url(r'^facebook_auth/?$',MyChatBotView.as_view()),
)
