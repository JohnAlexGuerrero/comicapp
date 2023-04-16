from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

from django.utils.text import slugify

from PIL import Image
from io import BytesIO
from django.core.files import File

class Collection(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()

    class Meta:
        verbose_name = ("Collection")
        verbose_name_plural = ("Collections")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.slug


class Comic(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(upload_to="uploads/", blank=True, null=True)
    thumbnail = models.ImageField(upload_to="uploads/", blank=True, null=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)
    fron_page = models.CharField(max_length=100, null=False)
    collection = models.ForeignKey(Collection, verbose_name=("collections"), on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = ("Comic")
        verbose_name_plural = ("Comics")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.slug
    
    def get_logo(self):
        if self.logo:
            return 'http://127.0.0.1:8000' + self.logo.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' +  self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return 'http://127.0.0.1:8000' +  self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(400,300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thum_io = BytesIO()
        img.save(thum_io, 'JPEG', quality=85)
        
        thumbnail = File(thum_io, name=image.name)
        
        return thumbnail
        
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''



@receiver(post_save, sender=Collection)
def save_slug_collection(sender, instance, created, **kwargs):
    collection = Collection.objects.get(name=instance)
    
    if created:
        collection.slug = slugify(collection.name)
        collection.save()

@receiver(post_save, sender=Comic)
def save_slug_comic(sender, instance, created, **kwargs):
    comic = Comic.objects.get(title=instance)
    
    if created:
        comic.slug = slugify(comic.title)
        comic.save()