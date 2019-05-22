from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import DonationPlace


@staff_member_required
def review_place(request, id):
    place = get_object_or_404(DonationPlace, pk=id)
    if request.method == 'POST':
        if request.POST['approve'] == 'true':
            place.published = True
            place.save()
            # redirect to donation place page
            redirect('/')
    else:
        num_contributions = DonationPlace.objects.filter(contributor=place.contributor).count()
        return render(request, 'admin/review_place.html', {'place': place, 'num_contributions': num_contributions})
