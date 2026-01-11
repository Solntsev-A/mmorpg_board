from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from board.models import Advertisement
from django.views.generic import ListView, DetailView

from .forms import ResponseForm
from .services.responses import create_response


def advertisement_list(request):
    advertisements = Advertisement.objects.select_related('category', 'author').order_by('-created_at')

    return render(
        request,
        'board/advertisement_list.html',
        {
            'advertisements': advertisements,
        }
    )


class AdvertisementListView(ListView):
    model = Advertisement
    template_name = 'board/advertisement_list.html'
    context_object_name = 'advertisements'


class AdvertisementDetailView(DetailView):
    model = Advertisement
    template_name = 'board/advertisement_detail.html'
    context_object_name = 'advertisement'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ResponseForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = ResponseForm(request.POST)

        if form.is_valid():
            create_response(
                user=request.user,
                advertisement=self.object,
                text=form.cleaned_data['text']
            )
            return redirect('board:advertisement_detail', pk=self.object.pk)

        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
