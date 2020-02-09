import json
from collections import namedtuple
import requests
import time
import sys


class TinderBot:

    def __init__(self, headersPath):
        self.headers = {}
        self.userIds = []
        self.s_numbers = []
        self.likes_url = "https://api.gotinder.com/like/{}?locale=en&s_number={}"
        self.core_url = 'https://api.gotinder.com/v2/recs/core?locale=en'
        self.travel_url = 'https://api.gotinder.com/passport/user/travel?locale=en'
        self.currentlen = 0
        self.loggedIn = False
        self.counter = 0
        txtfile = open(headersPath, "r")
        for line in txtfile.readlines():
            key_val = line.split(": ")
            self.headers[key_val[0]] = key_val[1].replace('\n', '')
        self.__loadUserIds()

    def __loadUserIds(self):
        response = requests.get(self.core_url, headers=self.headers)
        if 300 > response.status_code >= 200:
            self.loggedIn = True
        else:
            self.loggedIn = False

            return
        jsr = json.loads(json.dumps(response.json()))
        if len(jsr['data']["results"]) < 1:
            self.loggedIn = False

            return

        self.loggedIn = True

        # Grabbing all the user ids --> List
        for user in jsr['data']["results"]:
            self.s_numbers.append(user["s_number"])
            self.userIds.append(user["user"]["_id"])
        currentlen = len(self.userIds)

    def travel(self, location):
        if not isinstance(location, dict) or location['lat'] is None or location['lon'] is None:
            raise Exception(
                'Location variable in travel() function needs to be a dictionary and must contain lon and lat keys')

        travel_response = requests.post(self.travel_url, data=location, headers=self.headers)
        if 300 > travel_response.status_code >= 200:
            print("Changed Location successfully")
        else:
            print('Something went wrong while changing the location')

    def likeNext(self):
        # Calling the like API
        if len(self.userIds) > 0 and len(self.s_numbers) > 0:
            likes_response = requests.get(self.likes_url.format(self.userIds[0], self.s_numbers[0]),
                                          headers=self.headers)
            if 300 > likes_response.status_code >= 200:
                self.loggedIn = True
                self.userIds.pop(0)
                self.s_numbers.pop(0)
                self.counter = self.counter + 1
                return True
        else:
            self.loggedIn = False

            return False

    def likeAll(self, sleep=0.5, printProgress=True):
        if sleep < 0.5:
            raise Exception('Sleep variable in likeMany() function should at least be 0.5 seconds')
        newcounter = 0
        counter = 0
        currentlen = len(self.userIds)

        while True:
            time.sleep(sleep)
            if self.likeNext():
                if printProgress:
                    # Printing progress for curiosity
                    newcounter = newcounter + 1
                    self.__update_print(newcounter, currentlen, self.counter)
                else:
                    break

            else:
                self.__loadUserIds()
                newcounter = 0
                currentlen = len(self.userIds)

    def likeMany(self, maxLikes=5, sleep=0.5, printProgress=True):
        if sleep < 0.5:
            raise Exception('Sleep variable in likeMany() function should at least be 0.5 seconds')

        newcounter = 0
        currentlen = len(self.userIds)
        for i in range(len(self.userIds)):
            time.sleep(sleep)

            if maxLikes == 0:
                return
            else:
                self.likeNext()
                if printProgress:
                    # Printing progress for curiosity
                    newcounter = newcounter + 1
                    self.__update_print(newcounter, currentlen, self.counter)
                maxLikes = maxLikes - 1

    def __update_print(self, newcounter, currentlen, counter):

        sys.stdout.write('\r')
        sys.stdout.write("The user # {}/{} has been liked now! -- {} in total ".format(newcounter, currentlen, counter))
        sys.stdout.flush()
