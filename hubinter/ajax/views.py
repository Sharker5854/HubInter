from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from videos.models import Tag

@csrf_exempt
def tags_by_theme(request):
	tags = Tag.objects.filter(theme__name=request.POST.get('theme')).values_list('name')
	if not tags: # if current theme is not chosen, will show all tags
		return JsonResponse({'tags' : "all"})
	else:
		return JsonResponse({
			'tags' : list(tags) #convert to a list, because QuerySet is not json-serializable
		})