import time
import requests

class API:
    '''
    This is a parent class which takes care of making requests to APIs and receiving their response
    No endpoints are defined here. Each subclass has specific ones.
    '''

    def __init__(self, time_out, sleep, good_result):
        '''
        sleep is time in seconds between the repetitions of the same request. Sometimes, the request can fail due to the limit set by the website.
        The class will keep making the same request unless it gets a valid response or the time_out time is reached
        good_result is list of valid responses (integers)
        '''
        self.time_out = time_out
        self.sleep = sleep
        self.good_result = good_result
        
    def change_param(self, time_out, sleep):
        '''
        Changes time_out and sleep parameters
        '''
        self.time_out = time_out
        self.sleep = sleep 
    
    def unit_timestamp(self, date_time):
        '''
        Converts timestamp to datetime
        '''
        return time.mktime(date_time.timetuple())

    def make_request(self, url, *args):
        '''
        Makes request. Returns json if it receives valid response. Otherwise it returns empty directory.
        The url is the enpoint and *args are its optional parameters.
        '''
        response = requests.get(url, *args)
        if response.status_code not in self.good_result:
            return {}
        return response.json()
    
    def get_response(self, url, *args):
        '''
        Keeps repeating request until either time_out time is reached or a valid response is received.
        The url is the enpoint and *args are its optional parameters.
        '''
        response = self.make_request(url, *args)
        if response != {}:
            return response
        seconds = time.time()
        while(response == {}):
            if time.time() - seconds > self.time_out:
                raise Exception("time_out time reached")
            time.sleep(self.sleep)
            response = self.make_request(url, *args)
        return response