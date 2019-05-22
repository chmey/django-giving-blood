from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def review_place(request):
    return render(request, 'admin/review_place.html')
