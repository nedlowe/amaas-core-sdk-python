from __future__ import absolute_import, division, print_function, unicode_literals

from amaascore.transactions.cash_transaction import CashTransaction
from amaascore.transactions.enums import CASH_TRANSACTION_TYPES
from amaascore.transactions.position import Position
from amaascore.transactions.transaction import Transaction

import inspect

def json_to_position(json_position):
    position = Position(**json_position)
    return position


def json_to_transaction(json_transaction):
    # Iterate through the Transaction children, converting the various JSON attributes into the relevant class type
    for (collection_name, clazz) in Transaction.children().items():
        children = json_transaction.pop(collection_name, {})
        collection = {}
        for (child_type, child_json) in children.items():
            # Handle the case where there are multiple children for a given type - e.g. links
            if isinstance(child_json, list):
                child = set()
                for child_json_in_list in child_json:
                    child.add(clazz(**child_json_in_list))
            else:
                child = clazz(**child_json)
            collection[child_type] = child
        json_transaction[collection_name] = collection
    transaction_type = json_transaction.get('transaction_type')
    clazz = CashTransaction if transaction_type in CASH_TRANSACTION_TYPES else Transaction
    args = inspect.getargspec(clazz.__init__)
    # Some fields are always added in, even though they're not explicitly part of the constructor
    clazz_args = args.args + clazz.amaas_model_attributes()
    # is not None is important so it includes zeros and False
    constructor_dict = {arg: json_transaction.get(arg) for arg in clazz_args
                        if json_transaction.get(arg) is not None and arg != 'self'}
    transaction = clazz(**constructor_dict)
    return transaction
