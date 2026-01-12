from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from board.models import Advertisement
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy

from .forms import ResponseForm, AdvertisementForm
from .models import Response
from .services.responses import create_response, accept_response, delete_response


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


@login_required
@require_POST
def accept_response_view(request, pk):
    response = get_object_or_404(Response, pk=pk)

    accept_response(
        response=response,
        user=request.user
    )

    return redirect('board:my_responses')


@login_required
@require_POST
def delete_response_view(request, pk):
    response = get_object_or_404(Response, pk=pk)

    delete_response(
        response=response,
        user=request.user
    )

    return redirect('board:my_responses')


class MyAdvertisementResponsesView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'board/my_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = (
            Response.objects
            .filter(advertisement__author=self.request.user)
            .select_related('advertisement', 'author')
            .order_by('-created_at')
        )

        advertisement_id = self.request.GET.get('advertisement')

        if advertisement_id:
            queryset = queryset.filter(advertisement_id=advertisement_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advertisements'] = Advertisement.objects.filter(
            author=self.request.user
        )
        context['selected_advertisement'] = self.request.GET.get('advertisement')
        return context


class MyAdvertisementsView(LoginRequiredMixin, ListView):
    model = Advertisement
    template_name = 'board/my_advertisements.html'
    context_object_name = 'advertisements'

    def get_queryset(self):
        return (
            Advertisement.objects
            .filter(author=self.request.user)
            .select_related('category')
            .order_by('-created_at')
        )


class AdvertisementCreateView(LoginRequiredMixin, CreateView):
    model = Advertisement
    form_class = AdvertisementForm
    template_name = 'board/advertisement_create.html'
    success_url = reverse_lazy('board:advertisement_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
