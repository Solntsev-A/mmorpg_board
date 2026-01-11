from django.shortcuts import render
from board.models import Advertisement
from django.views.generic import ListView

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
