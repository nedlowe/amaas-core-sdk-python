import datetime
import uuid

from amaascore.core.amaas_model import AMaaSModel


class Book(AMaaSModel):
    """
    TODO - does this derive from anything?  Sort of depends on whether or not we are planning on storing it.
    """

    @staticmethod
    def non_interface_attributes():
        return ['positions']

    def __init__(self, asset_manager_id, book_id=None, book_status='Active', owner_id=None, close_time=None,
                 timezone='UTC', description='', positions=None, *args, **kwargs):
        self.asset_manager_id = asset_manager_id
        self.book_id = book_id or uuid.uuid4().hex
        self.book_status = book_status
        self.owner_id = owner_id
        self.close_time = close_time or datetime.timedelta(hours=18)
        self.timezone = timezone
        self.description = description
        self.positions = positions
        super(Book, self).__init__(*args, **kwargs)

    def positions_by_asset(self):
        """
        A dictionary of Position objects keyed by asset_id.  If an asset position exists in more than one book, they
         are combined into a single position.
        :return:
        """
        return {position.asset_id: position for position in self.positions}
