import factory
from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from main.models import (Follow, Friendship, Hood, Message, Notification,
                         Thread, User)


class HoodFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Hood

    name = factory.Faker("city")
    polygon = factory.LazyFunction(
        lambda: MultiPolygon(Polygon(((0.0, 0.0), (0.0, 1.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0))))
    )

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
    description = factory.Faker("text")
    photo_url = factory.Faker("image_url")
    coords = factory.LazyFunction(lambda: Point(-75.1764407, 39.9404423, srid=4326))
    address = factory.Faker("address")
    hood = factory.SubFactory(HoodFactory)

class FriendshipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Friendship

    from_user = factory.SubFactory(UserFactory)
    to_user = factory.SubFactory(UserFactory)
    status = "REQUESTED"

class FollowFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Follow

    follower = factory.SubFactory(UserFactory)
    followee = factory.SubFactory(UserFactory)

class ThreadFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thread

    name = factory.Faker("sentence", nb_words=3)
    type = "PUBLIC"
    hood = factory.SubFactory(HoodFactory)
    author = factory.SubFactory(UserFactory)

class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    thread = factory.SubFactory(ThreadFactory)
    author = factory.SubFactory(UserFactory)
    content = factory.Faker("text")

class NotificationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Notification

    user = factory.SubFactory(UserFactory)
    thread = factory.SubFactory(ThreadFactory)
    message = factory.SubFactory(MessageFactory)
    type = "MESSAGE_TAG"
    status = "UNREAD"
