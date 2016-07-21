from datetime import datetime
from datetime import date

import re
import unirest

class APICalls(object):
    def __init__(self):
        self.API_KEY = '8mzBiWrKeqmshseRxCczOZoVPHM3p1Gs7bcjsnFezHLyxB2y8e'

    # TODO: Check if there was a response with shows or empty
    def search_show(self, query, search):
        responses = unirest.get("https://tvjan-tvmaze-v1.p.mashape.com/search/shows?q=" + self.query_tostring(query),
            headers={
                "X-Mashape-Key": self.API_KEY
            }
        )
    
        i = 1
        for response in responses.body:
            print '\t[%d] %s (status: %s)\n\t\t%s\n' % (i, response['show']['name'],
                                                        response['show']['status'],
                                                        self.shorten_summary(response['show']['summary']))
            i += 1
            
        if search:
            try:
                id = input("\nWhich show? Choose a number. >> ")
            except NameError:
                return None
            
            if type(id) == int and id > 0 and id < i:
                e = responses.body[id - 1]
                status = e['show']['status']
                
                if status == "Ended":
                    print "\nShow has ENDED, there is NO POINT in following it. DUH!"
                    return None
                elif status == "In Development":
                    print "\nThe show is in development. Check back later and go GOLD fish!"
                elif status == "To Be Determined":
                    print "\nLooks like you're favorite show might not make it. I'm so sorry, just know that I know how you feel."
                else:
                    # (name, identification, network, day)
                    return (e['show']['name'], e['show']['id'],
                            e['show']['network']['name'],
                            e['show']['schedule']['days'][0])
                
        return None

    def season_premiere(self, identification):
        responses = unirest.get("https://tvjan-tvmaze-v1.p.mashape.com/shows/" + str(identification) + "/seasons",
            headers={
                "X-Mashape-Key": self.API_KEY
            }
        )
        
        length = len(responses.body)
        
        premiere = responses.body[length - 1]['premiereDate']
        ending = responses.body[length - 1]['endDate']
        
        if premiere == None:
            if length > 1:
                return self.season_finale(responses.body[length - 2])
            else:
                print "\nThe season hasn't started yet, and currently I am not able to handle things such as this. You're just asking for TOO much!\nBut here is what is currently being watched... because I need to feel like I've done something right."
                return None
        else:
            premiere_date = datetime.strptime(premiere, '%Y-%m-%d')
            today = date.today()
            
            if premiere_date.year == today.year:
                if premiere_date.month < today.month:
                    return (premiere, ending)
                elif premiere_date.month == today.month:
                    if premiere_date.day <= today.day:
                        return (premiere, ending)
                    
            print "\nSeason hasn't started yet. Get back to me later."
            return None

    def season_finale(self, prev):
        premiere = prev['premiereDate']
        ending = prev['endDate']
        
        if ending != None:
            end_date = datetime.strptime(ending, '%Y-%m-%d')
            today = date.today()
            
            if end_date.year == today.year:
                if end_date.month > today.month:
                    return (premiere, ending)
                elif end_date.month == today.month:
                    if end_date.day >= today.day:
                        return (premiere, ending)
                    
        print "\n The season hasn't started yet was not renewed. More likely not renewed. So sad for you!"
        return None

    def remove_tags(self, string):
        return re.sub("\n", "", re.sub("</?\\w+>", "", string))

    def shorten_summary(self, summary):
        descript = self.remove_tags(summary)
        
        if len(descript) < 1:
            return "No summary, so take a chance if you want"
        
        return descript[0:80] + "\n\t\t" + descript[80:160] + "\n\t\t" + descript[160:240] + "..."
    
    def query_tostring(self, query):
        nw = ""
        
        for q in query:
            nw += q + "+"
            
        return nw
