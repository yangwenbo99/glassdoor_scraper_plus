#!/usr/bin/env python
import time
import requests
from bs4 import  BeautifulSoup
import pandas as pd
from urllib.request import urlopen
from userAgents import user_agents, randomUserAgents
import lxml
import re
import math

class Company:
    def __init__ (self, 
            url, 
            start_index = 1,
            end_index = math.inf,
            company_name = None,
            max_retry_time = 3,
            page_type = 'normal', 
            base_url = None):
        if base_url == None:
            self.url = url
        else:
            self.url = base_url
        if (page_type == 'country'):
            m = re.match('^(.*?)(_IP\d+|)(\.htm.*)$', url)
            self.url_prefix = m.group(1) + '_IP' 
            self.url_postfix = m.group(3)
        else:
            m = re.match('^(.*?)(_P\d+|)(\.htm.*)$', url)
            self.url_prefix = m.group(1) + '_P' 
            self.url_postfix = m.group(3)
        self.start_index = start_index
        self.end_index = end_index
        self.head = randomUserAgents()
        self.max_retry_time = max_retry_time
        self.result = {
                'count': [],
                'date': [],
                'reviewNo': [],
                'employeeType': [],
                'position': [],
                'summary': [],
                'pro': [],
                'con': [],
                'advice': [],
                'locations': [],
                'overallStar': [],
                'workLifeStar': [],
                'cultureStar': [],
                'careerOppStar': [],
                'comBenefitsStar': [],
                'srManagementStar': [],
                'recommendations': [],
                'outlook': [],
                'approvals_of_ceo': [],
                'reviewLink': [] }

    # Return: index of the last page read
    def extract (self):
        current_index = self.start_index
        count = 1;
        not_last_page = True
        ceo_re = re.compile('^\s*CEO\s*$')
        while current_index <= self.end_index and not_last_page:
            page = self.url_prefix + str(current_index) + self.url_postfix

            print("Extracting reviews from page No.", current_index)
            bs = Company.soup(page, self.head)
            retry_count = 0
            next_page_buttons = bs.select(
                    "div.pagingControls > ul > li.next a")
            while len(next_page_buttons) == 0:
                time.sleep(1)
                retry_count += 1;
                if retry_count > self.max_retry_time: 
                    not_last_page = False
                    print("Assuming the last page found")
                    break
                print("Cannot find the \'next page\' button, retry", 
                        retry_count)
                bs = Company.soup(page, self.head)
                next_page_buttons = bs.select(
                        "div.pagingControls > ul > li.next a")

            for x in bs.findAll('li',{'class',' empReview cf '}):

                # ## PK
                self.result['count'].append(count)
                count += 1

                ## Rev Number
                try:
                    self.result['reviewNo'].append(x.attrs['id'])
                    # revNo.append(x.find('li',{'class':' empReview cf '}).attrs[' id'])
                    # for emp in x.find(':
                    #     print(emp.attrs[' id'])
                except:
                    self.result['reviewNo'].append('None')

                ## location 
                location_span = x.select('span.authorLocation')
                if len(location_span) == 0:
                    self.result['locations'].append('None')
                else:
                    self.result['locations'].append(location_span[0].string)

                ## overall rating
                try:
                    rating = x.find('span',{'class':'rating'})
                    for y in rating:
                        self.result['overallStar'].\
                                append(rating.find(\
                                'span',{'class':'value-title'})\
                                .attrs['title'])
                except:
                    self.result['overallStar'].append('None')

                ## subRatings list
                # Work/Life Balance
                div = x.find('div', string='Work/Life Balance')
                if div == None:
                    self.result['workLifeStar'].append('None')
                else:
                    span = div.next_sibling
                    self.result['workLifeStar'].append(span.attrs['title'])
                # Culture & Values
                div = x.find('div', string='Culture & Values')
                if div == None:
                    self.result['cultureStar'].append('None')
                else:
                    span = div.next_sibling
                    self.result['cultureStar'].append(span.attrs['title'])
                # Career Opportunities
                div = x.find('div', string='Career Opportunities')
                if div == None:
                    self.result['careerOppStar'].append('None')
                else:
                    span = div.next_sibling
                    self.result['careerOppStar'].append(span.attrs['title'])
                # Comp & Benefits
                div = x.find('div', string='Comp & Benefits')
                if div == None:
                    self.result['comBenefitsStar'].append('None')
                else:
                    span = div.next_sibling
                    self.result['comBenefitsStar'].append(span.attrs['title'])
                # Senior Management
                div = x.find('div', string='Senior Management')
                if div == None:
                    self.result['srManagementStar'].append('None')
                else:
                    span = div.next_sibling
                    self.result['srManagementStar'].append(span.attrs['title'])

                ## Date
                try:
                    self.result['date'].append(x.find('time',{'class':'date subtle small'}).text)
                except:
                    self.result['date'].append('None')
                # Summary
                try:
                    summar = x.a.text
                    summar = summar.split('"')
                    self.result['summary'].append(summar[1])
                except:
                    self.result['summary'].append('None')
                ## Pros
                try:
                    self.result['pro'].append(
                            x.find('p',{'class':\
                                    ' pros mainText truncateThis'\
                                    ' wrapToggleStr'}).text)
                except:
                    self.result['pro'].append('None')
                ## Cons
                try:
                    self.result['con'].append(x.find('p',{'class':' cons mainText truncateThis'\
                                    ' wrapToggleStr'}).text)
                except:
                    self.result['con'].append('None')
                ## Advice to Management
                try:
                    self.result['advice'].append(x.find('p',{'class':' adviceMgmt mainText truncateThis'\
                                    ' wrapToggleStr'}).text)
                except:
                    self.result['advice'].append('None')

                ## Employee Type
                try:
                    self.result['employeeType'].append(x.find('span',{'class':"authorJobTitle"}).text)
                except:
                    self.result['employeeType'].append('None')
                ## Position and Location
                try:
                    self.result['position'].append(x.find('p',{'class':' tightBot mainText'}).text)
                except:
                    self.result['position'].append('None')
                ## Review Link
                self.result['reviewLink'].append(self.url+(x.find('a',{'class':'reviewLink'}).attrs['href'])) 

                ## recommendation
                rec = x.find('div', string='Recommends')
                if rec != None:
                    self.result['recommendations'].append('1')
                else:
                    rec = x.find('div', string='Doesn\'t Recommend')
                    if rec != None:
                        self.result['recommendations'].append('-1')
                    else:
                        self.result['recommendations'].append('None')
                ## outlook
                rec = x.find('div', string='Positive Outlook')
                if rec != None:
                    self.result['outlook'].append('1')
                else:
                    rec = x.find('div', string='Neutral Outlook')
                    if rec != None:
                        self.result['outlook'].append('0')
                    else:
                        rec = x.find('div', string='Negative Outlook')
                        if rec != None:
                            self.result['outlook'].append('-1')
                        else:
                            self.result['outlook'].append('None')
                ## CEO
                ceo = x.find(string=ceo_re)
                if ceo != None:
                    div = ceo.parent
                    while(div.name != 'div'):
                        div = div.parent
                    i_tag = div.previous_sibling.find('i')
                    if 'green' in i_tag['class']:
                        self.result['approvals_of_ceo'].append('1')
                    elif 'yellow' in i_tag['class']:
                        self.result['approvals_of_ceo'].append('0')
                    elif 'red' in i_tag['class']:
                        self.result['approvals_of_ceo'].append('-1')
                    else:
                        self.result['approvals_of_ceo'].append('Error')
                else:
                    self.result['approvals_of_ceo'].append('None')
            
            current_index += 1

        return current_index-1

    
    @staticmethod
    def soup(url,headers):
        ''' url = full glassdoor.com/reviews url'''
        session = requests.Session()
        req = session.get(url, headers=headers)
        bs = BeautifulSoup(req.text, 'lxml')
        return bs


