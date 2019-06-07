from logging import getLogger
from random import randrange
from typing import Dict

from eth_account import Account
import factory
from faker import Faker
from faker.providers import internet

from ..models import Country, User
from ..utils import country_iso_codes


logger = getLogger(__name__)
faker = Faker()
faker.add_provider(internet)


class CountryFactory(factory.DjangoModelFactory):
    class Meta:
        model = Country

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        obj = model_class(*args, **kwargs)
        country_iso_code = country_iso_codes[randrange(0, len(country_iso_codes))]
        obj.name = country_iso_code[1]
        obj.iso2 = country_iso_code[0]
        obj.iso3 = country_iso_code[2]
        obj.is_enabled = True
        obj.numeric = country_iso_code[3]
        obj.save()
        return obj


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    cra = faker.random.randrange(0, 10)
    ethereum_address = factory.LazyFunction(lambda: Account.create().address)
    email = faker.safe_email()
    is_source_of_funds_verified = False
    lastname = faker.name()  # surname() or lastname() doesn't exist
    name = faker.name()
    status = faker.random.randrange(0, 5)
    country = factory.SubFactory(CountryFactory)


def get_mocked_signup_data(**kwargs) -> Dict:
    """

    :param kwargs: optional dictionary that overrides/adds extra data
    :return: mocked data
    """
    country_iso_code = country_iso_codes[randrange(0, len(country_iso_codes))]
    mock_data = {
        'email': faker.safe_email(),
        'name': faker.name(),
        'lastname': faker.name(),
        'country': country_iso_code[2]
    }
    # Provide extra data or override default ones
    mock_data.update(kwargs)
    return mock_data
