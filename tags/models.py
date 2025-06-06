from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.
class TaggedItemManager(models.Manager):
    def get_tags_for(self,obj_type,obj_id):
        content_type = ContentType.objects.get_for_model(obj_type)
        return TaggedItem.objects.\
        select_related('tag')\
        .filter(
        content_type=content_type,
        object_id=obj_id
        )
class Tag(models.Model):
    label=models.CharField(max_length=255)
    def __str__(self):
        return self.label
    
    
class TaggedItem(models.Model):
    # what tag is applied to what object(product,video, article, service..)
    tag=models.ForeignKey(Tag,on_delete=models.CASCADE)
    #object(product,video, article, service..) -> to determine table in the database
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE)
    #ID of that object -> 
    object_id=models.PositiveIntegerField()
    #to know exactly what is the  that object:
    content_object=GenericForeignKey()
    objects=TaggedItemManager() # a class
    
