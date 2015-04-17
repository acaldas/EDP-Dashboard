# -*- coding: latin1 -*-

from django.db import models


class RegressionFunction(models.Model):
    LINEAR = 1
    EXPONENTIAL = 2
    QUADRATIC_SECOND = 3
    QUADRATIC_THIRD = 4

    TYPE_CHOICES = (
        (LINEAR, u'Linear'),
        (EXPONENTIAL, u'Exponencial'),
        (QUADRATIC_SECOND, u'Quadrática 2º Grau'),
        (QUADRATIC_THIRD, u'Quadrática 3º Grau'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES,
                               default=LINEAR)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name


class FunctionValue(models.Model):
    function = models.ForeignKey(RegressionFunction)
    x = models.FloatField()
    y = models.FloatField()

    def __unicode__(self):
        return "{} - {}".format(self.x, self.y)