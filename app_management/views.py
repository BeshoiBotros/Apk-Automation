from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views import View
from .models import AppManagement
from .forms import AppManagementForm
import automation

def is_auth(request):
    return not request.user.is_anonymous

class HomeView(View):

    def get(self, request, *args, **kwargs):
        if not is_auth(request):
            return redirect('login')
        
        form  = AppManagementForm()
        user_apps = AppManagement.objects.filter(uploaded_by=request.user)
        context = {
            "apps": user_apps,
            "form": form,
            "update_form": form,  # Pass form for rendering in modal
        }
        return render(request, "apk_management/home.html", context)
    
    def post(self, request):
        form  = AppManagementForm(request.POST, request.FILES)
        if form.is_valid():
            app_management = form.save(commit=False)
            app_management.uploaded_by = request.user
            app_management.save()
            return redirect("home")
        user_apps = AppManagement.objects.filter(uploaded_by=request.user)
        context = {
            'errors': form.non_field_errors,
            "apps": user_apps,
            "form": form,
            "update_form": form,
        }
        return render(request, 'apk_management/home.html', context)
    
def delete_app(request, pk):
    if not is_auth(request):
        return redirect('login')
    
    app = get_object_or_404(AppManagement, pk=pk)
    if app.uploaded_by.pk != request.user.pk:
        return redirect("home")
    else:
        app.delete()
        return redirect("home")

def update_app(request, pk):
    app = get_object_or_404(AppManagement, pk=pk)

    if request.method == 'POST':
        form = AppManagementForm(request.POST, request.FILES, instance=app)
        if form.is_valid() and app.uploaded_by.pk == request.user.pk:
            form.save()
            return redirect("home")
    else:
        form = AppManagementForm(instance=app)

    return render(request, 'apk_management/home.html', {'form': form})


def run_app(request, pk):
    app = get_object_or_404(AppManagement, id=pk)
    if app.uploaded_by.pk != request.user.pk:
        return redirect('home')
    automation.automate_app(app)
    return redirect("home")

    