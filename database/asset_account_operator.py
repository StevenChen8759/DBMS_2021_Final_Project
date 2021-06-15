from datetime import datetime

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from database.schema import AssetAccount

str_to_list = lambda x: x.replace(" ", "").split(",")

def make_list(self):

    # Get AAID List
    aaid_text = self.lineEdit_asset_aaid.text()
    if aaid_text != "":
        aaid_list = str_to_list(aaid_text)
    else:
        aaid_list = []

    # Get UID List
    uid_text = self.lineEdit_asset_uid.text()
    if uid_text != "":
        uid_list = str_to_list(uid_text)
    else:
        uid_list = []

    # Get Name List
    name_text = self.lineEdit_asset_name.text()
    if name_text != "":
        name_list = str_to_list(name_text)
    else:
        name_list = []

    # Get Gender List
    type_text = self.lineEdit_asset_type.text()
    if type_text != "":
        type_list = str_to_list(type_text)
    else:
        type_list = []

    # Get Birthday List
    currency_text = self.lineEdit_asset_currency.text()
    if currency_text != "":
        currency_list = str_to_list(currency_text)
    else:
        currency_list = []

    return aaid_list, uid_list, name_list, type_list, currency_list

def select(
    session,
    aaid_list,
    uid_list,
    name_list,
    type_list,
    currency_list,
):
    # Edit filter - Add query constriant (WHERE PART)
    filter_list = []

    if aaid_list != []:
        filter_list.append(
            AssetAccount.aaid.in_(aaid_list)
        )

    if uid_list != []:
        filter_list.append(
            AssetAccount.uid.in_(uid_list)
        )

    if name_list != []:
        filter_list.append(
            AssetAccount.name.in_(name_list)
        )

    if type_list != []:
        filter_list.append(
            AssetAccount.aatype.in_(type_list)
        )

    if currency_list != []:
        filter_list.append(
            AssetAccount.currency.in_(currency_list)
        )

    # Convert filter to tuple type
    filter_tuple = tuple(filter_list)

    # Prepare Query Statement and print out
    try:
        qstat = session.query(AssetAccount).filter(*filter_tuple).order_by("uid", "aaid")
        logger.debug(f"Equivalent SQL: {qstat}")
    except SQLAlchemyError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, None

    # Execute Query
    try:
        result = qstat.all()
        return "OK", result
    except SQLAlchemyError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, None

def insert(
    session,
    aaid_list,
    uid_list,
    name_list,
    type_list,
    currency_list,
):
    # Check length of data to insert
    if len(aaid_list) != 1 or len(uid_list) != 1 or len(name_list) != 1 or len(type_list) != 1 or len(currency_list) != 1:
        logger.warning("Error: All insert data attribute should be equel to 1")
        return "Error: at least one insert data attribute should be equel to 1", True

    try:
        asset_account = AssetAccount(
            aaid = aaid_list[0],
            uid = uid_list[0],
            name = name_list[0],
            aatype = type_list[0],
            currency = currency_list[0]
        )
    except ValueError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, True

    try:
        session.add(asset_account)
    except SQLAlchemyError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, True

    try:
        session.commit()
        return "OK", False
    except SQLAlchemyError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, True

def update(
    session,
    aaid_list,
    uid_list,
    name_list,
    type_list,
    currency_list,
):
    # Check length of data to update
    if len(aaid_list) != 1:
        logger.warning("Error: UID count must be 1")
        return "Error: UID count must be 1", True

    if len(name_list) == 0 and len(type_list) == 0 and len(currency_list) == 0:
        logger.warning("Error: at least insert data attribute should be equel to 1")
        return "Error: at least insert data attribute should be equel to 1", True

    if len(name_list) > 1 or len(type_list) > 1 or len(currency_list) > 1:
        logger.warning("Error: Length of insert data attribute should be less than or equel to 1")
        return "Error: Length of all insert data attribute should be be less than or equal to 1", True

    try:
        update_map = {}

        asset_account_id = aaid_list[0]

        if len(name_list) > 0:
            update_map["name"] = name_list[0]

        if len(type_list) > 0:
            update_map["aatype"] = type_list[0]

        if len(currency_list) > 0:
            update_map["currency"] = currency_list[0]
    except ValueError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, True

    try:
        update_query = (
            session.query(AssetAccount)
                   .filter(AssetAccount.aaid == asset_account_id)
                   .update(update_map)
        )
    except SQLAlchemyError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, True

    try:
        session.commit()
        return "OK", False
    except SQLAlchemyError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, True
