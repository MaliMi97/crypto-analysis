from datetime import datetime
from datetime import timedelta
from datetime import date
import pandas as pd
import numpy as np
from . import API

class CoinGeckoAPI(API.API):
    '''
    Class that connects to the API of https://www.coingecko.com/
    '''
    base_api_path = "https://api.coingecko.com/api/v3/"
    def __init__(self, time_out=60, sleep=5, good_result = [200]):
        super().__init__(time_out, sleep, good_result)
    
    def from_timestamp(self, stamp):
        aux = datetime.fromtimestamp(stamp/1000)
        return datetime(year=aux.year, month=aux.month, day=aux.day)

    def is_sunday(self, day):
        return date.weekday(day) == 6

    def next_sunday(self, _day):
        return datetime(year=_day.year, month=_day.month, day=_day.day) + timedelta(days = 6 - date.weekday(_day))

    def endpoint_price_market_cap_volume(self, date_time_from, date_time_to, coin="bitcoin"):
        '''
        Endpoclosing_priceint for price, market cap and trading volume between date_time_from and date_time_to for a coin (default is bitcoin).
        The data can be by hours or days depending on how much data we ask for and when were the data collected.
        '''
        return f"{self.base_api_path}coins/{coin}/market_chart/range?vs_currency=usd&from={self.unit_timestamp(date_time_from)}&to={self.unit_timestamp(date_time_to)}"
    
    def get_price_cap_volume(self, _date_time_from, _date_time_to, period='day', coin="bitcoin"):
        '''
        Returns a dataframe containing dates and either daily or weekly closing prices. For daily, set period to day. For weekly, set it to week.
        The time frame is from _date_time_from to _date_time_to, where _date_time_to is exclusive.
        '''
        if _date_time_from > _date_time_to:
            raise Exception("_date_time_to is bigger than _date_time_from")
        if period == 'day':
            date_time_from = datetime(year=_date_time_from.year, month=_date_time_from.month, day=_date_time_from.day)
            date_time_to = datetime(year=_date_time_to.year, month=_date_time_to.month, day=_date_time_to.day)
        elif period == 'week':
            date_time_from = self.next_sunday(_date_time_from) + timedelta(days = 1)
            date_time_to = self.next_sunday(_date_time_to)
            if date_time_from > date_time_to:
                raise Exception("the first monday is farther than the last sunday")
        else:
            raise Exception("The only viable periods are day and week")
        response = self.get_response(self.endpoint_price_market_cap_volume(date_time_from, date_time_to, coin))
        prices = np.array(response['prices'])
        df = pd.DataFrame(columns=['time','price', 'market cap', 'volume in $'])
        df[['time','price']] = prices
        df['time'] = df['time'].apply(self.from_timestamp)
        df['market cap'] = np.array(response['market_caps']).T[1]
        df['volume in $'] = np.array(response['total_volumes']).T[1]
        df = df[::-1]
        df = df.drop_duplicates('time')
        df = df[::-1]
        df = df.reset_index().drop('index', axis=1)
        if period == 'week':
            volume = [np.sum(df['volume in $'][i-6:i+1]) for i in np.arange(6,len(df),7)]
            df = df[df['time'].apply(self.is_sunday)]
            df['volume in $'] = volume
            df = df.reset_index().drop('index', axis=1)
        df['volume'] = df['volume in $']/df['price']
        return df