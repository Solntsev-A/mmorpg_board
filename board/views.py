from django.shortcuts import render
from board.models import Advertisement


def advertisement_list(request):
    advertisements = Advertisement.objects.select_related('category', 'author').order_by('-created_at')

    return render(
        request,
        'board/advertisement_list.html',
        {
            'advertisements': advertisements,
        }
    )
