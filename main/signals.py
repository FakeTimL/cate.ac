from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model, user_logged_in
from .models import UserLearningData

UserModel = get_user_model()


@receiver(user_logged_in, sender=UserModel)
def create_learning_data(sender, request, user, **kwargs):
  if not hasattr(user, 'learning_data'):
    print('Creating learning data for', user)
    UserLearningData.objects.create(user=user)
