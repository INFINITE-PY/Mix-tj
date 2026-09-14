from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Video, Category, Channel, Comment
from django.contrib.auth import logout
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm

def index(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '')
    filter_type = request.GET.get('filter', 'popular')

    videos = Video.objects.all()
    categories = Category.objects.all()
    channels = Channel.objects.all()[:5]

    # 1. Полнофункциональный поиск (Title + Description)
    if query:
        videos = videos.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # 2. Фильтрация по категориям
    if category_slug:
        videos = videos.filter(category__slug=category_slug)

    # 3. Фильтрация по вкладкам (Популярное / ТОП дня / Новинки)
    if filter_type == 'popular':
        videos = videos.order_by('-views')
    elif filter_type == 'new':
        videos = videos.order_by('-created_at')

    # Видео для сайдбара "Новинки"
    sidebar_new_videos = Video.objects.order_by('-created_at')[:4]

    context = {
        'videos': videos,
        'categories': categories,
        'channels': channels,
        'query': query,
        'filter_type': filter_type,
        'sidebar_new_videos': sidebar_new_videos
    }
    return render(request, 'youtube/index.html', context)


def watch(request, id):
    video = get_object_or_404(Video, id=id)
    video.views += 1
    video.save()

    if request.method == 'POST' and request.user.is_authenticated:
        text = request.POST.get('text')
        if text:
            Comment.objects.create(video=video, user=request.user, text=text)
            return redirect('watch', id=video.id)

    comments = video.comments.all().order_by('-created_at')
    return render(request, 'youtube/watch.html', {'video': video, 'comments': comments})


def upload_video(request):
    if not request.user.is_authenticated:
        return redirect('index')

    categories = Category.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration', '00:00')
        category_id = request.POST.get('category')
        video_file = request.FILES.get('video')
        thumbnail = request.FILES.get('thumbnail')

        channel, _ = Channel.objects.get_or_create(user=request.user, defaults={'name': request.user.username})
        category = Category.objects.filter(id=category_id).first()

        Video.objects.create(
            channel=channel,
            category=category,
            title=title,
            description=description,
            duration=duration,
            video_file=video_file,
            thumbnail=thumbnail
        )
        return redirect('index')

    return render(request, 'youtube/upload.html', {'categories': categories})


def logout_view(request):
    logout(request)
    return redirect('index')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()

    return render(request, 'youtube/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'youtube/register.html', {'form': form})