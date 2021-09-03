from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist

from videos.models import Tag, Video, Comment
from accounts.models import User
from videos.forms import AddCommentForm


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
					'current_likes' : video.liked_by.count(),
					'current_dislikes' : video.disliked_by.count(),
				})
			else:
				if user.disliked_videos.filter(slug=video.slug).exists(): # if opposite mark is put
					turn_off_marker(request) # turn opposite off
					video = Video.objects.filter(slug=request.POST.get('slug')).first() # should get video-object again, to have actual data after executing turn_off_marker()
					user.liked_videos.add(video) # and then, add our mark
				else:
					user.liked_videos.add(video)
		else:
			if video in user.disliked_videos.all():
				return JsonResponse({
					'status' : '200',
					'current_likes' : video.liked_by.count(),
					'current_dislikes' : video.disliked_by.count(),
				})
			else:
				if user.liked_videos.filter(slug=video.slug).exists(): # the same, as above...
					turn_off_marker(request)
					video = Video.objects.filter(slug=request.POST.get('slug')).first() # the same, as above...
					user.disliked_videos.add(video)
				else:
					user.disliked_videos.add(video)

		user.save()
		video.save()
	else:
		return JsonResponse({
			'status' : '200',
			'current_likes' : video.liked_by.count(),
			'current_dislikes' : video.disliked_by.count(),
			'need_to_login' : True
		})

	return JsonResponse({
		'status' : '200',
		'current_likes' : video.liked_by.count(),
		'current_dislikes' : video.disliked_by.count(),
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
		else:
			user.disliked_videos.remove(video.pk)

		user.save()
		video.save()
	else:
		return JsonResponse({
			'status' : '200',
			'current_likes' : video.liked_by.count(),
			'current_dislikes' : video.disliked_by.count(),
			'need_to_login' : True
		})

	return JsonResponse({
		'status' : '200',
		'current_likes' : video.liked_by.count(),
		'current_dislikes' : video.disliked_by.count(),
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
			author.save()

	else:
		return JsonResponse({
			"status" : "200",
			"need_to_login" : True
		})

	return JsonResponse({
		"status" : "200",
		"current_subs" : author.subscribers.count(),
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
		"current_subs" : author.subscribers.count(),
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



@login_required
@require_http_methods(["POST"])
def add_comment(request):
	"""Create new comment and fill in path to the parent comment (if answer to another one)"""
	form = AddCommentForm(request.POST)
	video = Video.objects.get(slug=request.POST["video_slug"])

	if form.is_valid():
		comment = Comment(
			path=[], # will resave it below...
			author=request.user,
			video=video,
			text=form.cleaned_data['comment_text']
		)
		comment.save()

		try:
			comment.path.extend( Comment.objects.get(pk=form.cleaned_data['parent_comment']).path )
			comment.path.append(comment.id)
		except ObjectDoesNotExist:
			comment.path.append(comment.id)

		comment.save()

		if comment.get_comment_offset() == 0:
			return JsonResponse({
				"comment_id" : comment.id,
				"parent_comment_id" : "no-parent",
				"author_username" : comment.author.username,
				"author_url" : comment.author.get_absolute_url(),
				"created_at" : comment.get_created_at(),
				"text" : comment.text,
				"answer" : False,
				"current_comments_count" : video.comment_set.count()
			})
		else:
			return JsonResponse({
				"comment_id" : comment.id,
				"parent_comment_id" : form.cleaned_data['parent_comment'],
				"author_username" : comment.author.username,
				"author_url" : comment.author.get_absolute_url(),
				"created_at" : comment.get_created_at(),
				"text" : comment.text,
				"answer" : True,
				"current_comments_count" : video.comment_set.count()
			})