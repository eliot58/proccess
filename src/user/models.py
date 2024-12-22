from tortoise import models, fields

class User(models.Model):
    id = fields.IntField(pk=True)
    tg_id = fields.CharField(max_length=256, unique=True)
    toncoin = fields.FloatField(default=0)
    notcoin = fields.FloatField(default=0)
    tether = fields.FloatField(default=0)