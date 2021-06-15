from datetime import datetime

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from database import schema

str_to_list = lambda x: x.replace(" ", "").split(",")

def user_info_make_list(self):
    # Get UID List
    uid_text = self.lineEdit_userinfo_uid.text()
    if uid_text != "":
        uid_list = str_to_list(uid_text)
    else:
        uid_list = []

    # Get Name List
    name_text = self.lineEdit_userinfo_name.text()
    if name_text != "":
        name_list = str_to_list(name_text)
    else:
        name_list = []

    # Get Gender List
    gender_text = self.lineEdit_userinfo_gender.text()
    if gender_text != "":
        gender_list = str_to_list(gender_text)
    else:
        gender_list = []

    # Get Birthday List
    birthday_text = self.lineEdit_userinfo_birthday.text()
    if birthday_text != "":
        birthday_list = str_to_list(birthday_text)
    else:
        birthday_list = []

    return uid_list, name_list, gender_list, birthday_list

# Operation for user information
def user_info_select(
    session,
    uid_list,
    name_list,
    gender_list,
    birthday_list
):

    # Edit filter - Add query constriant (WHERE PART)
    filter_list = []

    if uid_list != []:
        filter_list.append(
            schema.UserInfo.uid.in_(uid_list)
        )

    if name_list != []:
        filter_list.append(
            schema.UserInfo.name.in_(name_list)
        )

    if gender_list != []:
        filter_list.append(
            schema.UserInfo.gender.in_(gender_list)
        )

    # Convert filter to tuple type
    filter_tuple = tuple(filter_list)

    # Prepare Query Statement and print out
    try:
        qstat = session.query(schema.UserInfo).filter(*filter_tuple).order_by("uid")
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

# Operation for user information
def user_info_insert(
    session,
    uid_list,
    name_list,
    gender_list,
    birthday_list
):
    # Check length of data to insert
    if len(uid_list) != 1:
        logger.warning("Error: UID count must be 1")
        return "Error: UID count must be 1", True

    if len(name_list) == 0 and len(gender_list) == 0 and len(birthday_list) == 0:
        logger.warning("Error: at least insert data attribute should be equel to 1")
        return "Error: at least insert data attribute should be equel to 1", True

    if len(name_list) > 1 or len(gender_list) > 1 or len(birthday_list) > 1:
        logger.warning("Error: Length of insert data attribute should be less than or equel to 1")
        return "Error: Length of all insert data attribute should be be less than or equal to 1", True


    try:
        update_map = {}

        user_id = uid_list[0]

        if len(name_list) > 0:
            update_map["name"] = name_list[0]

        if len(gender_list) > 0:
            update_map["gender"] = gender_list[0]

        if len(birthday_list) > 0:
            update_map["birthdate"] = datetime.fromisoformat(birthday_list[0])

    except ValueError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, True

    try:
        update_query = (
            session.query(schema.UserInfo)
                   .filter(schema.UserInfo.uid == user_id)
                   .update(update_map)
        )
    except SQLAlchemyError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, True

    try:
        session.commit()
    except SQLAlchemyError as e:
        error_msg = f"<{type(e).__name__}> {str(e)}"
        return error_msg, True

    return "OK", False