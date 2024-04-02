import fastapi
from loguru import logger

from alpaca.trading.models import Order

from trading_service import trade_service

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from dotenv import load_dotenv
load_dotenv()


app = fastapi.FastAPI()
FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/make_trade/buy")
async def post_make_trade_buy(
    market_order_request: trade_service.TradeRequest,
) -> Order:

    logger.info(market_order_request)
    market_order = trade_service.make_trade(
        market_order_request=market_order_request, side="buy"
    )
    # print(market_order)
    logger.info(
        f"trade_side:buy<<|>>id:{market_order.id}<<|>>client_order_id:{market_order.client_order_id}<<|>>created_at:{market_order.created_at}"
    )
    return market_order.model_dump()


@app.post("/make_trade/sell")
async def post_make_trade_sell(
    market_order_request: trade_service.TradeRequest,
) -> Order:

    logger.info(market_order_request)
    market_order = trade_service.make_trade(
        market_order_request=market_order_request, side="sell"
    )
    # print(market_order)
    logger.info(
        f"trade_side:sell<<|>>id:{market_order.id}<<|>>client_order_id:{market_order.client_order_id}<<|>>created_at:{market_order.created_at}"
    )
    return market_order.model_dump()
