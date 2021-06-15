
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from database import schema

# Operation for user information
def user_info_query(
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