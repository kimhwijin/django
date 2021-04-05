from django.db import models

# Create your models here.

class StockInfo(models.Model):
    per = models.PositiveIntegerField(null=False,default=10)
    name = models.CharField(max_length=100,null=False)
    code = models.CharField(max_length=6,null=False)

    class Meta:
        managed = False
        db_table = 'stock_stockinfo'

    def __str__(self):
        return self.name
