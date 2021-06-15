from datetime import datetime

from sqlalchemy import Column, String, Integer, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()

# User Information
class UserInfo(base):
    __tablename__ = 'user_info'

    uid = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    joindate = Column(Date, default=datetime.now, nullable=False)


# Asset Account
class AssetAccount(base):
    __tablename__ = 'asset_account'

    aaid = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("user_info.uid"), nullable=False)
    name = Column(String, nullable=False)
    aatype = Column(String, nullable=False)
    currency = Column(String, nullable=False)

    user_info = relationship("UserInfo")


# General Accounting
class GeneralAccounting(base):
    __tablename__ = 'general_accounting'

    gaid = Column(Integer, primary_key=True)
    aaid = Column(Integer, ForeignKey("asset_account.aaid"), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
    shop_name = Column(String, nullable=True)
    price = Column(Float, nullable=False)

    asset_account = relationship("AssetAccount")


# Stock Accounting
class StockAccounting(base):
    __tablename__ = 'stock_accounting'

    said = Column(Integer, primary_key=True)
    aaid = Column(Integer, ForeignKey("asset_account.aaid"), nullable=False)  # For stock delivery (股票交割帳戶)
    stockid = Column(String, ForeignKey("stock_information.stockid"), nullable=False)
    trading_type_id = Column(Integer, ForeignKey('stock_trading_type.sttid'), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    stock_price = Column(Float, nullable=False)
    stock_volume = Column(Integer, nullable=False)

    asset_account = relationship("AssetAccount")
    stock_information = relationship("StockInformation")
    stock_trading_type = relationship("StockTradingType")


# Stock Informantion
class StockInformation(base):
    __tablename__ = 'stock_information'

    stockid = Column(String, primary_key=True)    # eg: 2330-TW(台積電), 6547-TW(高端疫苗), UMC-US(聯電ADR), TSM-US(台積電ADR)
    name = Column(String, nullable=False)         # 股票名稱
    currency = Column(String, nullable=False)     # 股價幣種 (e.g NTD, USD, RMB...等等)
    NDOpenPrice = Column(Float, nullable=False)   # 最近交易日開盤價
    NDHighPrice = Column(Float, nullable=False)   # 最近交易日盤中最高價
    NDLowPrice = Column(Float, nullable=False)    # 最近交易日盤中最低價
    NDClosePrice = Column(Float, nullable=False)  # 最近交易日收盤價
    NDVolume = Column(Integer, nullable=False)    # 最近交易日總成交量
    EPS_NQ_ACC = Column(Float, nullable=False)    # 最近一季累計 EPS
    EPS_NY_ACC = Column(Float, nullable=False)    # 最近一年累計 EPS
    DIV_NY_ACC = Column(Float, nullable=False)    # 最近一年累計總股利


# Stock Trading Type (Fitting 3rd Normalization Requirement)
class StockTradingType(base):
    __tablename__ = 'stock_trading_type'

    sttid = Column(Integer, primary_key=True)
    taxinfoid = Column(Integer, ForeignKey("tax_information.taxinfoid"), nullable=False) # 交易稅資訊 - 台股一般買/賣、台股 ETF 買/賣
    type_name = Column(String, nullable=False)   # 普買、普賣、零買、零賣、當沖買、當沖賣
    fee_rate = Column(Float, nullable=False)     # 手續費率
    fee_min = Column(Float, nullable=False)      # 最低手續費 (整股與現股當沖 = 20 元, 零股 = 1 元)


# Tax Information (Fitting 3rd Normalization Requirement)
class TaxInformation(base):
    __tablename__ = 'tax_information'

    taxinfoid = Column(Integer, primary_key=True)   # 交易稅率編號
    tax_type = Column(String, nullable=False)       # 交易類別 - 台股買進、台股一般賣、台股 ETF 買
    rate = Column(Float, nullable=False)            # 交易稅率值
