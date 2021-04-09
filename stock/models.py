from django.db import models

# Create your models here.

class StockInfo(models.Model):
    name = models.CharField(max_length=120,null=False)
    code = models.CharField(max_length=6,null=False)
    

    class Meta:
        db_table = 'stock_stockinfo'

    def __str__(self):
        return self.name


class PerInfo(models.Model):
    year = models.IntegerField(null=False)
    per = models.PositiveIntegerField(null=False,default=10)
    stock_id = models.ForeignKey(StockInfo, on_delete=models.CASCADE, db_column="stock_id")
    
    class Meta:
        db_table = 'stock_perinfo'

    def __str__(self):
        return self.name