#!/usr/bin/env python
import time
import requests
from bs4 import  BeautifulSoup
import pandas as pd
from urllib.request import urlopen
from userAgents import user_agents, randomUserAgents
import lxml
import re

company_name = "Deloitte"
url = "https://www.glassdoor.com/Reviews/KPMG-Reviews-E2867.htm"
url_prefix = 'https://www.glassdoor.com/Reviews/KPMG-Reviews-E2867_P'
url_postfix = '.htm?filter.defaultEmploymentStatuses=false&filter.defaultLocation=false&filter.employmentStatus=REGULAR&filter.employmentStatus=PART_TIME&filter.employmentStatus=UNKNOWN'
start_index = 445
index_to_stop = 9999

head = randomUserAgents()
start = time.time()

def soup(url,headers):
    ''' url = full glassdoor.com/reviews url'''
    session = requests.Session()
    req = session.get(url, headers=headers)
    bs = BeautifulSoup(req.text, 'lxml')
    return bs

def getPages(url_prefix, url_postfix, head, start_index=1, index_to_stop=500):
    pages = []
    current_index = start_index
    while current_index <= index_to_stop:
        current_page = url_prefix + str(current_index) + url_postfix
        print("Adding page No.", current_index, "to list")
        pages.append(current_page)
        bs = soup(current_page, head)
        next_page_buttons = bs.select("div.pagingControls > ul > li.next a")
        if len(next_page_buttons) == 0:
            print("Last page found")
            break
        current_index += 1
    return pages

startTime = start - time.time()

a=[]
date=[]
revNo=[]
employee=[]
position = []
summ=[]
pro=[]
con=[]
advice=[]
locations = []
review = []
work_life_balance = []
culture_value = []
career_opportunities = []
comp_benefits = []
senior_management = []
link=[]
recommendations = []
outlook = []
approvals_of_ceo = []

current_index = start_index
count = 1
ceo_re = re.compile('^\s*CEO\s*$')
while current_index <= index_to_stop:
    page = url_prefix + str(current_index) + url_postfix

    print("Extracting reviews from page No.", current_index)
    bs = soup(page,head)
    for x in bs.findAll('li',{'class',' empReview cf '}):

    # ## PK
        a.append(count)
        count += 1

    ## Rev Number
        try:
            revNo.append(x.attrs['id'])
            # revNo.append(x.find('li',{'class':' empReview cf '}).attrs[' id'])
            # for emp in x.find(':
            #     print(emp.attrs[' id'])
        except:
            revNo.append('None')

    ## location 
        location_span = x.select('span.authorLocation')
        if len(location_span) == 0:
            locations.append('None')
        else:
            locations.append(location_span[0].string)

    ## overall rating
        try:
            rating = x.find('span',{'class':'rating'})
            for y in rating:
                review.append(rating.find('span',{'class':'value-title'})\
                              .attrs['title'])
        except:
            review.append('None')

    ## subRatings list
        # Work/Life Balance
        div = x.find('div', string='Work/Life Balance')
        if div == None:
            work_life_balance.append('None')
        else:
            span = div.next_sibling
            work_life_balance.append(span.attrs['title'])
        # Culture & Values
        div = x.find('div', string='Culture & Values')
        if div == None:
            culture_value.append('None')
        else:
            span = div.next_sibling
            culture_value.append(span.attrs['title'])
        # Career Opportunities
        div = x.find('div', string='Career Opportunities')
        if div == None:
            career_opportunities.append('None')
        else:
            span = div.next_sibling
            career_opportunities.append(span.attrs['title'])
        # Comp & Benefits
        div = x.find('div', string='Comp & Benefits')
        if div == None:
            comp_benefits.append('None')
        else:
            span = div.next_sibling
            comp_benefits.append(span.attrs['title'])
        # Senior Management
        div = x.find('div', string='Senior Management')
        if div == None:
            senior_management.append('None')
        else:
            span = div.next_sibling
            senior_management.append(span.attrs['title'])


    ## Date
        try:
            date.append(x.find('time',{'class':'date subtle small'}).text)
        except:
            date.append('None')
    # Summary
        try:
            summar = x.a.text
            summar = summar.split('"')
            summ.append(summar[1])
        except:
            summ.append('None')
    ## Pros
        try:
            pro.append(x.find('p',{'class':' pros mainText truncateThis'\
                            ' wrapToggleStr'}).text)
        except:
            pro.append('None')
    ## Cons
        try:
            con.append(x.find('p',{'class':' cons mainText truncateThis'\
                            ' wrapToggleStr'}).text)
        except:
            con.append('None')
    ## Advice to Management
        try:
            advice.append(x.find('p',{'class':' adviceMgmt mainText truncateThis'\
                            ' wrapToggleStr'}).text)
        except:
            advice.append('None')

    ## Employee Type
        try:
            employee.append(x.find('span',{'class':"authorJobTitle"}).text)
        except:
            employee.append('None')
    ## Position and Location
        try:
            position.append(x.find('p',{'class':' tightBot mainText'}).text)
        except:
            position.append('None')
    ## Review Link
        link.append(url+(x.find('a',{'class':'reviewLink'}).attrs['href'])) 

    ## recommendation
        rec = x.find('div', string='Recommends')
        if rec != None:
            recommendations.append('1')
        else:
            rec = x.find('div', string='Doesn\'t Recommend')
            if rec != None:
                recommendations.append('-1')
            else:
                recommendations.append('None')
    ## outlook
        rec = x.find('div', string='Positive Outlook')
        if rec != None:
            outlook.append('1')
        else:
            rec = x.find('div', string='Neutral Outlook')
            if rec != None:
                outlook.append('0')
            else:
                rec = x.find('div', string='Negative Outlook')
                if rec != None:
                    outlook.append('-1')
                else:
                    outlook.append('None')
    ## CEO
        ceo = x.find(string=ceo_re)
        if ceo != None:
            div = ceo.parent
            while(div.name != 'div'):
                div = div.parent
            i_tag = div.previous_sibling.find('i')
            if 'green' in i_tag['class']:
                approvals_of_ceo.append('1')
            elif 'yellow' in i_tag['class']:
                approvals_of_ceo.append('0')
            elif 'red' in i_tag['class']:
                approvals_of_ceo.append('-1')
            else:
                approvals_of_ceo.append('Error')
        else:
            approvals_of_ceo.append('None')
    

    next_page_buttons = bs.select("div.pagingControls > ul > li.next a")
    if len(next_page_buttons) == 0:
        print("Last page found")
        break
    current_index += 1


df=pd.DataFrame(index=a)
df['date'] = date
df['reviewNo'] = revNo
df['employeeType'] = employee
df['position'] = position
df['summary'] = summ
df['pro'] = pro
df['con'] = con
df['advice'] = advice
df['locations'] = locations
df['overallStar'] = review
df['workLifeStar'] = work_life_balance
df['cultureStar'] = culture_value
df['careerOppStar'] = career_opportunities
df['comBenefitsStar'] = comp_benefits
df['srManagementStar'] = senior_management
df['recommendations'] = recommendations
df['outlook'] = outlook
df['approvals_of_ceo'] = approvals_of_ceo
df['reviewLink'] = link

print('StartTime = {}\nEnd Time = {}'.format(startTime, start - time.time()))
csvName = input('What do you want to call the csv?')
df.to_csv('{}.csv'.format(csvName), sep=',')
