# from botocore.vendored import requests
import requests
import dateutil
import datetime
import json
import time


class L2LApi:
    '''Make API requests to a server running Leading2Lean's CloudDISPATCH. See l2l.com for more info.'''

    def __init__(self, url, auth, verbose=False):
        '''Sets up the L2LApi class.
        Variables:
            url : The URL of the CloudDISPATCH server. e.g. https://customer.leading2lean.com/api/1.0/
            auth : The authorization key for the server
            verbose : Set to True if you want to see logging in the terminal'''

        self.URL = url
        self.AUTH = auth
        self.VERBOSE = verbose
        self.LOGFILENAME = None
        self.CACHE = {}  # e.g. {'dispatches': {1234: {'id':1234, 'number':'2345', ...}}}

    def setLogFilename(self, log_filename):
        '''Sets the filename of a log file to be used to log each API call. If this is not set, no log entries will be made.
        Variables:
            log_filename : The full path of the log file.'''

        self.LOGFILENAME = log_filename

    def doPost(self, url, data, limit=1):
        '''Perform a POST operation on the L2L server.
        Variables:
            url : The path of the API call. e.g. dispatches/open
            data : An object of variables to send in the POST body. e.g. {"dispatchtypecode":"CODE RED", "description":"Machine is down" ... }
            limit : The number of results to be returned. defaults to 1'''

        # perform the actual POST
        result = requests.post(self.URL + url, {'auth': self.AUTH, 'limit': limit, **data})
        # retry if needed
        if self.__doIntelligentRetry(result):
            return self.doPost(url, data, limit)

        return self.__finishRequest('POST', result, limit)

    def doGet(self, url, data, limit=1):
        '''Performs a GET operation on the L2L server.
        Variables:
            url : The path of the API call. e.g. dispatches
            data : An object of variables to send in the request. e.g. {"dispatchnumber":"12345"}
            limit : The number of results to be returned. defaults to 1'''

        # perform the actual GET
        result = requests.get(self.URL + url, {'auth': self.AUTH, 'limit': limit, **data})
        # retry if needed
        if self.__doIntelligentRetry(result):
            return self.doGet(url, data, limit)

        return self.__finishRequest('GET', result, limit)

    def doGetAll(self, url, data, limit=500):
        '''Performs a GET operation on the L2L server, returning all results across all pages. This method should only be used when all objects are needed from L2L.
        Variables:
            url : The path of the API call. e.g. dispatches
            data : An object of variables to send in the request. **Be sure to include all possible filters to decrease the load on the server.**
            e.g. {"dispatchtypecode":"CODE RED", "created__gte":"2020-01-01 00:00:00", "created__lt":"2020-01-08 00:00:00"}
            limit : The number of results to be returned per page. defaults to 500'''

        result_all = []
        finished = False
        offset = 0

        while not finished:
            # perform the actual GET
            result = self.doGet(url, {**data, 'offset': offset}, limit)
            # append the result to the result_all list
            if result is not None:
                result_all.extend(result)
            # last result. stop the loop
            if result is None or len(result) < limit:
                finished = True
            else:
                offset += len(result)

        return result_all

    def doGetWithCache(self, url, data):
        '''Performs a GET operation, and caches the result. This decreases the number of API calls performed on a server, which will speed up an application.
        ONLY USE THIS METHOD TO LOOK UP ITEMS BY CODE OR BY KEY. Otherwise, results will be inconsistent. `limit` is hard coded to 1 to enforce this assumption.
        Cache is only stored in memory. Cache will be destroyed when the application terminates.'''

        # build a key to store and look up cached items
        cache_key_arr = []
        for key, value in data.items():
            cache_key_arr.extend((str(key), str(value)))
        cache_key = '-'.join(cache_key_arr)

        # no cached item. perform the API call, cache the result
        if url not in self.CACHE or cache_key not in self.CACHE[url]:
            result = self.doGet(url, data, 1)
            if url not in self.CACHE:
                self.CACHE[url] = {}
            self.CACHE[url][cache_key] = result

        # return from cache
        return self.CACHE[url][cache_key]

    def __finishRequest(self, verb, result, limit):
        '''Private method. Finishes the doPost and doGet methods with common reporting and return strategies'''

        self.__log(' : {} : {} : {}'.format(verb, result.elapsed, result.url))

        resultJson = result.json()

        if resultJson['success'] and resultJson['data']:
            # only return the top object if the request was for a single object
            if limit == 1 and len(resultJson['data']) > 0 and isinstance(resultJson['data'], list):
                return resultJson['data'][0]
            else:
                return resultJson['data']
        # log the response if the request was not successful.
        else:
            self.__log(str(result.status_code) + ': ' + result.text)
            return None

    def __doIntelligentRetry(self, result):
        '''Retry the request if status 429 is returned. Will pause for the number of seconds indicated in the "Retry-After" header, if provided. If none is
        provided, will pause for 5 seconds'''

        if result.status_code == 429:
            retry_seconds = 5
            if result.headers['Retry-After']:
                retry_seconds = int(result.headers['Retry-After'])
            self.__log('WARNING: received status 429. retrying in {} seconds.'.format(retry_seconds), True)
            time.sleep(retry_seconds)
            return True
        return False

    def makeDateString(self, date_time, format="%Y-%m-%d %H:%M:%S"):
        '''Creates a date/time string using the date_time provided.
        Variables:
            date_time : string or datetime object to be converted.
            format : The format of the string. Defaults to the standard format accepted by L2L'''

        if type(date_time) is str:
            date_time = dateutil.parser.parse(date_time)
        return date_time.strftime(format)

    def __log(self, items, verbose=False):
        '''Outputs an item or list of items to a log file. Accepts strings and json objects. Can also output each item to the terminal.'''

        # create a list if only a single item is passed in. doing so simplifies the rest of this method.
        if not isinstance(items, list):
            items = [items]

        # loop through each item, and write it to the log
        for item in items:
            if(self.LOGFILENAME):
                with open(self.LOGFILENAME, 'a') as logfile:
                    logfile.write(item+'\n')
            # output to the terminal
            if self.VERBOSE or verbose:
                if type(item) is json:
                    print(json.dumps(item, indent=4, separators=(',', ': ')))
                else:
                    print(item)
        return None
