import sys
import os
import re
import subprocess
from operator import itemgetter

class FunFinder:

    #===== CONSTRUCTOR STUFF =====

    #Initialize it with a list of args
    def __init__(self, argList):
        
        #Initialize our members
        self.target = ''
        self.DEBUG = False
        self.useGoto = False            #cd to best matching directory
        self.useColor = False           #color the output
        self.useDirOnly = False         #only find directories
        self.useFeelingLucky = False    #only return the best result
        self.useForceRoot = False       #start find from '/'

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
            if(arg == "--debug"):
                self.DEBUG = True
            elif(arg == "--root"):
                self.useForceRoot = True
            elif('d' in arg):
                self.useDirOnly = True
            
        else:
            #we have a target
            self.target = arg


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
        else:
            findShellCall.append('.')

        if(self.useDirOnly):
            findShellCall.append('-type')
            findShellCall.append('d')
        
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
        
    def dump_results(self):
        while(len(self.sortedResults)):
            curResult = self.sortedResults.pop()
            print curResult[0]


