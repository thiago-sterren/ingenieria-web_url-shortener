from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ShortenedURL

def index(request):
    if request.method == 'POST':
        original_url = request.POST.get('original_url')
        if original_url:
            user = request.user if request.user.is_authenticated else None
            url = ShortenedURL.objects.create(original_url=original_url, creator=user)
            host = request.get_host()
            scheme = request.scheme
            full_short_url = f"{scheme}://{host}/{url.short_id}"
            return render(request, 'shortener/index.html', {'short_url': full_short_url, 'url_obj': url})
    return render(request, 'shortener/index.html')

@login_required
def dashboard(request):
    urls = ShortenedURL.objects.filter(creator=request.user).order_by('-created_at')
    host = request.get_host()
    scheme = request.scheme
    base_url = f"{scheme}://{host}/"
    return render(request, 'shortener/dashboard.html', {'urls': urls, 'base_url': base_url})

def redirect_url(request, short_id):
    url = get_object_or_404(ShortenedURL, short_id=short_id)
    url.clicks += 1
    url.save(update_fields=['clicks'])
    return redirect(url.original_url)
