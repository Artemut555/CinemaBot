import typing as tp
from decimal import Decimal

import pytest
from sqlalchemy import select

from db_api.models.base import Session
from db_api.models import User
from db_api.core import add_user, add_movie, add_history, get_history
from db_api.models.base import clear_database, Session

clear_database()
# session = Session()
# add_user(4, session=session)
# add_movie("TESt", 2022, 4356, session=session)
# add_history(4, "lala", 4356, session=session)
# res = get_history(4, session=session)
# print(res)
# session.close()
