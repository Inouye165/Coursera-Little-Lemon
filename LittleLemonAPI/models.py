from django.db import models

# Create your models here.

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.title
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6,decimal_places=2)
    inventory = models.SmallIntegerField()
    
    # I continually had a 500 error " NOT NULL constraint failed: LittleLemonAPI_menuitem.category_id"
    # After checking this with Gemini I changed the following line from the course instructions to null = true.  I do not know why yet why it didnt work the previous way
    category = models.ForeignKey(Category, on_delete=models.PROTECT,default=1)
    # category = models.ForeignKey(Category, on_delete=models.PROTECT,null = True)

    