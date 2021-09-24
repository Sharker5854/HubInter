from django.utils.text import slugify
from django.db.models import signals
from django.dispatch import receiver



@receiver(signals.pre_save, sender="videos.Theme")
@receiver(signals.pre_save, sender="videos.Tag")
def populate_slug(sender, instance, **kwargs):
	'''Due to the fact that the slug doesn't change while editing the name in admin panel,
	should use presave signal to change slug again'''
	instance.slug = slugify(instance.name)