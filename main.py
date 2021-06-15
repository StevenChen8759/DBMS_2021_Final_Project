import sys
from typing import List

from PyQt5 import QtCore, uic
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt5.QtWidgets import QApplication, QMainWindow
from loguru import logger

from database import (
    psql_session,
    user_info_operator,
    schema,
)

class QueryResultTable(QAbstractTableModel):

    data_schema = None
    data_list = None

    def __init__(self, parent, table_schema, table_data, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.data_schema = table_schema
        self.data_list = table_data

    def rowCount(self, parent):
        return len(self.data_list)

    def columnCount(self, parent):
        return len(self.data_schema)

    def data(self, index, role):
        if not index.isValid():
            return None
        if (role == Qt.DisplayRole):
            return self.data_list[index.row()][index.column()]
        else:
            return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.data_schema[col]
        return None

    def update_data(self, parent, schema, data):

        # Update Data
        self.data_schema = schema
        self.data_list = data

        # Refresh Screen Trigger
        self.layoutChanged.emit()

class StockDBMS_GUI(QMainWindow):

    # Declare GUI Attribute
    psql_session = None      # PostgreSQL session
    output_data_model = None

    def __init__(self):
        super(StockDBMS_GUI, self).__init__() # Call the inherited classes __init__ method
        logger.info("Load GUI")
        uic.loadUi('accounting.ui', self) # Load the .ui file

        # Add Button Callback - User Information
        self.pushButton_userinfo_select.clicked.connect(self.__userinfo_select)
        self.pushButton_userinfo_insert.clicked.connect(self.__userinfo_insert)
        self.pushButton_userinfo_update.clicked.connect(self.__userinfo_update)

        # Add Button Callback - Asset Account
        self.pushButton_asset_select.clicked.connect(self.__asset_select)
        self.pushButton_asset_insert.clicked.connect(self.__asset_insert)
        self.pushButton_asset_update.clicked.connect(self.__asset_update)
        self.pushButton_asset_general_balance_eval.clicked.connect(self.__asset_general_account_balance_eval)
        self.pushButton_asset_stock_balance_eval.clicked.connect(self.__asset_stock_account_value_eval)

        # Add Button Callback - Stock Trading Type
        self.pushButton_stt_select.clicked.connect(self.__stt_trading_type_select)
        self.pushButton_stt_update_by_sttid.clicked.connect(self.__stt_trading_type_update)
        self.pushButton_stt_tax_update_by_taxid.clicked.connect(self.__stt_tax_info_update)

        # Add Button Callback - General Accounting
        self.pushButton_ga_select.clicked.connect(self.__ga_select)
        self.pushButton_ga_insert.clicked.connect(self.__ga_insert)
        self.pushButton_ga_update.clicked.connect(self.__ga_update)
        self.pushButton_ga_delete_by_gaid.clicked.connect(self.__ga_delete_by_gaid)
        self.pushButton_ga_cost_eval_by_type.clicked.connect(self.__ga_eval_cost_by_type)
        self.pushButton_ga_cost_eval_by_shop.clicked.connect(self.__ga_eval_cost_by_shop)
        self.pushButton_ga_cost_eval_by_aaid.clicked.connect(self.__ga_eval_cost_by_aaid)

        # Add Button Callback - Stock Accounting
        self.pushButton_sa_select.clicked.connect(self.__sa_select)
        self.pushButton_sa_insert.clicked.connect(self.__sa_insert)
        self.pushButton_sa_update.clicked.connect(self.__sa_update)
        self.pushButton_sa_delete_by_said.clicked.connect(self.__sa_delete_by_said)
        self.pushButton_sa_eval_holding_by_aaid.clicked.connect(self.__sa_eval_holding_value_by_aaid)
        self.pushButton_sa_eval_curr_val_by_said_stockid.clicked.connect(self.__sa_eval_stock_by_aaid_and_stockid)
        self.pushButton_sa_eval_real_profit_by_aaid.clicked.connect(self.__sa_eval_real_profit_by_aaid)

        # Add Button Callback - Stock Information
        self.pushButton_si_select.clicked.connect(self.__si_select)
        self.pushButton_si_insert.clicked.connect(self.__si_insert)
        self.pushButton_si_update.clicked.connect(self.__si_update)
        self.pushButton_si_delete_by_stockid.clicked.connect(self.__si_delete_by_stockid)

        # Add Button Callback - Direct SQL Input
        self.pushButton_run_sql_query.clicked.connect(self.__run_input_sql_query)

        # Add default data list
        self.output_data_model = QueryResultTable(
            self,
            ["Class", "Name", "Student ID"],
            [["AI學程碩一", "陳順祥", "NE6091051"]]
        )

        # Set Data Output List Default Value
        self.tableView_data_output.setModel(self.output_data_model)

        # UI operation
        logger.info("Configure and show GUI")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
        self.show() # Show the GUI


    def closeEvent(self, event):
        # Bypass Class QMainWindow Close Event
        logger.info("Close GUI")
        QMainWindow.closeEvent(self, event)


    def output_query_result(self, data_schema, data_raw):
        self.output_data_model.update_data(self, data_schema, data_raw)


    def output_session_response(self, resp_text, is_error):
        if is_error:
            self.textBrowser.setTextColor(
                QColor("white")
            )
            self.textBrowser.setTextBackgroundColor(
                QColor("red")
            )
        else:
            self.textBrowser.setTextColor(
                QColor("black")
            )
            self.textBrowser.setTextBackgroundColor(
                QColor("lime")
            )
        self.textBrowser.reload()
        self.textBrowser.setText(resp_text)


    def openSession(self):
        # Connect PostgreSQL Session
        logger.info("Connect to PostgreSQL session on the server")
        self.psql_session = psql_session.connect()
        logger.success("PostgreSQL session is connected now...")


    def closeSession(self):
        # StockDBMS_GUI QMainWindow Close Event
        logger.info("Disconnect PostgreSQL Session")
        psql_session.disconnect(self.psql_session)
        logger.success("PostgreSQL session is disconnected now...")

#--------------------------------------------------------------------------------------------------
# User Information Button

    def __userinfo_select(self):
        # Open Session
        self.openSession()

        # Make User Information
        uid_list, name_list, gender_list, birthday_list = user_info_operator.user_info_make_list(self)
        logger.debug(f"Parameter Length -> UID: {len(uid_list)}, Name: {len(name_list)}, Gender: {len(gender_list)}, Birthday: {len(birthday_list)}")

        qresp, result = user_info_operator.user_info_select(
            self.psql_session,
            uid_list,
            name_list,
            gender_list,
            birthday_list,
        )

        # Check Query Result
        if result is not None:

            # Success, Make list for table view
            data_schema = ["uid", "name", "gender", "birthdate", "joindate"]
            data_list = [
                [raw.uid,
                 raw.name,
                 raw.gender,
                 raw.birthdate.isoformat(),
                 raw.joindate.isoformat()
                 ] for raw in result
            ]

            # Output Final Result
            self.output_query_result(data_schema, data_list)
            self.output_session_response(qresp, False)

        else:
            self.output_session_response(f"Query Failed: {qresp}", True)

        self.closeSession()


    def __userinfo_insert(self):
        self.openSession()

        uid_list, name_list, gender_list, birthday_list = user_info_operator.user_info_make_list(self)
        logger.debug(f"Parameter Length -> UID: {len(uid_list)}, Name: {len(name_list)}, Gender: {len(gender_list)}, Birthday: {len(birthday_list)}")

        qresp, is_error = user_info_operator.user_info_insert(
            self.psql_session,
            uid_list,
            name_list,
            gender_list,
            birthday_list,
        )

        self.output_session_response(qresp, is_error)

        self.closeSession()


    def __userinfo_update(self):
        self.openSession()

        uid_list, name_list, gender_list, birthday_list = user_info_operator.user_info_make_list(self)
        logger.debug(f"Parameter Length -> UID: {len(uid_list)}, Name: {len(name_list)}, Gender: {len(gender_list)}, Birthday: {len(birthday_list)}")

        qresp, is_error = user_info_operator.user_info_insert(
            self.psql_session,
            uid_list,
            name_list,
            gender_list,
            birthday_list,
        )

        self.output_session_response(qresp, is_error)

        self.closeSession()

#--------------------------------------------------------------------------------------------------
# Asset Account Button

    def __asset_select(self):
        logger.info("Select Asset Account Information")

    def __asset_insert(self):
        logger.info("Insert Asset Account Information")

    def __asset_update(self):
        logger.info("Update Asset Account Information")

    def __asset_general_account_balance_eval(self):
        logger.info("General Account Balance Evaluation")

    def __asset_stock_account_value_eval(self):
        logger.info("Stock Account Balance Evaluation")

#--------------------------------------------------------------------------------------------------
# Stock Trading Type

    def __stt_trading_type_select(self):
        logger.info("Select Trading Type Information")

    def __stt_trading_type_update(self):
        logger.info("Update Trading Type Information")

    def __stt_tax_info_update(self):
        logger.info("Update Tax Information")

#--------------------------------------------------------------------------------------------------
# General Accounting

    def __ga_select(self):
        logger.info("Select General Accounting")

    def __ga_insert(self):
        logger.info("Insert General Accounting")

    def __ga_update(self):
        logger.info("Update General Accounting")

    def __ga_delete_by_gaid(self):
        logger.info("Delete General Accounting by GAID")

    def __ga_eval_cost_by_type(self):
        logger.info("Evaluate Cost by Type of Accounting")

    def __ga_eval_cost_by_shop(self):
        logger.info("Evaluate Cost by Shop of Accounting")

    def __ga_eval_cost_by_aaid(self):
        logger.info("Evaluate Cost by AAID of Accounting")

#--------------------------------------------------------------------------------------------------
# Stock Accounting

    def __sa_select(self):
        logger.info("Select Stock Accounting")

    def __sa_insert(self):
        logger.info("Insert Stock Accounting")

    def __sa_update(self):
        logger.info("Update Stock Accounting")

    def __sa_delete_by_said(self):
        logger.info("Delete Stock Accounting by SAID")

    def __sa_eval_holding_value_by_aaid(self):
        logger.info("Evaluate Current Holding Stock by AAID")

    def __sa_eval_stock_by_aaid_and_stockid(self):
        logger.info("Evaluate Holding Stock Current Value by AAID and Stock ID")

    def __sa_eval_real_profit_by_aaid(self):
        logger.info("Evaluate Really Implemented Stock Profit by AAID")

#--------------------------------------------------------------------------------------------------
# Stock Information

    def __si_select(self):
        logger.info("Select Stock Information")

    def __si_insert(self):
        logger.info("Insert Stock Information")

    def __si_update(self):
        logger.info("Update Stock Information")

    def __si_delete_by_stockid(self):
        logger.info("Delete Stock Information")

#--------------------------------------------------------------------------------------------------
# Directly SQL Query Input

    def __run_input_sql_query(self):
        logger.info("Run Directly Input SQL Query")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockDBMS_GUI()
    window.show()
    sys.exit(app.exec_())
