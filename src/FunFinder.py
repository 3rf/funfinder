import sys
import os
import re
import subprocess

class FunFinder:

    #===== CONSTRUCTOR STUFF =====

    #Initialize it with a list of args
    def __init__(self, argList):
        
        #Initialize our members
        self.target = ''
        self.DEBUG = False
        self.usePath = False            #use -ipath instead of -iname
        self.useGoto = False            #cd to best matching directory
        self.useColor = False           #color the output
        self.useDirOnly = False         #only find directories
        self.useFeelingLucky = False    #only return the best result
        self.useForceRoot = False       #start find from '/'
        self.useForceHome = False       #start find from '~/'

        for arg in argList:
            self.parse_argument(arg)

        self.generate_regex()


    #Generate find --name and regex for sorting
    def generate_regex(self):

        #TODO: does * in target break this?

        targetString = self.target
        allChars = [x for x in targetString]

        #Get the wildcarded name parameter for UNIX find to use
        self.findTarget = '*'+'*'.join(allChars)+'*'
        
        #Generate compiles regex for results analysis and ranking
        self.regexTarget = re.compile(r'(?=('+".*?".join(allChars)+r'))',
                                      re.DOTALL|re.IGNORECASE)


    #Parse an argument, setting flags, and so on
    def parse_argument(self, arg):

        if(arg[0] == '-'):
            #we have a flag
            if('--' in arg):
                if(arg == "--debug"):
                    self.DEBUG = True
                elif(arg == "--root"):
                    self.useForceRoot = True
                elif(arg == "--help"):
                    self.show_help()                    
                elif(arg == "--home"):
                    self.useForceHome = True
                elif(arg == "--goto"):
                    self.useFeelingLucky = True
                    self.useDirOnly = True
            else:
                if('d' in arg):
                    self.useDirOnly = True
                if('c' in arg):
                    self.useColor = True
                if('p' in arg):
                    self.usePath = True
                if('l' in arg):
                    self.useFeelingLucky = True
                if('h' in arg):
                    self.show_help()
        else:
            #we have a target
            self.target = arg

    #Hmmm I wonder what this function does...
    def show_help(self):
        print"""
\tusage: funfind [-dcplh] [--OPTION] [EXPRESSION TO FIND]

\t    -c    : highlight expression in results using ANSI color
\t    -p    : apply expression to whole path, not just filename
\t    -l    : only display best result ("lucky")
\t    -d    : only find directories
\t    -h    : show this message
\t--root    : start search from /
\t--home    : start search from ~/        
"""
        exit(0)


    #===== UNIX FIND STUFF =====

    def run_unix_find(self):

        findCallList = self.build_find_call()

        if(self.DEBUG):
            print findCallList

        #create temp subproc for find
        findResultsRaw = subprocess.check_output(findCallList)
        self.findResults = findResultsRaw.rstrip().split('\n')

    def build_find_call(self):
        findShellCall = ['find']

        #check find flags
        if(self.useForceRoot):
            findShellCall.append('/')
        elif(self.useForceHome):
            findShellCall.append('/home')
        else:
            findShellCall.append('.')

        if(self.useDirOnly):
            findShellCall.append('-type')
            findShellCall.append('d')
        
        if(self.usePath):
            findShellCall.append('-ipath')
        else:
            findShellCall.append('-iname')
        findShellCall.append(self.findTarget)

        return findShellCall


    #===== SORTING STUFF =====

    def rank_results(self):
        results = self.get_analyzed_results()
        #sort by match len, then path len, then alphabet
        self.sortedResults = sorted(results, key=lambda a:(len(a[1]), len(a[0]), a[0]))


    def get_analyzed_results(self):  

        #quick lil' get shortest match func
        def shortest_match(string):
            matches = self.regexTarget.findall(string)
            return min(matches, key=len)

        analyzedResults = [(r, shortest_match(r)) for r in self.findResults if r != ""]
        return analyzedResults


    #===== PRINTING STUFF =====

    #helper function for colored highlighting
    def get_color_substr(self, result):
        colorANSI = "\x1B[32;40m"   #TODO make this a confid
        colorStopANSI = "\x1B[0m"

        subStart = result[0].find(result[1])
        subEnd = subStart + len(result[1])
        split = (result[0][:subStart],
                 result[0][subStart: subEnd],
                 result[0][subEnd:])
        return split[0]+colorANSI+split[1]+colorStopANSI+split[2]

        
    def dump_results(self):

        #quick helper for printing
        def print_result(result):
            if(self.useColor):
                print self.get_color_substr(result)
            else:
                print result[0]

        #only print best match if flag is on
        if(self.useFeelingLucky):
            if(len(self.sortedResults) > 0):
                print_result(self.sortedResults[0])
            return
            
        #else print all from worst to best
        while(len(self.sortedResults) > 0):
            curResult = self.sortedResults.pop()
            print_result(curResult)


