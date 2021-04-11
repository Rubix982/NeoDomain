import json
import sys
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

class DNSMessageCacheHandler():

    # self static identification counter
    IDENTIFICATION_COUNTER = '0x0'

    # Capacity Size
    CACHE_CAPACITY = int(os.environ['CACHE_CAPACITY'])

    def __init__(self, identification='',
                 flags='', numQuestions='',
                 numAnswerRRs='', numAuthorityRRs='',
                 numAdditionalRRs='', questions='',
                 answers='', authority='',
                 additional=[]):

        # Identification - 16 bit # for query,
        # reply to query uses same, 2 bytes
        self.identification = identification

        # Flags - query or reply, recursion desired
        # recursion available, reply is authoritative
        # 2 bytes
        self.flags = flags

        # 2 bytes
        self.numQuestions = numQuestions

        # 2 bytes
        self.numAnswerRRs = numAnswerRRs

        # 2 bytes
        self.numAuthorityRRs = numAuthorityRRs

        # 2 bytes
        self.numAdditionalRRs = numAdditionalRRs

        # Name, type fields for a query, 4 bytes
        self.questions = questions

        # RRs in a response to query, 4 bytes
        self.answers = answers

        # Records for authoritative servers, 4 bytes
        self.authority = authority

        # Additional "helpful" info that maybe used, 4 bytes
        self.additional = additional

    def DefaultInit(self):
        # # # Get the identification number
        identificationNumber = hex(
            int(DNSMessageCacheHandler.IDENTIFICATION_COUNTER, 0) + 1)

        # # # Self updation
        DNSMessageCacheHandler.IDENTIFICATION_COUNTER = identificationNumber

        # # # Reduce to just packet number
        identificationNumber = identificationNumber[2:]

        # # # Flag indicators
        flagByteOne, flagByteTwo = 10, 10

        # # # Hex conversion
        flag = hex(flagByteOne)[2:] + hex(flagByteTwo)[2:]

        # # # Num of questions, range is 0 - 255
        numQuestions = 255

        numQuestionsHex = hex(numQuestions)[2:]

        # # # Num of questions, range is 0 - 255
        numAnswersRR = 255

        numAnswersRRHex = hex(numAnswersRR)[2:]

        # # # Num of authority RRs, range is 0 - 255
        numAuthorityRRs = 255

        numAuthorityRRsHex = hex(numAuthorityRRs)[2:]

        # # # Num of additional RRs, 0 - 2555
        numAdditionalRRs = 255

        numAdditionalRRsHex = hex(numAdditionalRRs)[2:]

        # # # # Question, Variable # Of Question
        # websiteDomainHexConversion = ''
        # for character in self.questions:
        #     if character == '.':
        #         websiteDomainHexConversion += '.'
        #     else:
        #         websiteDomainHexConversion += hex(
        #             ord(character.lower()) - 97)[2:]

        # # # For the record type, let
        # # # A = 0, AAAA = 1, NS = 2, MX = 3, CNAME = 4
        # # # With default, since we are querying a A record
        # # # for TLDs, we'll use A as the default type
        # websiteDomainHexConversion += '0'

        self.identification = identificationNumber
        self.flags = flag
        self.numQuestions = numQuestionsHex
        self.numAnswerRRs = numAnswersRRHex
        self.numAuthorityRRs = numAuthorityRRsHex
        self.numAdditionalRRs = numAdditionalRRsHex
        # self.questions = websiteDomainHexConversion
        self.answers = ''
        self.authority = ''
        self.additional = []

        return self

    def EncodeObject(self):
        return json.dumps(vars(self)).encode('utf-8')

    def setWebsiteConfig(self, hostName, domainName):
        self.questions = hostName + '.' + domainName

    def GetStrForWebsiteDomain(self):
        # websiteDomainStr = ''

        # for character in self.questions.split('.')[-1][0:-1]:
        #     websiteDomainStr += chr(int(character, 26) + 97)
        return self.questions.split('.')[-1]

    def GetStrForWebsiteHost(self):
        # websiteHostStr = ''

        # for character in self.questions.split('.')[0]:
        #     websiteHostStr += chr(int(character, 26) + 97)
        return '.'.join(self.questions.split('.')[0:-1])

    def GetStrForWebsite(self):
        return self.GetStrForWebsiteHost() + '.' + self.GetStrForWebsiteDomain()

    def DumpToCache(self, fileName: str):

        with open(fileName, mode='r') as cacheFile:
            JSONdata = json.load(cacheFile)

        # flush file
        if len(JSONdata) == DNSMessageCacheHandler.CACHE_CAPACITY:
            open(fileName, mode='w').close()

        JSONToDump = {}

        additionalObject = self.additional

        if len(additionalObject) >= 1:
            JSONToDump['A'] = {}
            JSONToDump['A']['IPv4'] = additionalObject[0]

        if len(additionalObject) >= 2:
            JSONToDump['NS'] = {}
            JSONToDump['NS']['names'] = additionalObject[1]

        if len(additionalObject) >= 3:
            JSONToDump['MX'] = {}
            JSONToDump['MX']['preferences'] = additionalObject[2]

        JSONdata[self.GetStrForWebsite()] = JSONToDump

        with open(fileName, mode='w') as cacheFile:
            json.dump(JSONdata, cacheFile, ensure_ascii=False, indent=4)
