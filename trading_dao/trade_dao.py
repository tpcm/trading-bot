from typing import Optional
from uuid import UUID
from datetime import datetime

import duckdb
import pydantic

from alpaca.trading.models import Order


class TradeDetails(pydantic.BaseModel):
    id: UUID
    client_order_id: str
    created_at: datetime
    updated_at: datetime
    submitted_at: datetime
    filled_at: datetime
    expired_at: Optional[datetime]
    canceled_at: Optional[datetime]
    failed_at: Optional[datetime]
    asset_id: UUID
    symbol: str
    asset_class: str
    notional: float
    qty: float
    filled_qty: float
    filled_avg_price: float
    order_class: str
    order_type: str
    type: str
    side: str
    time_in_force: str
    limit_price: Optional[float]
    stop_price: Optional[float]
    status: str
    extended_hours: bool
    trail_percent: Optional[float]
    trail_price: Optional[float]
    hwm: Optional[float]

class TradeDAO:

    def __init__(self, connection_path: duckdb.DuckDBPyConnection):
        self.conn = duckdb.connect(connection_path)
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS trade_details (
                id UUID PRIMARY KEY,
                client_order_id VARCHAR,
                created_at TIMESTAMP,
                updated_at TIMESTAMP,
                submitted_at TIMESTAMP,
                filled_at TIMESTAMP,
                expired_at TIMESTAMP,
                canceled_at TIMESTAMP,
                failed_at TIMESTAMP,
                asset_id UUID,
                symbol VARCHAR,
                asset_class VARCHAR,
                notional REAL,
                qty REAL,
                filled_qty REAL,
                filled_avg_price REAL,
                order_class VARCHAR,
                order_type VARCHAR,
                type VARCHAR,
                side VARCHAR,
                time_in_force VARCHAR,
                limit_price REAL,
                stop_price REAL,
                status VARCHAR,
                extended_hours BOOLEAN,
                trail_percent REAL,
                trail_price REAL,
                hwm REAL
            )
            """
        )

    def save_trade(self, trade_details: Order) -> None:
        trade_detail_dict = trade_details.model_dump()

        declared_fields = TradeDetails.__annotations__.keys()

        columns_to_include = [key for key in trade_detail_dict.keys() if key in declared_fields]
        values_to_include = [trade_detail_dict[key] for key in columns_to_include]
        columns_insert = ", ".join(columns_to_include)
        placeholders = ", ".join("?" * len(columns_to_include))

        insert_query = f"""
            INSERT INTO trade_details ({columns_insert})
            VALUES ({placeholders})
        """

        self.conn.execute(insert_query, values_to_include)
        
    def get_all_trades(self):
        return self.conn.execute("""SELECT * FROM trade_details""").fetchall()

    def get_trade_detail(self, id: int) -> Order:
        result = self.conn.execute("""
            SELECT * FROM trade_details WHERE id = ?
        """, (id,)).fetchone()
        return Order(**dict(result))