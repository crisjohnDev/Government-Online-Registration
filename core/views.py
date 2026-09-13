from django.shortcuts import render, redirect, get_object_or_404
from Applicants.models import Barangay

def add_brgy(request):

    if request.method == "POST":
        name = request.POST.get("name")

        # Check if barangay already exists
        if Barangay.objects.filter(name=name).exists():
            return render(request, "comelec/brgy_form.html", {
                "error": "Barangay already exists!",
                "name": name,
            })

        Barangay.objects.create(
            name=name
        )

        return redirect("brgy_list")

    return render(request, "comelec/brgy_form.html")


def brgy_list(request):
    barangays = Barangay.objects.all()
    return render(request, 'comelec/brgy_list.html', {"barangays":barangays})

def delete_brgy(request, pk):

    barangay = Barangay.objects.get(pk=pk)

    if request.method == "POST":
        barangay.delete()
        return redirect("brgy_list")

    return render(request, "comelec/brgy_delete.html", {
        "barangay": barangay
    })