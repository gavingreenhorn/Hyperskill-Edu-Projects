from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView

from news.utils import *


class MainView(View):
    """ Main page view """

    def get(self, request):
        JSON = get_json()
        if q := request.GET.get('q'):
            grouped_data = group_by_date(pattern=q)
        else:
            grouped_data = group_by_date()
        sorted_data = sorted(grouped_data.items(), reverse=True)
        return render(request, 'news/main.html', {'data': sorted_data})


class PostView(TemplateView):
    """ Individual post view """
    template_name = 'news/post.html'

    def get_context_data(self, **kwargs):
        JSON = get_json()
        link = kwargs['link']
        context = next((obj for obj in JSON if obj['link'] == int(link)))
        return context


class CreateView(View):
    """ New post page view """

    def get(self, request):
        return render(request, 'news/create.html')

    def post(self, request):
        JSON = get_json()
        title, text = request.POST['title'], request.POST['text']
        created, link = get_post_data()
        add_post(created, text, title, link)
        return redirect('/news/')
