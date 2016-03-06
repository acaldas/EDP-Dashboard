# -*- coding: latin1 -*-

from django.db import models
import abc
from scipy import stats
from math import log
from pylab import *
from numpy import poly1d, polyfit

class RegressionFunction(models.Model):

    LINEAR = 1
    EXPONENTIAL = 2
    QUADRATIC_SECOND = 3
    QUADRATIC_THIRD = 4

    TYPE_CHOICES = (
        (LINEAR, u'Linear'),
        (EXPONENTIAL, u'Exponencial'),
        (QUADRATIC_SECOND, u'Quadr�tica 2� Grau'),
        (QUADRATIC_THIRD, u'Quadr�tica 3� Grau'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES, default=LINEAR, verbose_name=u"Tipo de Regress�o")
    name = models.CharField(max_length=200, verbose_name=u"Nome")

    class Meta:
        ordering = ('name',)
        verbose_name = u'Fun��o de Regress�o'
        verbose_name_plural = u'Fun��es de Regress�o'

    def __unicode__(self):
        return self.name

    def predict(self, value):
        x_values = map(lambda val: val.x, self.functionvalue_set.all())
        y_values = map(lambda val: val.y, self.functionvalue_set.all())
        if self.type == self.LINEAR:
            model = LinearFunction(x_values, y_values)
        elif self.type == self.EXPONENTIAL:
            model = ExponentialFunction(x_values, y_values)
        elif self.type == self.QUADRATIC_SECOND:
            model = QuadraticFunction(x_values, y_values, 2)
        elif self.type == self.QUADRATIC_THIRD:
            model = QuadraticFunction(x_values, y_values, 3)
        else:
            print "Function {} has invalid type: {}".format(self.name, self.type)
            raise Exception

        return model.predict(value)


class FunctionValue(models.Model):
    class Meta:
        verbose_name = u'Valor de Fun��o'
        verbose_name_plural = u'Valores de Fun��o'

    function = models.ForeignKey(RegressionFunction)
    x = models.FloatField()
    y = models.FloatField()

    def __unicode__(self):
        return "{} - {}".format(self.x, self.y)


class Function(object):
    def __init__(self, x_values, y_values):
        self.x_values = x_values
        self.y_values = y_values

    @abc.abstractmethod
    def predict(self, value):
        return


class LinearFunction(Function):
    def __init__(self, x_values, y_values,):
        Function.__init__(self, x_values, y_values)
        self.slope, self.intercept, r_value, p_value, std_err = stats.linregress(np.array(self.x_values), np.array(self.y_values))

    def predict(self, value):
        return round(self.intercept + self.slope * value, 3)


class QuadraticFunction(Function):
    def __init__(self, x_values, y_values, degree):
        Function.__init__(self, x_values, y_values)
        self.model = poly1d(polyfit(self.x_values, self.y_values, degree))

    def predict(self, value):
        return round(self.model(value), 3)


class ExponentialFunction(Function):
    def __init__(self, x_values, y_values):
        Function.__init__(self, x_values, y_values)
        self.slope, self.intercept = self.get_slope()

    @staticmethod
    def expfunc(x, a, b):
        return a * exp(b * x)

    def get_slope(self):
        slope, intercept, r_value, p_value, std_err = stats.linregress(np.array(self.x_values), np.array(log(self.y_values)))# map(lambda y: log(y), self.y_values))

        return slope, intercept

    def predict(self, value):
        return round(ExponentialFunction.expfunc(value, exp(self.intercept), self.slope), 3)