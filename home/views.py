from django.shortcuts import render
from django.views.generic import TemplateView, FormView


class Home(TemplateView):

    template_name = 'home/index.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.request.session["my_name"]='amir'
        print(self.request.session.get('my_name','default'))
        return context


