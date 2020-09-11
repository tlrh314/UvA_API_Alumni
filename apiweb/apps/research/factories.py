import factory
from faker import Factory

from apiweb.apps.research.models import Thesis

FAKER = Factory.create("nl_NL")
THESIS_TYPES = [item[0] for item in Thesis.THESIS_TYPE]


class ThesisFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Thesis

    type = THESIS_TYPES[FAKER.random_int(min=0, max=len(THESIS_TYPES) - 1)]

    title = factory.LazyAttribute(
        lambda _: "TestThesis: " + FAKER.sentence(nb_words=12)
    )
