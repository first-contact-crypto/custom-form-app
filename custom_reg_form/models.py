from time import sleep
import logging
from django.conf import settings
from django.db import models
from badges.models import BadgeClass
from badges.models import BadgeAssertion
from badges.backends.badgr import BadgrBackend


LOGGER = logging.getLogger(__name__)

# Backwards compatible settings.AUTH_USER_MODEL
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


PROMO_CODES = [
    'FREECRYPTO'
]

NUM_EPIPH_AWARDED = 10




class ExtraInfo(models.Model):
    """
    This model contains an extra field that will be saved when a user registers.
    The form that wraps this model is in the forms.py file.
    """
    user = models.OneToOneField(USER_MODEL, null=True)
    promo_code = models.CharField(verbose_name="Promo Code", max_length=25, blank=True, null=True)

    def __str__(self):
        return self.promo_code

    def save(self, force_insert=False, force_update=False):
        if self.promo_code:
            self.promo_code = self.promo_code.strip().upper()
            self._validate_promo_code(self.promo_code)
            super(ExtraInfo, self).save(force_insert, force_update)

    def _validate_promo_code(self, value):
        LOGGER.info("In ExtraInfo::_validate_promo_code.. the value is {}".format(value))
        value = value.upper()
        if value in PROMO_CODES:
            bc = BadgeClass.objects.get(badgr_server_slug='CM-sak0wQuCty2BfSEle3A')
            be = BadgrBackend()
            for i in range(NUM_EPIPH_AWARDED):
                be.award(bc, self.user)
                if i < NUM_EPIPH_AWARDED:
                    sleep(10 / 1000)
