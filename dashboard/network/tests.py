from django.test import TestCase
from models.Asset import Asset
from algorithms.models.AssetType import AssetType, Technology
from algorithms.models.Parameter import Parameter, ValueCorrespondence
from utils.models import RegressionFunction, FunctionValue
# Create your tests here.


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

    def test_asset_creation(self):
        asset = Asset.objects.get()
        assettype = AssetType.objects.get()
        tec = Technology.objects.get()
        self.assertEqual(asset, self.asset)

    def test_probability_calculation(self):
        from collections import namedtuple
        MockFault = namedtuple('MockFault', 'failure_probability')
        a = MockFault(failure_probability=7.13)
        b = MockFault(failure_probability=8.13)
        c = MockFault(failure_probability=14.13)
        probabilities = []
        probabilities.append(a)
        self.assertEqual(self.asset.get_asset_failure_probability(probabilities), 0.071)
        probabilities.append(b)
        self.assertEqual(self.asset.get_asset_failure_probability(probabilities), 0.147)
        probabilities.append(c)
        self.assertEqual(self.asset.get_asset_failure_probability(probabilities), 0.267)