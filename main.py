# import requests
# from bs4 import BeautifulSoup
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
# }
#
# URL = "https://connect2concepts.com/connect2/?type=circle&key=2A2BE0D8-DF10-4A48-BEDD-B3BC0CD628E7/"
# r = requests.get(URL, headers=headers)
#
# soup = BeautifulSoup(r.content, "html.parser")
#
# print(soup.prettify())

# import requests
# from requests_html import HTMLSession
# session = HTMLSession()
#
# r = session.get('https://python.org/')

import math
import random
import time

import pymysql
from datetime import date, datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def add_capacity(a_date, a_dow, a_interval, a_a1, a_a2, a_a3, a_a4, a_a5, a_a6):
    cur = cnx.cursor()
    sql_register = "CALL add_capacity(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

    data = (a_date, a_dow, a_interval, a_a1, a_a2, a_a3, a_a4, a_a5, a_a6)

    try:
        cur.execute(sql_register, data)
    except pymysql.err.OperationalError as err:
        print("Adding capcity entry failed")
    print("Successfully added capacity entry to database")
    cnx.commit()
    cur.close()

def add_avg(id, a_a1, a_a2, a_a3, a_a4, a_a5, a_a6):
    cur = cnx.cursor()
    sql_register = "CALL add_avg(%s,%s,%s,%s,%s,%s,%s,%s)"

    data = (id, a_a1, a_a2, a_a3, a_a4, a_a5, a_a6, 1)

    try:
        cur.execute(sql_register, data)
    except pymysql.err.OperationalError as err:
        print("Adding capcity entry failed")
    print("Successfully added capacity entry to database")
    cnx.commit()
    cur.close()


def read_avg(r_iid):
    cur = cnx.cursor()
    sql_register = "SELECT * FROM capacity_avg WHERE iid = %s"
    try:
        cur.execute(sql_register, r_iid)
        return cur.fetchone()

    except pymysql.err.OperationalError as err:
        print("Reading average failed")

    print("Successfully reading average from database")
    cnx.commit()
    cur.close()


def update_avg(u_id, u_avg1, u_avg2, u_avg3, u_avg4, u_avg5, u_avg6):
    cur = cnx.cursor()
    sql_register = "CALL update_avg(%s,%s,%s,%s,%s,%s,%s)"

    data = (u_id, u_avg1, u_avg2, u_avg3, u_avg4, u_avg5, u_avg6)

    try:
        cur.execute(sql_register, data)
    except pymysql.err.OperationalError as err:
        print("Updating average failed")
    print("Successfully updated average and pushed to database")
    cnx.commit()
    cur.close()

def init_random():
    for x in range (673):
        random1 = random.randrange(0,105)
        random2 = random.randrange(0, 60)
        random3 = random.randrange(0, 65)
        random4 = random.randrange(0, 90)
        random5 = random.randrange(0, 20)
        random6 = random.randrange(0, 55)
        add_avg(x, random1, random2, random3, random4, random5,random6)

# url of the page we want to scrape
url = "https://connect2concepts.com/connect2/?type=circle&key=2A2BE0D8-DF10-4A48-BEDD-B3BC0CD628E7"

# initiating the webdriver. Parameter includes the path of the webdriver.
driver = webdriver.Chrome('./chromedriver')
driver.get(url)

# this is just to ensure that the page is loaded
time.sleep(1)

html = driver.page_source

# this renders the JS code and stores all
# of the information in static HTML code.

# Now, we could simply apply bs4 to html variable
soup = BeautifulSoup(html, "html.parser")

capacities = []

# appending the fullness of each of the on campus locations
for element in driver.find_elements_by_class_name('cir'):
    capacities.append(element.text.replace('%', ''))

#print(capacities)
driver.close()  # closing the webdriver

try:
    cnx = pymysql.connect(
        host='localhost',
        user='root',
        password="94943546m",
        db='cal',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    loginSuccessful = True
except pymysql.err.OperationalError as err:
    print("Incorrect login please try again")

today = date.today()
date = today.strftime("%d/%m/%y")
dow = today.weekday()

fmt = '%Y-%m-%d %H:%M:%S'
datetime_start = datetime.strptime('2022-02-07 00:00:00', fmt)
datetime_now = datetime.today()

cur_total_interval = math.floor((datetime_now - datetime_start).total_seconds() / 900)

#print(date, dow, cur_total_interval, capacities[0], capacities[1], capacities[2], capacities[3], capacities[4], capacities[5])

add_capacity(date, dow, cur_total_interval, capacities[0], capacities[1], capacities[2], capacities[3], capacities[4],
             capacities[5])

cur_interval = cur_total_interval % 672

capacity_avg = read_avg(cur_interval)

num_entries_new = capacity_avg.get('num_entries') + 1
avg_r1_new = (capacity_avg.get('avg_r1') + int(capacities[0]))/num_entries_new
avg_r2_new = (capacity_avg.get('avg_r2') + int(capacities[1]))/num_entries_new
avg_r3_new = (capacity_avg.get('avg_r3') + int(capacities[2]))/num_entries_new
avg_r4_new = (capacity_avg.get('avg_r4') + int(capacities[3]))/num_entries_new
avg_r5_new = (capacity_avg.get('avg_r5') + int(capacities[4]))/num_entries_new
avg_r6_new = (capacity_avg.get('avg_r6') + int(capacities[5]))/num_entries_new

update_avg(cur_interval, avg_r1_new, avg_r2_new, avg_r3_new, avg_r4_new, avg_r5_new, avg_r6_new)

####################################
# Sean's Code

# Data Initialization
user_hours = input("input your desired workout length in hours: ")
# multiplies the desired number of hours by 4 to turn it into number
# of 15 minute time blocks (to work with dan's data)
user_blocks = math.ceil(float(user_hours) * 4)
length = int(user_blocks)
time = input("Enter your preferred time of day: ")
day = input("input what day of the week you would like: ")
fc = input("input what fitness center you would like: ")
#print(length)

# In[2]:


# Takes the day as a string from devanshi's UI and turns it into a readable day value in dan's database
days_dict = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
cur_day = days_dict[day]
#print(cur_day)

# In[3]:


# Takes the time of day as a string from devanshi's UI and turns it into a readable day value in dan's database
time_of_day = {"Morning": 24, "Afternoon": 48, "Evening": 72, "Night": 84}
cur_time = time_of_day[time]
if time == "Morning":
    end_time = 47
elif time == "Afternoon":
    end_time = 71
elif time == "Evening":
    end_time = 83
else:
    end_time = 92
#print(cur_time)

# In[4]:


# Takes the specific fitness center the user prompts from devanshi's UI
# and turns it into a readable day value in dan's database
fc_dict = {"MC2": "avg_r1", "MCG": "avg_r2", "MC3": "avg_r3", "MCW": "avg_r4", "MCT": "avg_r5", "SB4": "avg_r6"}
fitness_center = fc_dict[fc]
#print(fitness_center)

# In[5]:


# takes in dan's database, filters out unnecessary values based on
# what day of the week we are prompted, and what time of day.
start_val = cur_day * 96
end_val = (cur_day + 1)*96
dans_hash = {}
for i in range(start_val, end_val):
    hm = read_avg(i)
    dans_hash[i%96] = hm.get(fitness_center)

print(dans_hash)
# In[15]:


# Initializing a random table of times to their respective crowd scores, and a table of
# times the user is busy (just to test with)

#times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#scores = [3.3, 2.2, 9.8, 4.1, 6.4, 7.3, 2.4, 2.6, 3.9, 1.1, 2.6]
#dict1 = {times[i]: scores[i] for i in range(len(times))}

#bad_start_times = [.7, 1.3]
#start_times = [0] * len(bad_start_times)

#for i in range(len(bad_start_times)):
#    start_times[i] = math.ceil(bad_start_times[i] * 4)

#lengths = [.75, .9]

#bad_lengths = [0] * len(lengths)
#for i in range(len(lengths)):
#    bad_lengths[i] = math.ceil(lengths[i] * 4)

#print(start_times)
#print(bad_lengths)
#bad_times = {start_times[j]: bad_lengths[j] for j in range(len(start_times))}
#print(bad_times)

times = list(dans_hash.keys())
#print(times)
scores = list(dans_hash.values())
#print(scores)
dict1 = {times[i]: scores[i] for i in range(len(times))}

#bad_start_times = [.7, 1.3]
#start_times = [0] * len(bad_start_times)

#for i in range(len(bad_start_times)):
#    start_times[i] = math.ceil(bad_start_times[i] * 4)

#lengths = [.75, .9]

#bad_lengths = [0] * len(lengths)
#for i in range(len(lengths)):
#    bad_lengths[i] = math.ceil(lengths[i] * 4)

#print(start_times)
#print(bad_lengths)
#bad_times = {start_times[j]: bad_lengths[j] for j in range(len(start_times))}
#print(bad_times)

# # The acutal Algorithm:

# In[16]:


# initializes return values
score = 0
retval = {}
for i in range(length):
    score += dict1[i]

avg = score / length
retval[0] = avg
#print(retval)

# In[17]:


# algorithm calculates average scores for a certain length time block at any possible point in thee day
for i in range(1, len(scores) - length + 1):
    mid = (avg * length) - scores[i - 1]
    avg = (mid + scores[i + length - 1]) / length
    retval[i] = round(avg, 3)

#for i in range(24):
#    retval.pop(i)
#print(retval)

for i in reversed(range(len(retval))):
    if not (i >= cur_time and i <= end_time):
        retval.pop(i)

maxKey = max(retval, key = retval.get)
bestTime = str(int(maxKey/4)) + ":" + str(maxKey*15 % 60).zfill(2)
print("Your optimal gym time today is: " + bestTime)

# In[18]:


# filters out possible optimal times based on whether they clash
# with existing scheduled items from devanshi's UIs

#num_bad_times = len(bad_times.keys())
#print(start_times[0])

#for i in reversed(range(num_bad_times)):
#    print(i)
#    for j in reversed(range(bad_lengths[i])):
#        print(j)
#        if start_times[i] + j < len(retval.keys()):
#            retval.pop(start_times[i] + j)
#print(retval)

cnx.close()
