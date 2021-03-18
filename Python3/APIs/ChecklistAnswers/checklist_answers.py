import os, sys
# add the parent directory to the system path to use shared config and l2l_api module. Can put the l2l_api file in the same directory as this file as well.
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import l2l_api, csv, json, datetime, dateutil
from dateutil import parser

# change directory so the .csv file and log file will be saved in the same directory as this file. Can change the save location in the config.json file.
os.chdir(os.path.dirname(os.path.realpath(__file__)))


class ChecklistAnswers:
    '''Creates a .csv spreadsheet of checklist answers from a single site over a date range.
    
    Sample script usage:
    $ python3 checklist_answers.py
    
    User will be prompted for the site and start and end dates.'''

    def __init__(self):
        '''Sets up all the class variables.'''

        # Set the CONFIG object from the config.json file
        self.CONFIG = None
        self.loadConfig()

        # set the L2L API class
        self.L2L = l2l_api.L2LApi(self.CONFIG['apiurl'], self.CONFIG['apikey'], self.CONFIG['verbose'])

        # set the log and csv directires. create if needed.
        current_path = os.path.dirname(os.path.realpath(__file__))
        if not self.CONFIG['logdirectory'] or not os.path.isdir(self.CONFIG['logdirectory']):
            self.CONFIG['logdirectory'] = os.path.join(current_path, 'log')
            if not os.path.isdir(self.CONFIG['logdirectory']):
                os.mkdir(self.CONFIG['logdirectory'])
        else:
            self.CONFIG['logdirectory'] = self.CONFIG['logdirectory'].rstrip('/')
        if not self.CONFIG['csvdirectory'] or not os.path.isdir(self.CONFIG['csvdirectory']):
            self.CONFIG['csvdirectory'] = os.path.join(current_path, 'csv')
            if not os.path.isdir(self.CONFIG['csvdirectory']):
                os.mkdir(self.CONFIG['csvdirectory'])
        else:
            self.CONFIG['csvdirectory'] = self.CONFIG['csvdirectory'].rstrip('/')
        
        self.VERBOSE = self.CONFIG['verbose']
        self.SITE = None
        self.CATEGORIES = []
        self.ENDDATE = None
        self.STARTDATE = None
        self.LOGFILENAME = os.path.join(self.CONFIG['logdirectory'], 'log-' + self.getCurrentDateTimeStrForFilename() + '.log')
        self.CSVFILENAME = os.path.join(self.CONFIG['csvdirectory'], 'checklist-' + self.getCurrentDateTimeStrForFilename() + '.csv')
        self.log('log file: {}\ncsv file: {}'.format(self.LOGFILENAME, self.CSVFILENAME))
        
        self.L2L.setLogFilename(self.LOGFILENAME)
        return None

    def main(self):
        '''Run the application. User will be prompted to choose a site and a date range, then the CSV sheet will be created'''

        # choose a site. if no site is selected, stop the process.
        if not self.chooseSite():
            return None

        # choose a date range. if an invalid date range is provided, stop the process.
        if not self.chooseDateRange():
            return None

        # export answers to a .csv spreadsheet.
        self.exportAnswersToCSV()

    def loadConfig(self):
        '''Loads the configuration settings into the app. Can create a config-dev.json file for development purposes, and remove it before deployment.'''
        
        # find the nearest config file. Give precedence to the config-dev.json files.
        config_filename = None
        if os.path.exists('config-dev.json'):
            config_filename = 'config-dev.json'
        elif os.path.exists('../config-dev.json'):
            config_filename = '../config-dev.json'
        elif os.path.exists('config.json'):
            config_filename = 'config.json'
        elif os.path.exists('../config.json'):
            config_filename = '../config.json'
        else:
            raise ValueError('Cannot find config.json file')

        # load the configuration settings
        with open(config_filename) as config:
            self.CONFIG = json.load(config)

    def chooseSite(self):
        '''Pulls a list of sites from the L2L server, and prompts the user to enter a Site ID'''

        # get a list of sites from the server and display them on screen
        sites = self.L2L.doGet('sites', {'order_by':'site'}, 1000)
        print('SITES:')
        for site in sites:
            print('{}: {}'.format(site['site'], site['description']))

        # prompt the user to enter a site id
        user_site_id = int(input('Please enter a site number from above: '))

        # find the site the user entered, store it.
        for site in sites:
            if site['site'] == user_site_id:
                self.SITE = site
                break

        # if the user entered a bad site id, retry
        if self.SITE == None:
            self.log('ERROR: Not a valid site id. Please try again.', True)
            return self.chooseSite()
        
        # print out the selected site
        self.log('Site selected: {}: {}'.format(self.SITE['site'], self.SITE['description']), True)

        return True

    def chooseDateRange(self):
        '''Prompts the user to choose a start and end date. Limit the date range to 31 days (one month).'''

        # prompt the user for a start and end date
        start_date = input('Please enter the start date: ')
        end_date = input('Please enter the end date: ')

        # validate the dates, take the earlist date as the start date, latest date as end date.
        # if any of the dates are invalid, retry.
        try:
            self.STARTDATE = min([parser.parse(start_date), parser.parse(end_date)])
            self.ENDDATE = max([parser.parse(start_date), parser.parse(end_date)])
        except ValueError:
            self.log('ERROR: One of the dates was not valid. Please try again.', True)
            return self.chooseDateRange()

        # verify the date is 
        if (self.ENDDATE - self.STARTDATE).total_seconds() >= 31 * 24 * 60 * 60:
            self.log('ERROR: You can only select one month at a time. Please try again.', True)
            return self.chooseDateRange()

        self.log('Start date: {}, End date: {}'.format(self.makeDateString(self.STARTDATE), self.makeDateString(self.ENDDATE)))

        return True
        
    def exportAnswersToCSV(self):
        '''Creates a .csv spreadsheet with one answer per row. Gets all checklist documents using the
        selected site and for the selected date range. Uses the L2L /checklists/ API, which returns one 
        record per filled out checklsit. Each checklist object contains a list of answers and a list of 
        tasks.'''

        # start the timer
        self.log('Gathering checklist answers', True)
        start = datetime.datetime.now()

        # define a list of headers for the .csv file. create the .csv file using the headers list.
        field_names = ['checklist_id', 'document_id', 'document_name', 'checklist_number', 'checklist_created', 'checklist_updated', 'checklist_udpated_by', 'checklist_closed', 'checklist_closed_date', 'dispatch_number', 'area_id', 'area_code', 'area_description', 'line_id', 'line_code', 'line_description', 'machine_id', 'machine_code', 'machine_description', 'technology_id', 'product_id', 'product_code', 'product_description', 'product_order_id', 'build_sequence_id', 'question', 'answer_na', 'answer', 'answer_created', 'answer_by', 'control_limit_low', 'control_limit_high', 'reject_limit_low', 'reject_limit_high']
        with open(self.CSVFILENAME, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames = field_names, quoting=csv.QUOTE_NONNUMERIC, delimiter=',', quotechar='"')
            writer.writeheader()
            
            # get completed checklists 500 at a time.
            finished = False
            offset = 0
            limit = 500
            data = {'site':self.SITE['site'], 'closeddate__gte':self.L2L.makeDateString(self.STARTDATE), 'closeddate__lte':self.L2L.makeDateString(self.ENDDATE)}
            while not finished:
                # get the checklists from the L2L server
                checklists = self.L2L.doGet('checklists', {**data, 'offset': offset}, limit)
                print('.', end='')
                if checklists is not None and len(checklists) > 0:
                    for checklist in checklists:
                        writer.writerows(self.formatChecklistAnswers(checklist)) # write answers to file
                if checklists is None or len(checklists) < limit:
                    finished = True
                else:
                    offset += len(checklists)
        
        # print out the total time it took to gather checklist answers
        self.log('\nCompleted in ' + str(datetime.timedelta(seconds = (datetime.datetime.now() - start).seconds)), True)
                        
        return None

    def formatChecklistAnswers(self, checklist):
        '''Re-formats a checklist object into a list of answers.'''

        # get the Area, Line, Machine, Product info
        area = line = machine = product = {'code':'', 'description': ''} # default values
        if checklist['area']:
            area = self.L2L.doGetWithCache('areas', {'site':self.SITE['site'], 'id':checklist['area']})
        # line = {'code':'', 'description': ''} # default line values
        if checklist['line']:
            line = self.L2L.doGetWithCache('lines', {'site':self.SITE['site'], 'id':checklist['line']})
        # machine = {'code':'', 'description': ''} # default machine values
        if checklist['machine']:
            machine = self.L2L.doGetWithCache('machines', {'site':self.SITE['site'], 'id':checklist['machine']})
        # product = {'code':'', 'description': ''} # default product values
        if checklist['product']:
            product = self.L2L.doGetWithCache('productcomponents', {'site':self.SITE['site'], 'id':checklist['product']})

        answers = []
        # shared document variables. these are attributes that are shared by all answers.
        document = {
            'checklist_id': checklist['id'],
            'document_id':checklist['document'], 
            'document_name': checklist['name'], 
            'checklist_number': checklist['number'], 
            'checklist_created': checklist['created'], 
            'checklist_updated': checklist['lastupdated'],
            'checklist_udpated_by': checklist['lastupdatedby'],
            'checklist_closed': checklist['closed'],
            'checklist_closed_date': checklist['closeddate'], 
            'dispatch_number': checklist['dispatch'], 
            'area_id': checklist['area'], 
            'area_code': area['code'],
            'area_description': area['description'],
            'line_id': checklist['line'], 
            'line_code': line['code'], 
            'line_description': line['description'], 
            'machine_id': checklist['machine'], 
            'machine_code': machine['code'], 
            'machine_description': machine['description'], 
            'technology_id': checklist['technology'], 
            'product_id': checklist['product'], 
            'product_code': product['code'], 
            'product_description': product['description'], 
            'product_order_id': checklist['product_order'], 
            'build_sequence_id': checklist['build_sequence'],
        }

        # sometimes python leaves the task list as a string instead of parsing it. skip the checklist. re-running the script for the same date range usally works the second time.
        if isinstance(checklist['tasks'], str):
            self.log(['tasks is not an object. skipping the checklist.', checklist['tasks']])
            return answers

        # loop through all checklist answers. dataset contains one record per checklist answer, even if the answer is inside a table.
        if checklist['answers'] is not None:
            for answer in checklist['answers']:
                # if the answer is part of a table, pull the question text accordingly
                if answer['table_row_number'] is not None and answer['table_column_number'] is not None:
                    question = checklist['tasks'][int(answer['task_number'])-1]['table']['rows'][int(answer['table_row_number'])-1]['columns'][int(answer['table_column_number'])-1]['text']
                # question was not inside a table
                else:
                    question = checklist['tasks'][int(answer['task_number'])-1]['text']
                # append the answer the answers list
                answers.append({
                    **document,
                    'question': question,
                    'answer_na': answer['na'], 
                    'answer': answer['answer'], 
                    'answer_created': answer['created'], 
                    'answer_by': answer['lastupdatedby'], 
                    'control_limit_low': answer['control_limit_low'], 
                    'control_limit_high': answer['control_limit_high'], 
                    'reject_limit_low': answer['reject_limit_low'], 
                    'reject_limit_high': answer['reject_limit_high'],
                })
        return answers
    
    def getCurrentDateTimeStrForFilename(self):
        '''Returns the current date time in a format that can be used to name files.'''
        return self.makeDateString(datetime.datetime.now(), '%Y-%m-%d %H-%M-%S')
    
    def makeDateString(self, date_time, format="%Y-%m-%d %H:%M:%S"):
        '''Creates a date/time string using the date_time provided.
        Variables:
            date_time : string or datetime object to be converted.
            format : The format of the string. Defaults to the standard format accepted by L2L'''

        if type(date_time) is str:
            date_time = dateutil.parser.parse(date_time)
        return date_time.strftime(format)

    def log(self, items, verbose = False):
        '''Outputs an item or list of items to a log file. Accepts strings and json objects. Can also output the string to the terminal.'''
        # create a list if only a single item is passed in. doing so simplifies the rest of this method.
        if not isinstance(items, list):
            items = [items]
        
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


# automatically run the application
if os.getenv('ENVIRONMENT') is None and __name__ == '__main__':
    CA = ChecklistAnswers()
    CA.main()