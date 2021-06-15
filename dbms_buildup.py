from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from database.schema import UserInfo, AssetAccount, base, StockInformation

db = create_engine(db_string)

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)



# Create
# user_info = UserInfo(uid=1,
#                        name="Steven HH CHen",
#                        gender="M",
#                        birthdate=datetime.fromisoformat("1997-08-15"),
#                        )
# session.add(user_info)
# session.commit()

# Read
users = session.query(UserInfo)
for user in users:
    print(user.uid, user.name, user.gender, user.birthdate, user.joindate)

    # if user.uid == 1:
    #     # Update
    #     user.name = "Steven Hsun Hsiang Chen"
    #     session.commit()

print("--------------------------------------------------")

# asset_account = AssetAccount(
#     aaid = 0,
#     uid = 1,
#     name = "Carry-on Cash",
#     aatype = "Cash",
#     currency = "NTD"
# )
# session.add(asset_account)
# session.commit()

asaccs = session.query(AssetAccount)
for asacc in asaccs:
    print(asacc.aaid, asacc.uid, asacc.name, asacc.aatype, asacc.currency)

tests = session.query(StockInformation)
