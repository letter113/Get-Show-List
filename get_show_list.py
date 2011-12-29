'''
Created on Dec 13, 2011

@author: ehhexxn
'''
import urllib.request
import Cat_html_parser
import html.parser
import argparse
import datetime
import os

def get_days_show(date, end_date, address,output_file): # parse the cat html page
    cat = Cat_html_parser.Cat_html_parser(date, end_date, output_file)
    sock = urllib.request.urlopen(address)
    htmlpage = sock.read()
#        cat.feed(str(self.htmlpage))
    try:
#            cat.feed('<td></td>')
        cat.feed(htmlpage.decode('utf-8'))
    except html.parser.HTMLParseError:
        print("HTML Parse Error")
        

def format_date(date):
    return "d_{}_{}_{}".format(date.day,date.month,date.year)

# the starting and ending date of this week in format d_dd_mm_yyyy
# consider the special case when the week is splited into 2 months
def get_start_end(args):
    mid = None
    if args.start != None and args.end != None:
        start = args.start
        end = args.end
    else:
        start = datetime.date.today()
        while start.isoweekday() > 1:
            start = start - datetime.timedelta(1)
        end = start + datetime.timedelta(6)

    if(start.month != end.month):
        mid = start
        while mid.month == start.month and mid != end:
            mid = mid + datetime.timedelta(1)
            if args.source != None:
                source = args.source
                if (len(source)!=2):
                    print ("You must specify 2 file")
                    exit(0)
                
            else:
                source = ["http://www.pogdesign.co.uk/cat/" + str(start.month) + "-" + str(start.year),
                          "http://www.pogdesign.co.uk/cat/" + str(end.month) + "-" + str(end.year)]
                
        print ((format_date(start), format_date(mid - datetime.timedelta(1))))
        print ((format_date(mid), format_date(end)))
        return [(format_date(start), format_date(mid - datetime.timedelta(1)),source[0]),
                (format_date(mid), format_date(end), source[1])]

def get_address(address):
    pass

def get_args():
#    get_days_show("d_12_12_2011", "d_13_12_2011", "file:///C:/Users/ehhexxn/Downloads/TV%20Calendar%20-%20December%202011%20TV%20listings%20guide.htm")
    parser = argparse.ArgumentParser(description='Process arguments of get_show_list')
    parser.add_argument('--start', dest='start',
                   help='The starting date, format yymmdd')
    parser.add_argument('--end', dest='end',
                   help='The ending date, format yymmdd')
    parser.add_argument('--source', dest="source", nargs="*",
                    help="The source file, default is http://www.pogdesign.co.uk/cat/")
    args = parser.parse_args()    
    return args

if __name__ == '__main__':
    args = get_args()
    get = get_start_end(args)
    try:
        os.system("rm add.txt")
    except:
        pass
    output_file = "add.txt"
    for item in get:
        get_days_show(item[0],item[1],item[2],output_file)
    file = open(output_file,"a")
    file.write("1111")
    file.close()
    os.system("perl align_add.pl")
    
    
    
