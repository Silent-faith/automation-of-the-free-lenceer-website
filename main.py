#import parameters
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd 



username =  input("please enter your emaill id - ")
password =  input("your password - ") 


driver = webdriver.Chrome('chromedriver.exe')

driver.get("https://www.freelancer.in/login")

sleep(5)

username_input = driver.find_element_by_xpath("//input[@placeholder='Email or Username']")
password_input = driver.find_element_by_xpath("//input[@placeholder='Password']")
login_button =  driver.find_element_by_xpath("//button[@type='submit']")

   
username_input.send_keys(username)
password_input.send_keys(password)
login_button.click()

sleep(20)

driver.get("https://www.freelancer.in/jobs/data-entry/1/?cl=l-en-hi")

source = driver.page_source
data=bs(source, 'html.parser')

Links = data.find_all("h2", class_ = "ProjectTable-title")



df = []
for i in range (len(Links)) :
    try :
        Link_data =  Links[i]
        Link_data = Link_data.find('a')
        url = Link_data.get('href')

        driver.get(url)
        sleep(10) 
        
        
        source = driver.page_source
        data=bs(source, 'html.parser')
        
        headline_data = data.find('div', class_ ="MainContent")
        headline = headline_data.find('span', class_ ="NativeElement ng-star-inserted")
        
        
        
        Id_data = data.find('fl-text', class_ ="ProjectViewDetailsId")
        project_Id = Id_data.find('div', class_ ="NativeElement ng-star-inserted")
        
        
        pay_range_data = data.find('fl-bit', class_ ="ProjectViewDetails-budget")
        pay_range = pay_range_data.find('div', class_ ="NativeElement ng-star-inserted")
        
        
        
        bid = pay_range.getText().split('–')
        
        for i in range(len(bid)) :
            price = bid[i]
            new = ""
            for j in range(len(price)) :
                if price[j] == "." :
                    break
                if price[j].isnumeric() :
                    new += price[j] 
            bid[i] = int(new)
        
        low_bid = bid[0] 
        high_bid = bid[1] 
        
        
        
        bid_amount = driver.find_element_by_id("bidAmountInput")
        bid_amount.clear()
        bid_amount.send_keys(low_bid)
        
        new_df = [project_Id.getText(), headline.getText(), low_bid, url] 
        
        df.append(new_df)
        
    
        description = driver.find_element_by_id("descriptionTextArea")
        description.clear()
        description.send_keys("We have done a lot of data entry work and have good data entry person and a send person will validate also so accuracy will be high.")
        
        
        
        place_bid = driver.find_element_by_xpath("//button[@data-color='secondary']")
        place_bid.click()
        sleep(5)         
    except :
        pass 

df = pd.DataFrame(df, columns= ['project-Id', 'Heading', 'bid_amount', 'url']) 

try : 
    df_intial = pd.read_csv("Bid_data.csv")
    frames = [df, df_intial]
    df = pd.concat(frames, ignore_index=True)
except :
    pass
df.to_csv("Bid_data.csv")
