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
        
        #Generate regex for results analysis and ranking
        self.regexTarget = r'(?=('+".*?".join(allChars)+r'))'
        

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
        
        findShellCall.append('-name')
        findShellCall.append(self.findTarget)

        return findShellCall







