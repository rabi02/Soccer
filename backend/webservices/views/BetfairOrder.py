import betfairlightweight
from betfairlightweight import filters
import requests
import json
import requests
import json
from db_table.models import *
from webservices.views.constants import *
from webservices.views.bitfairapi import *
from webservices.views.BitfairLib import *
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from webservices.serializers import *
import datetime
import re
from django.db.models import Q
import logging
import logging.handlers as handlers
import pandas as pd
import xlwt
# from webservices.views.constants import *

# # create trading instance
# trading = betfairlightweight.APIClient(BetUsername,BetPassword, app_key=ApplicationKey)

# # login
# trading.login_interactive()

# update for test
# market_id = "1.131347484"
# selection_id = 12029579


def place_order(market_id,selection_id,handicap,price,size,user_id,ApplicationKey,BetPassword,BetUsername,bookmaker_price,bookmaker_size):
    try:
        trading = betfairlightweight.APIClient(BetUsername,BetPassword, app_key=ApplicationKey, session=requests.Session())
        # login
        trading.login_interactive()
        # placing an order
       
        limit_order = filters.limit_order(size=size, price=price, persistence_type="LAPSE")
        # limit_order = filters.limit_order(size=2.00, price=1.01, persistence_type="LAPSE")
        instruction = filters.place_instruction(
            order_type="LIMIT",
            selection_id=selection_id,
            side="BACK",
            limit_order=limit_order,
        )
        place_orders = trading.betting.place_orders(
            market_id=market_id, 
            instructions=[instruction]  # list
        )

        for order in place_orders.place_instruction_reports:
            status=order.status
            bet_id = order.bet_id
            average_price_matched = order.average_price_matched
            placedDate =order.placed_date
            sizeMatched =order.size_matched

            # print(
            #     "Status: %s, BetId: %s, Average Price Matched: %s "
            #     % (order.status, order.bet_id, order.average_price_matched)
            # )
        resp = PlaceOrdersBetfair.objects.create(
            market_id=market_id,
            selection_id=selection_id,
            handicap=handicap,
            price=price ,
            size=size,
            bookmaker_price =price,
            bookmaker_size=size,
            user_id=user_id,
            status=status,
            bet_id=bet_id,
            average_price_matched=average_price_matched,
            placedDate=placedDate,
            sizeMatched =sizeMatched,
            placeorder_update_status=False
        )
        
        trading.logout()
        return(True)
    except :
        return (False)
def update_order(bet_id):
    # updating an order
    instruction = filters.update_instruction(
        bet_id=bet_id, new_persistence_type="PERSIST"
    )
    update_order = trading.betting.update_orders(
        market_id=market_id, instructions=[instruction]
    )

    print(update_order.status)
    for order in update_order.update_instruction_reports:
        print("Status: %s" % order.status)
def AutobetPlaceOrder(AutobetArr,user_id,ApplicationKey,BetPassword,BetUsername):
    
    try:
        handicap=0
        trading = betfairlightweight.APIClient(BetUsername,BetPassword, app_key=ApplicationKey, session=requests.Session())
        # login
        trading.login_interactive()
        # placing an order
        for autobet in AutobetArr:
            PriceFlag = False
            SizeFlag = False
            price=''
            size=''
            price_market_id = autobet['price_market_id']
            size_market_id= autobet['size_market_id']
            if price_market_id in  autobet:
                if autobet[price_market_id] !='':
                    PriceFlag =True
                    price = autobet[price_market_id]
            if size_market_id in  autobet:
                if autobet[size_market_id] !='':
                    SizeFlag =True
                    size = autobet[size_market_id]
            if size!='' and price!='':
                limit_order = filters.limit_order(size=size, price=price, persistence_type="LAPSE")
                # limit_order = filters.limit_order(size=2.00, price=1.01, persistence_type="LAPSE")
                instruction = filters.place_instruction(
                    order_type="LIMIT",
                    selection_id=autobet['selection_id'],
                    side="BACK",
                    limit_order=limit_order,
                )
                place_orders = trading.betting.place_orders(
                    market_id=autobet['market_id'], 
                    instructions=[instruction]  # list
                )

                for order in place_orders.place_instruction_reports:
                    status=order.status
                    bet_id = order.bet_id
                    average_price_matched = order.average_price_matched
                    placedDate =order.placed_date
                    sizeMatched =order.size_matched

                    print(
                        "Status: %s, BetId: %s, Average Price Matched: %s "
                        % (order.status, order.bet_id, order.average_price_matched)
                    )
                resp = PlaceOrdersBetfair.objects.create(
                    market_id=autobet['market_id'],
                    selection_id=autobet['selection_id'],
                    handicap=handicap,
                    price=price ,
                    size=size,
                    user_id=user_id,
                    status=status,
                    bet_id=bet_id,
                    bookmaker_price =price,
                    bookmaker_size=size,
                    average_price_matched=average_price_matched,
                    placedDate=placedDate,
                    sizeMatched =sizeMatched,
                    placeorder_update_status=False
                )
        
        trading.logout()
        return(True)
    except :
        return (False)


def replace_order(bet_id):
    # replacing an order
    instruction = filters.replace_instruction(bet_id=bet_id, new_price=1.10)
    replace_order = trading.betting.replace_orders(
        market_id=market_id, instructions=[instruction]
    )

    print(replace_order.status)
    for order in replace_order.replace_instruction_reports:
        place_report = order.place_instruction_reports
        cancel_report = order.cancel_instruction_reports
        print(
            "Status: %s, New BetId: %s, Average Price Matched: %s "
            % (order.status, place_report.bet_id, place_report.average_price_matched)
        )

def cancel_order(market_id,selection_id,size,user_id,ApplicationKey,BetPassword,BetUsername):
    try:
        trading = betfairlightweight.APIClient(BetUsername,BetPassword, app_key=ApplicationKey, session=requests.Session())
        # login
        trading.login_interactive()
        instruction = filters.cancel_instruction(bet_id=bet_id, size_reduction=2.00)
        cancel_order = trading.betting.cancel_orders(
            market_id=market_id, instructions=[instruction]
        )

        print(cancel_order.status)
        for cancel in cancel_order.cancel_instruction_reports:
            print(
                "Status: %s, Size Cancelled: %s, Cancelled Date: %s"
                % (cancel.status, cancel.size_cancelled, cancel.cancelled_date)
            )
        return(True)
    except :
        return (False)

def clearOrder(BetUsername,BetPassword,ApplicationKey):

    trading = betfairlightweight.APIClient(BetUsername,BetPassword, app_key=ApplicationKey, session=requests.Session())
    # login
    trading.login_interactive()
    data = PlaceOrdersBetfair.objects.all()
    for rec in data:
        market_id = rec.market_id
        bet_id = rec.bet_id
        cleared_orders = trading.betting.list_cleared_orders(market_ids=[market_id])
        for order in cleared_orders._data['clearedOrders']:
            UpdData = PlaceOrdersBetfair.objects.filter(market_id=market_id,bet_id=bet_id).update(
                persistenceType= order['persistenceType'],
                orderType= order['orderType'],
                side= order['side'],
                betOutcome= order['betOutcome'],
                settledDate= order['settledDate'],
                priceReduced= order['priceReduced'],
                profit = order['profit'],
                placeorder_update_status=True
            )
            # print(order)
            print(market_id,bet_id)

   
    trading.logout()
