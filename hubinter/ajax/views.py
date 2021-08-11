from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages

from videos.models import Tag, Video
from accounts.models import User


""" ----- Add video form ----- """

def tags_by_theme(request):
	"""Get list of tags by passed theme"""
	tags = Tag.objects.filter(theme__name=request.POST.get('theme')).values_list('name')
	if not tags: # if current theme is not chosen, will show all tags
		return JsonResponse({'tags' : "all"})
	else:
		return JsonResponse({
			'tags' : list(tags) #convert to a list, because QuerySet is not json-serializable
		})




""" ----- Video detail ----- """

def turn_on_marker(request):
	"""Add mark for video (and delete opposite mark if necessary)"""
	user = request.user
	video = Video.objects.filter(slug=request.POST.get('slug')).first()

	if user.is_authenticated:
		marker_type = request.POST.get('marker_type')

		if marker_type == 'like':
			if video in user.liked_videos.all():
				return JsonResponse({
					'status' : '200',
					'current_likes' : video.likes,
					'current_dislikes' : video.dislikes,
				})
			else:
				if user.disliked_videos.filter(slug=video.slug).exists(): # if opposite mark is put
					turn_off_marker(request) # turn opposite off
					video = Video.objects.filter(slug=request.POST.get('slug')).first() # should get video-object again, to have actual data after executing turn_off_marker()
					user.liked_videos.add(video) # and then, add our mark
				else:
					user.liked_videos.add(video)
				video.likes += 1
		else:
			if video in user.disliked_videos.all():
				return JsonResponse({
					'status' : '200',
					'current_likes' : video.likes,
					'current_dislikes' : video.dislikes,
				})
			else:
				if user.liked_videos.filter(slug=video.slug).exists(): # the same, as above...
					turn_off_marker(request)
					video = Video.objects.filter(slug=request.POST.get('slug')).first() # the same, as above...
					user.disliked_videos.add(video)
				else:
					user.disliked_videos.add(video)
				video.dislikes += 1

		user.save()
		video.save()
	else:
		return JsonResponse({
			'status' : '200',
			'current_likes' : video.likes,
			'current_dislikes' : video.dislikes,
			'need_to_login' : True
		})

	return JsonResponse({
		'status' : '200',
		'current_likes' : video.likes,
		'current_dislikes' : video.dislikes,
	})


def turn_off_marker(request):
	"""Remove mark from video"""
	user = request.user
	video = Video.objects.filter(slug=request.POST.get('slug')).first()

	if user.is_authenticated:
		if request.POST.get("is_ajax"): # if was sent by ajax (request to just remove the mark, not change it to opposite)
			marker_type = request.POST.get("marker_type")
		else: # if called by function "turn_on_marker", change given value to opposite (why? see above)
			marker_type = "like" if request.POST.get('marker_type') == 'dislike' else "dislike"

		if marker_type == 'like':
			user.liked_videos.remove(video.pk)
			video.likes -= 1
		else:
			user.disliked_videos.remove(video.pk)
			video.dislikes -= 1

		user.save()
		video.save()
	else:
		return JsonResponse({
			'status' : '200',
			'current_likes' : video.likes,
			'current_dislikes' : video.dislikes,
			'need_to_login' : True
		})

	return JsonResponse({
		'status' : '200',
		'current_likes' : video.likes,
		'current_dislikes' : video.dislikes,
	})



def subscribe(request):
	"""Subscribe request-user to the author"""
	user = request.user

	if user.is_authenticated:
		author = User.objects.get(username=request.POST.get("author_username"))

		if user in author.subscribers.all(): # if already subscribed
			return JsonResponse({
				"status" : "200",
			})
		else:
			author.subscribers.add(user)
			author.subscribers_amount += 1
			author.save()

	else:
		return JsonResponse({
			"status" : "200",
			"need_to_login" : True
		})

	return JsonResponse({
		"status" : "200",
		"current_subs" : author.subscribers_amount,
		"current_user_is_author" : True if user == author else False
		# current_user_is_author - this arg is for that the author of the video doesn't see the notification button after subscribing to himself
	})


def unsubscribe(request):
	"""Unsubscribe request-user from the author"""
	user = request.user

	if user.is_authenticated:
		author = User.objects.get(username=request.POST.get("author_username"))
		
		if user not in author.subscribers.all(): # if already unsubscribed
			return JsonResponse({
				"status" : "200",
			})
		else:
			author.subscribers.remove(user)
			author.subscribers_amount -= 1
			if user in author.notifications.all(): # also turn off notifications
				author.notifications.remove(user)
			author.save()

	else:
		return JsonResponse({
			"status" : "200",
			"need_to_login" : True
		})

	return JsonResponse({
		"status" : "200",
		"current_subs" : author.subscribers_amount,
	})



def notify(request):
	"""Notify request-user about new author's video"""
	user = request.user

	if user.is_authenticated:
		author = User.objects.get(username=request.POST.get("author_username"))

		if user not in author.subscribers.all(): # must be subscribed to get notifications
			return JsonResponse({
				"status" : "200",
				"need_to_subscribe" : True,
			})
		else:
			if user in author.notifications.all():
				return JsonResponse({
					"status" : "200",
				})
			else:
				author.notifications.add(user)
				author.save()

	else:
		return JsonResponse({
			"status" : "200",
			"need_to_login" : True,
		})

	return JsonResponse({
		"status" : "200",
	})


def not_notify(request):
	"""DONT notify request-user about new author's video"""
	user = request.user

	if user.is_authenticated:
		author = User.objects.get(username=request.POST.get("author_username"))

		if user not in author.notifications.all():
			return JsonResponse({
				"status" : "200",
			})
		else:
			author.notifications.remove(user)
			author.save()
	else:
		return JsonResponse({
			"status" : "200",
			"need_to_login" : True,
		})

	return JsonResponse({
		"status" : "200",
	})
