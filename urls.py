from django.urls import path
from . import views

urlpatterns=[
	path('',views.home, name='home'),
	path('start', views.start, name="start"),
	path('command', views.command, name="command"),
	path('recalculate', views.recalculate, name="recalculate"),
	path('summary_recalculate', views.summary_recalculate, name="summary_recalculate"),
	path('login_view', views.login_view, name="login_view"),
	path('command_json', views.command_json, name="command_json"),
	path('recalculate_previous', views.recalculate_previous, name="recalculate_previous"),
	path('summary', views.summary, name="summary"),
	path('logout_view', views.logout_view, name="logout_view"),
	path('home3', views.home3, name="home3"),
	path('gotocreatejsonmodule', views.gotocreatejsonmodule, name="gotocreatejsonmodule"),
	path('createjsonmodule_esdal', views.createjsonmodule_esdal, name="createjsonmodule_esdal"),
	path('createjsonmodule_email', views.createjsonmodule_email, name="createjsonmodule_email"),

]

# Create your views here.
