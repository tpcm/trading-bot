import os
from typing import Dict, Any
import fastapi
import pydantic
import pandas as pd
import json
from loguru import logger
from dotenv import load_dotenv

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, OrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce, OrderType
from alpaca.trading.models import Order

from opentelemetry.trace import get_tracer

from trading_dao import trade_dao


load_dotenv()

# app = fastapi.FastAPI()


class TradeRequest(pydantic.BaseModel):
    ticker: str
    notional: float
    time_in_force: str

    @pydantic.validator("ticker", pre=True)
    def make_ticker_upper(cls, v: str):
        return v.upper()


def make_trade(market_order_request: TradeRequest, side: str) -> Order:

    market_order_request = market_order_request.model_dump()
    # paper=True enables paper trading
    trading_client = TradingClient(
        api_key=os.getenv("ALPACA_KEY"),
        secret_key=os.getenv("ALPACA_SECRET"),
        paper=True,
    )

    market_order_data = MarketOrderRequest(
        symbol=market_order_request["ticker"],
        notional=market_order_request["notional"],
        side=side,
        time_in_force=market_order_request["time_in_force"],
    )

    # Market order
    market_order = trading_client.submit_order(
        order_data=market_order_data,
    )

    trade_db = trade_dao.TradeDAO(connection_path='./trades_db/trades_db.db')
    trade_db.save_trade(trade_details=market_order)

    return market_order



# @app.post("/make_trade/buy")
# async def post_make_trade_buy(market_order_request: TradeRequest) -> Order:

#     logger.info(market_order_request)
#     market_order = make_trade(
#         market_order_request=market_order_request, side="buy"
#     )
#     # print(market_order)
#     logger.info(
#         f"trade_side:buy<<|>>id:{market_order.id}<<|>>client_order_id:{market_order.client_order_id}<<|>>created_at:{market_order.created_at}"
#     )
#     return market_order.model_dump()


# @app.post("/make_trade/sell")
# async def post_make_trade_sell(market_order_request: TradeRequest) -> Order:

#     logger.info(market_order_request)
#     market_order = make_trade(
#         market_order_request=market_order_request, side="sell"
#     )
#     # print(market_order)
#     logger.info(
#         f"trade_side:sell<<|>>id:{market_order.id}<<|>>client_order_id:{market_order.client_order_id}<<|>>created_at:{market_order.created_at}"
#     )
#     return market_order.model_dump()


# if __name__ == "__main__":

#     # paper=True enables paper trading
#     trading_client = TradingClient(
#         api_key=os.getenv("ALPACA_KEY"), secret_key=os.getenv("ALPACA_SECRET"), paper=True
#     )

#     market_order_data = MarketOrderRequest(
#         symbol="SPY", notional=10, side=OrderSide.BUY, time_in_force=TimeInForce.DAY
#     )

#     # Market order
#     market_order = trading_client.submit_order(
#         order_data=market_order_data,
#     )

#     print(market_order)
