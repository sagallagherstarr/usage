# models

from peewee import Model, BooleanField, DateTimeField

class ModelBase(Model):
    active = BooleanField(default=True)
    inactive_date = DateTimeField(null=True, default=None)
    
    headerNames = [ "Unique ID", "Active", "Inactive date" ]

__all__ = [ "ModelBase"  ]
