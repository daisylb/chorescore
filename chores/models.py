from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.utils.timezone import UTC

def get_scoreboard(days=None):
    """Returns a list of users, annotated with their total score for the given
    number of days under `.score`. If `days` is ommitted, returns the score
    since the beginning of time.
    """
    qs = User.objects.all()

    if days:
        first_day = datetime.now() - timedelta(days=days)
        qs = qs.filter(choreevent__performed_at__gte=first_day)

    # note: filter must come before annotate, otherwise the generated SQL just
    # JOINs in the choreevent table twice, applying the filter to one and the
    # aggregation to the other
    qs = qs.annotate(score=models.Sum("choreevent__chore__score")
            ).order_by("-score")

    return qs

class Category (models.Model):
    name = models.CharField(max_length=256)
    def __unicode__(self):
        return self.name

class Chore (models.Model):
    name = models.CharField(max_length=256)
    score = models.PositiveSmallIntegerField()
    category = models.ForeignKey(Category, related_name='chores',
        blank=True, null=True)
    max_age = models.PositiveSmallIntegerField(blank=True, null=True)
    reminder = models.BooleanField(default=False)

    @property
    def last_performed_delta(self):
        return datetime.now().replace(tzinfo=UTC()) - self.last_performed

    @property
    def overdue(self):
        return self.last_performed_delta >= timedelta(days=self.max_age)

    def __unicode__(self):
        return "{}: {}".format(self.score, self.name)

class ChoreEvent (models.Model):
    chore = models.ForeignKey(Chore, related_name='events')
    user = models.ForeignKey(User)
    performed_at = models.DateTimeField(auto_now_add=True)
