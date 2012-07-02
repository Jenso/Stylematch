from django.db import models


class BetaEmail(models.Model):
    email = models.EmailField()

    def __unicode__(self):
        return u'%s' % (self.email)


class Tip(models.Model):
    name = models.CharField("Namn", max_length=30)
    address = models.CharField("Adress", max_length=30)
    zip = models.CharField("Postnummer", max_length=5)
    city = models.CharField("Stad", max_length=50)
    phone = models.CharField("Mobilnummer", max_length=15, unique=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s, %s' % (self.name, self.phone)
