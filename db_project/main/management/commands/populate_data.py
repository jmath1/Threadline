from django.core.management.base import BaseCommand
from main.factories import UserFactory, ThreadFactory, MessageFactory
from main.models import Hood, Thread, Message


class Command(BaseCommand):
    help = "Load Philadelphia GIS data into the database"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting data population...")

        # Create 20 members for each hood
        for hood in Hood.objects.all():
            self.stdout.write(f"Processing hood: {hood.name} (ID: {hood.id})")
            members = [UserFactory(hood=hood) for _ in range(20)]
            self.stdout.write(f"Created 20 members for hood: {hood.name}")

            # Each member creates a thread
            for member in members:
                thread = ThreadFactory(hood=hood, author=member)
                self.stdout.write(f"Created thread (ID: {thread.id}) by member (ID: {member.id}) in hood: {hood.name}")

                # Other members respond to the thread
                for responder in members:
                    message = MessageFactory(thread_id=thread.id, author_id=responder.id)
                    self.stdout.write(f"Created message (ID: {message.id}) in thread (ID: {thread.id}) by responder (ID: {responder.id})")

        self.stdout.write(self.style.SUCCESS("Successfully populated users, threads, and messages for each hood."))
