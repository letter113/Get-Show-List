'''
Created on 2010-8-16

@author: letter
'''
import html.parser
class Cat_html_parser(html.parser.HTMLParser):
    '''
    
    '''
#    http://www.pogdesign.co.uk/cat
#        the parser of the web site
#        input is a date e.g. 2009-09-09
#        output is the showlist
#        in the following format:
#    09
#    > True Blood
#    S: 3 - Ep: 9    
#    ...
    


    def __init__(self, date, end_date, output_file):
        '''
        Constructor
        get the show list from date to enddate [date,enddate]
        '''
#        the format of date: dd-mm-yyyy
#                    the address of cat is 
#                    http://www.pogdesign.co.uk/cat/8-2010
#                    with date in the trail
        html.parser.HTMLParser.__init__(self)
        self.date = date
        self.end_date = end_date
        self.start = False
        self.ready_to_end = False # handle this td and end the job
        self.a = False #get the data  of <a></a>
        self.span = False #get the data of <span></span>
        self.th = False #the date e.g. 19 (just a number)
        self.filepath = output_file
        self.counter = 0
        self.writefile = open(self.filepath, 'a')
    
    def is_episode(self, attrs):
        # episode attrs include eplink, eplink final and eplink premiar, so it's eplink*
        for attr in attrs:
            if attr[0] == "class" and attr[1].find("eplink") != -1:
                return True
        return False
    
    def is_seasep(self, attrs):
        # same reason, seasep*
        for attr in attrs:
            if attr[0] == "class" and attr[1].find("seasep") != -1:
                return True
        return False
    
    def is_capture(self,attrs):
        pass
        
    def handle_starttag(self, tag, attrs):
             
        if (tag == 'td' and False == self.start and 0 < attrs.count(('id', self.date))):
            # days begin with <td id="16-8-2009" ...>
            self.start = True      
        if tag == 'td' and self.start and 0 < attrs.count(('id', self.end_date)):
#            self.start = False
            self.ready_to_end = True
            
        if (self.start and tag == 'a' and self.is_episode(attrs)):
            #the tag of showname  <a>Showname</a>
            self.a = True   
        if (self.start and tag == 'span' and self.is_seasep(attrs)):
            #the tag of seasonEpi
            self.span = True 
        # print the date      
        if (self.start and tag == 'th'):
            self.th = True
            
    def handle_endtag(self, tag):
        if tag == 'html' or tag == 'body':
            self.writefile.close()
        elif tag=="table" and self.ready_to_end:
            self.counter = 1        
        elif tag == "td" and self.ready_to_end and self.counter == 1:
            self.start = False
            self.ready_to_end = False
            self.writefile.close()
            
    def handle_data(self, data):
        
        if self.a:
            self.writefile.write(data + '\t')
            self.a = False
        
        elif self.span:
            self.writefile.write(data + '\n')
            self.span = False
        
        elif self.th:
            self.writefile.write(data + '\n')
            self.th = False
            
    def close(self):
        html.parser.HTMLParser.close(self)
        self.writefile.close()
             
            
    
    
        
