from __future__ import absolute_import, division, print_function, unicode_literals

from dateutil.parser import parse
import sys

from amaascore.assets.asset import Asset

# This extremely ugly hack is due to the whole Python 2 vs 3 debacle.
type_check = str if sys.version_info >= (3, 0, 0) else (str, unicode)


class ForeignExchangeBase(Asset):
    """ This class should never be instantiated """

    def __init__(self, asset_id, asset_status, description, major, country_codes, display_name=None,
                 asset_manager_id=0, *args, **kwargs):
        self.asset_class = 'ForeignExchange'
        self.country_codes = country_codes
        self.major = major
        super(ForeignExchangeBase, self).__init__(asset_manager_id=asset_manager_id, asset_id=asset_id, fungible=True,
                                                  display_name=display_name or asset_id, roll_price=False,
                                                  asset_status=asset_status, description=description,
                                                  *args, **kwargs)

    def base_currency(self):
        return self.asset_id[0:3]

    def counter_currency(self):
        return self.asset_id[3:6]

    def get_country_codes(self):
        return self.country_codes

    def get_currencies(self):
        return [self.base_currency(), self.counter_currency()]

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, major):
        """

        :param major:
        :return:
        """
        if major:
            self._major = major
        else:
            self._major = False

    @property
    def country_codes(self):
        return self._country_codes

    @country_codes.setter
    def country_codes(self, country_codes):
        """

        :param country_codes:
        :return:
        """
        self._country_codes = country_codes

class ForeignExchange(ForeignExchangeBase):
    """
    A spot FX transaction.
    """
    def __init__(self, asset_id, asset_status='Active', country_codes=[], major=False, description='', *args, **kwargs):
        super(ForeignExchange, self).__init__(asset_id=asset_id, asset_status=asset_status, description=description,
                                              country_codes=country_codes, major=major,
                                              *args, **kwargs)


class ForeignExchangeForward(ForeignExchangeBase):
    """
    A forward-dated FX transaction.  If there is a fixing_date, it is an NDF.
    """

    def __init__(self, asset_id, asset_status='Active', description='', major=False, country_codes=[],
                 forward_rate=None, underlying=None, settlement_date=None, fixing_date=None,
                 display_name=None, *args, **kwargs):
        self.forward_rate = forward_rate
        self.underlying = underlying
        self.settlement_date = settlement_date
        self.fixing_date = fixing_date
        super(ForeignExchangeForward, self).__init__(asset_id=asset_id, asset_status=asset_status,
                                                     country_codes=country_codes, display_name=display_name,
                                                     major=major, description=description, *args, **kwargs)

    @property
    def fixing_date(self):
        return self._fixing_date

    @fixing_date.setter
    def fixing_date(self, fixing_date):
        self._fixing_date = parse(fixing_date).date() if isinstance(fixing_date, type_check) \
            else fixing_date

    @property
    def settlement_date(self):
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self, settlement_date):
        self._settlement_date = parse(settlement_date).date() if isinstance(settlement_date, type_check) \
            else settlement_date
        