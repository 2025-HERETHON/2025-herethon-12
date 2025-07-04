from django.shortcuts import render

# Create your views here.
def post_add(request):
    return render(request, "posts/post.html")