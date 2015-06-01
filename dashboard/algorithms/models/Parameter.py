__author__ = 'Afonso'

from django.db import models
from Fault import Fault
from AssetType import Technology

class Parameter(models.Model):

    name = models.CharField(max_length=200)
    fault = models.ForeignKey(Fault, blank=True, null=True)
    function = models.ForeignKey('utils.RegressionFunction', null=True, blank=True)
    technology = models.ForeignKey(Technology, null=True, blank=True)

    def __unicode__(self):
        return u'{}'.format(self.name)

    def get_possible_correspondences(self):
        return self.valuecorrespondence_set.all()

    def get_value_correspondent(self, value):
        value_correspondences = self.valuecorrespondence_set.all()
        if len(value_correspondences) == 0:
            print "No value correspondences have been defined"
            raise Exception
        correspondences = filter(lambda x: x.check_correspondence(value), value_correspondences)
        if len(correspondences) == 0:
            print "{}:{} No correspondence".format(self.name, value)
            raise Exception
        elif len(correspondences) > 1:
            print correspondences[0].value
            print correspondences[1].value
            print "Multiple correspondence {}".format(filter(lambda x: x.value, correspondences))
            raise Exception
        else:
            return correspondences[0]

    def is_function(self):
        return self.function is not None

    def get_health_index(self, value):
        if value is None:
            return 0
        if not self.function:
            return self.get_value_correspondent(value).health_index
        return self.function.predict(value)

    def get_alert(self, value):
        return self.get_value_correspondent(value).alert

    def get_warning(self, value):
        print "EEEE"
        print self.get_value_correspondent(value).warning
        return self.get_value_correspondent(value).warning

    def get_sum(self, value):
        return self.get_health_index(value)/100.0

    def save(self, *args, **kwargs):
        if isinstance(self.name, str):
            self.name = self.name.decode("utf-8")
        super(Parameter, self).save(*args, **kwargs)


class ValueCorrespondence(models.Model):
    parameter = models.ForeignKey(Parameter)
    value = models.CharField(max_length=200)
    health_index = models.FloatField()
    warning = models.CharField(max_length=200, null=True, blank=True)
    alert = models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return u'{0}'.format(self.value)

    def check_correspondence(self, value):
        return self.value == value

    def save(self, *args, **kwargs):
        if isinstance(self.value, str):
            self.value = self.value.decode("utf-8")
        super(ValueCorrespondence, self).save(*args, **kwargs)


class Parameters(Parameter):
    class Meta:
        proxy = True
        verbose_name_plural = "Parameters"