from django.urls import path
from . import views_Esdal

urlpatterns=[
	path('',views_Esdal.home, name='home'),
	path('start', views_Esdal.start, name="start"),
	path('command', views_Esdal.command, name="command"),
	path('recalculate', views_Esdal.recalculate, name="recalculate"),
	path('summary_recalculate', views_Esdal.summary_recalculate, name="summary_recalculate"),
	path('login_view', views_Esdal.login_view, name="login_view"),
	path('command_json', views_Esdal.command_json, name="command_json"),
	path('recalculate_previous', views_Esdal.recalculate_previous, name="recalculate_previous"),
	path('summary', views_Esdal.summary, name="summary"),
	path('logout_view', views_Esdal.logout_view, name="logout_view"),
	path('home3', views_Esdal.home3, name="home3"),
	path('gotocreatejsonmodule', views_Esdal.gotocreatejsonmodule, name="gotocreatejsonmodule"),
	path('createjsonmodule_esdal', views_Esdal.createjsonmodule_esdal, name="createjsonmodule_esdal"),
	path('createjsonmodule_email', views_Esdal.createjsonmodule_email, name="createjsonmodule_email"),

]

# Create your views here.
