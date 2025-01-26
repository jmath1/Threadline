NOTIFICATION_TYPES = [
    ('FRIEND_REQUESTED', 'Friend Request'),
    ('FRIEND_ACCEPTED', 'Friend Accept'),
    ('MESSAGE', 'Message'),
    ('FOLLOW', 'Follow'),
]

NOTIFICATION_STATUSES = [
    ('UNREAD', 'Unread'),
    ('READ', 'Read'),
]

FRIEND_REQUEST_STATUS_CHOICES = [
    ('REQUESTED', 'Requested'),
    ('ACCEPTED', 'Accepted'),
    ('REJECTED', 'Rejected'),
]

THREAD_TYPES = [
    ("PUBLIC", 'Public'), # everyone can see
    ("PRIVATE", 'Private'), # only tagged users
    ("HOOD", 'Hood'), # only hood members
]