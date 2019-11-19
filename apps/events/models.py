from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings


class TimeStampModel(models.Model):

    created = models.DateTimeField( auto_created=True )
    modified = models.DateTimeField( auto_now=True )

    class Meta:
        abstract = True

class Category(models.Model):

    name = models.CharField(max_length=50)
    slug = models.SlugField(editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Event(TimeStampModel):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(editable=False)
    summary = models.TextField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=False)
    place = models.CharField(max_length=50)
    start = models.DateTimeField()
    finish = models.DateTimeField()
    imagen = models.ImageField(upload_to='events') #Falta algo
    is_free = models.BooleanField(default=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    views = models.PositiveIntegerField(default=0)
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)

        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Assitant(TimeStampModel):

    assitant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=False)
    event = models.ManyToManyField(Event)

    attended = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.assitant.username, self.event.name)

class Comments(TimeStampModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=False)
    event = models.ForeignKey(Event, on_delete=False)
    content = models.TextField()

    def __str__(self):
        return "{} {}".format(self.user.username, self.event.name)

