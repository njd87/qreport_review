from bs4 import BeautifulSoup
import numpy as np
import requests

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
# list of functions used for scraping the q report

def request_page(link):
    return requests.get(url=link, headers=headers)

def getMeanHours(info):
    try:
        # parse html of q report
        soup = info['soup']

        # select mean hours
        return float([thing for thing in soup.find_all('td', class_='TabularBody_RightColumn_NoWrap', headers=True) if 'statValueID' in thing['headers'][0] and thing['headers'][1].lower() == 'mean'][0].encode_contents())
    except:
        return np.nan

def getStudents(info):
    try:
        # parse html of q report
        soup = info['soup']

        # select mean hours
        return int(soup.find_all('td', class_='TabularBody_MiddleColumn_NoWrap', attrs={'headers': 'hdGroup0 InvitedCount'})[0].encode_contents())
    except:
        return np.nan

def getDepartment(info):
    try:
        return str(info['name'][:info['name'].index(' ')])
    except:
        return np.nan

def getRecommendations(info):
    try:
        # parse html of q report
        soup = info['soup']

        # select mean hours
        return float([thing for thing in soup.find_all('td', class_='TabularBody_RightColumn_NoWrap', headers=True) if 'statValueID' in thing['headers'][0] and thing['headers'][1].lower() == 'mean'][1].encode_contents())
    except:
        return np.nan

def getInstructorRating(info):
    try:
        # parse html of q report
        soup = info['soup']

        # select mean hours
        return float([thing for thing in soup.find_all('td', class_='TabularBody_RightColumn_NoWrap2', headers=True) if '_7' in thing['headers'][0]][0].encode_contents())
    except:
        return np.nan
    
def getInstructor(info):
    try:
        # parse html of q report
        soup = info['soup']

        # find a span tag that has the text "Instructor Feedback"

        for possible in soup.find_all('span'):
            if 'Instructor Feedback' in possible.encode_contents().decode("utf-8"):
                res = possible.encode_contents().decode("utf-8")
                return res[res.index('for' ) + 4:]
            
        return np.nan

    except:
        return np.nan

# experimental
def getComments(info):
    try:
        # parse html of q report
        soup = info['soup']
        
        # select mean hours
        return [str(thing.encode_contents().decode("utf-8")) for thing in soup.find_all('td', class_='TabularBody_LeftColumn', headers=True) if 'comment' in thing['headers'][0]]
    except:
        return []