from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from board.models import Advertisement, Response
from django.views.generic import ListView, DetailView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from .forms import ResponseForm
from .models import Response
from .services.responses import create_response, accept_response


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
        context['responses'] = (self.object.responses.select_related('author').order_by('-created_at'))
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

@login_required
def accept_response_view(request, pk):
    response = get_object_or_404(Response, pk=pk)

    accept_response(
        response=response,
        user=request.user
    )

    return redirect(
        'board:advertisement_detail',
        pk=response.advertisement.pk
    )


class MyAdvertisementResponsesView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'board/my_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return (
            Response.objects
            .filter(advertisement__author=self.request.user)
            .select_related('advertisement', 'author')
            .order_by('-created_at')
        )
