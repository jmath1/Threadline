from datetime import datetime

import factory
from django.contrib.gis.geos import MultiPolygon, Point, Polygon
from main.models import Follow, Friendship, Hood, Message, Thread, User


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

    username = factory.Sequence(lambda n: f"User{n}")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall("set_password", "password")
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

class MessageFactory(factory.mongoengine.MongoEngineFactory):
    class Meta:
        model = Message
        
    thread_id = factory.LazyAttribute(lambda _: str(ThreadFactory().id))  # Reference to Thread (PostgreSQL)
    author_id = factory.LazyAttribute(lambda _: str(UserFactory().id)) 
    content = factory.Faker("text")
    created_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyFunction(datetime.now)
