

def update_object(obj, **kwargs) -> None:
    """
    Update object attributes in the database.
    """
    if kwargs:
        obj.__class__.objects.filter(pk=obj.pk).update(**kwargs)
