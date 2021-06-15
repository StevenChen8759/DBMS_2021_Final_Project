from datetime import datetime

from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

from database.schema import StockTradingType, TaxInformation

str_to_list = lambda x: x.replace(" ", "").split(",")

def make_list(self):

    # Get AAID List
    sttid_text = self.lineEdit_stt_sttid.text()
    if sttid_text != "":
        sttid_list = str_to_list(sttid_text)
    else:
        sttid_list = []

    # Get UID List
    description_text = self.lineEdit_stt_description.text()
    if description_text != "":
        description_list = str_to_list(description_text)
    else:
        description_list = []

    # Get Name List
    feerate_text = self.lineEdit_stt_fee_rate.text()
    if feerate_text != "":
        feerate_list = str_to_list(feerate_text)
    else:
        feerate_list = []

    # Get Gender List
    feemin_text = self.lineEdit_stt_fee_min.text()
    if feemin_text != "":
        feemin_list = str_to_list(feemin_text)
    else:
        feemin_list = []

    return sttid_list, description_list, feerate_list, feemin_list

def select(session):
    # Tax Info subquery
    tax_query = session.query(TaxInformation).subquery()

    # Stock Trading Type subquery
    main_query = (
        session.query(
            StockTradingType.sttid,
            StockTradingType.type_name,
            StockTradingType.fee_rate,
            StockTradingType.fee_min,
            TaxInformation.taxinfoid,
            TaxInformation.tax_type,
            TaxInformation.rate,
        ).join(tax_query, tax_query.columns.taxinfoid == StockTradingType.taxinfoid)
        .order_by("sttid")
    )

    logger.debug(f"Equivalent SQL: {main_query}")

    return "OK", main_query.all()


def update(
    session,
    sttid_list,
    description_list,
    feerate_list,
    feemin_list,
):
    pass