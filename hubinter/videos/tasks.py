from django.template.loader import render_to_string 
from django.core.mail import EmailMessage

from accounts.models import User
from .models import Video, YoutubeVideo
from hubinter.celery import app


@app.task
def send_email_notifications(author_username, video_slug, video_type, url):
	'''Send notifications for subscribers, when author publish new video'''
	author = User.objects.get(username=author_username)

	if video_type == "uploaded":
		video = Video.objects.get(slug=video_slug)
	else:
		video = YoutubeVideo.objects.get(slug=video_slug)

	context = {
		"author" : author,
		"video" : video,
		'url' : url
	}
	html_message = render_to_string("videos/email_notification_msg.html", context)

	msg = EmailMessage(
		f"🔴 New video on channel '{author.username}'",
		html_message,
		None,
		list(
			map( lambda x: x[0], author.notifications.values_list("email") )
		),
	)
	msg.content_subtype = 'html'
	msg.send()