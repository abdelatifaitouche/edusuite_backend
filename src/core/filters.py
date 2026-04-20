from enum import StrEnum
from sqlalchemy.sql import Select


class Order(StrEnum):
    ASC = "ASC"
    DESC = "DESC"


class BaseFilters:
    def __init__(self, order: Order = Order.ASC):
        self.order: Order = order

    def apply_filters(self, stmt: Select) -> Select:

        if self.order == Order.ASC:
            stmt = stmt.order_by("-created_at")
        else:
            stmt = stmt.order_by("created_at")

        return stmt
