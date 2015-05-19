
from django.test import TestCase
from models.AssetType import AssetType, Technology
from models.Parameter import Parameter, ValueCorrespondence
from utils.models import RegressionFunction, FunctionValue
from network.models import Asset

class AssetTestCase(TestCase):
    def setUp(self):
        self.tec = Technology.objects.create(name="Bateria Alcalina", max_lifetime=20, obsolescence_lifetime=10)
        f = RegressionFunction.objects.create(type=RegressionFunction.QUADRATIC_THIRD, name="Bateria Alcalina Aging")
        FunctionValue.objects.create(function=f, x=0, y=0.05)
        FunctionValue.objects.create(function=f, x=5, y=0.2)
        FunctionValue.objects.create(function=f, x=10, y=0.4)
        FunctionValue.objects.create(function=f, x=15, y=0.7)
        FunctionValue.objects.create(function=f, x=20, y=1)
        self.assettype = AssetType.objects.create(name="Bateria Alcalina", technology=self.tec, aging_function=f)
        self.asset = Asset.objects.create(name="Bateria Alcalina teste", fabrication_date=2000, asset_type=self.assettype)

    def test_asset(self):
        asset = Asset.objects.get()
        assettype = AssetType.objects.get()
        tec = Technology.objects.get()
        self.assertEqual(asset, self.asset)
        self.assertEqual(assettype, self.assettype)
        self.assertEqual(asset.asset_type, self.assettype)
        self.assertEqual(tec, self.tec)
        self.assertEqual(assettype.technology, self.tec)
        self.assertEqual(asset.get_age(), 15)
        self.assertEqual(asset.get_age_failure_probability(), 0.691)


class ParameterTestCase(TestCase):
    def setUp(self):
        self.tec = Technology.objects.create(name="Bateria Alcalina", max_lifetime=20, obsolescence_lifetime=10)
        f = RegressionFunction.objects.create(type=RegressionFunction.QUADRATIC_THIRD, name="Bateria Alcalina Aging")
        FunctionValue.objects.create(function=f, x=0, y=0.05)
        FunctionValue.objects.create(function=f, x=5, y=0.2)
        FunctionValue.objects.create(function=f, x=10, y=0.4)
        FunctionValue.objects.create(function=f, x=15, y=0.7)
        FunctionValue.objects.create(function=f, x=20, y=1)
        self.asset = Asset.objects.create(name="Bateria Alcalina Teste", fabrication_date=2000, technology=self.tec, aging_function = f)