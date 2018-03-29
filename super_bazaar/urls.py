from django.conf.urls import url
from django.contrib import admin
from maintain_records.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', sales, name="sales"),
    url(r'^purchase/$', purchase, name="purchase"),
    url(r'^register_new_dealer/$', register_new_dealer, name="register_new_dealer"),
    url(r'^sales/$', sales, name="sales"),
    url(r'^register_new_item/$', register_new_item, name="register_new_item"),
    url(r'^showstock/', show_stock, name="show_stock"),
    url(r'^declare_winner/', declare_the_winner, name="declare_the_winner"),
    url(r'^signin/$', LoginFormView.as_view(), name="signin"),
    url(r'^logout/', logout_user, name="logout_user"),
]
