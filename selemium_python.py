from selenium import webdriver
import time
import random
from selenium.webdriver.common.keys import Keys

ob = []
fake = None

# Method for parsing the html text and finding out the result from Weighing Table
def parse_list(s):
    arr = []
    for ch in list(s):
        if ch.isnumeric():
            arr.append(int(ch))
    return arr

# method for comparing the bars
def compare_results(s):
    global fake
    # equal bars
    if "=" in s:
        bars = s.split("=")
        for bar in bars:
            bar_num = parse_list(bar)
            for b in bar_num:
                if b not in ob:
                    ob.append(b)

    # unequal bars
    elif "<" in s:
        bars = s.split("<")
        bar_left = parse_list(bars[0])
        bar_right =parse_list(bars[1])
        if len(bar_right) == 1:
            fake = bar_left[0]
        else:
            for b in bar_left:
                if b not in ob:
                    compare_fake(b)
                    
    elif ">" in s:
        bars = s.split(">")
        bar_left = parse_list(bars[0])
        bar_right = parse_list(bars[1])
        if len(bar_right) == 1:
            fake = bar_right[0]
        else:
            for b in bar_right:
                if b not in ob:
                    compare_fake(b)
                        
# checking the fake bar after an inequality has been found
def compare_fake(b):
    global fake
    coin_id = "coin_" + str(b)
    driver.find_element_by_id(coin_id).click()
    if driver.switch_to.alert.text == "Yay! You find it":
        fake = b
    time.sleep(5)
    driver.switch_to.alert.accept()

# Checking if inequality has been found or not
def check_fake():
    if fake is not None:
        fake_button = driver.find_element_by_id("coin_" + str(fake))
        fake_button.click()
        assert driver.switch_to.alert.text == "Yay! You find it!"
        driver.switch_to.alert.accept()
        time.sleep(10)
        return True
    else:
        time.sleep(5)
        return False

# This is the path for chromedriver on my machine. User needs to put his/her path for the execution of this code.
driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe")
driver.get("http://ec2-54-208-152-154.compute-1.amazonaws.com/")

left_bowl_0 = driver.find_element_by_id("left_0")
right_bowl_0 = driver.find_element_by_id("right_0")
left_bowl_1 = driver.find_element_by_id("left_1")
right_bowl_1 = driver.find_element_by_id("right_1")
weigh_button = driver.find_element_by_id("weigh")
reset_button = driver.find_element_by_xpath("//button[contains(text(),'Reset')]")

gameinfo_div = driver.find_element_by_class_name("game-info")
ol = gameinfo_div.find_element_by_xpath("//body/div[@id='root']/div[1]/div[1]/div[5]/ol[1]")

# Basic solution
# Just click on the bars one by one and find out the fake one
# This is done without even using the balance
# this is a linear process which has better runtime than my other solutions
def basicSolution():
    for i in range(9):
        coin = driver.find_element_by_id("coin_" + str(i))
        coin.click()
        if driver.switch_to.alert.text == "Yay! You find it!":
            print("the fake bar is " + str(i))
            
        elif driver.switch_to.alert.text == "Oops! Try Again!":
            print(str(i) + " is not fake.")

        driver.switch_to.alert.accept()
        time.sleep(5)
    driver.close()
        

# Solution level 1
# We are weighing a couple of bars 1 on 1 and finding out which is the fake bar
def check_bars_1on1(bar1, bar2):
    left_bowl_0.send_keys(bar1)
    right_bowl_0.send_keys(bar2)
    weigh_button.click()
    time.sleep(5)

    # get result for 1 on 1
    results = ol.find_elements_by_tag_name("li")
    compare_results(results[0].text)

# After one 1 on 1 comparison, we are going to do 2 bars on 2 bars weighing.
def check_bars_2on2(bar1, bar2, bar3, bar4):
    left_bowl_0.send_keys(bar1)
    left_bowl_1.send_keys(bar2)
    right_bowl_0.send_keys(bar3)
    right_bowl_1.send_keys(bar4)
    weigh_button.click()
    time.sleep(5)
    # get result for 2 on 2 weighing
    results = ol.find_elements_by_tag_name("li")
    for r in results:
         compare_results(r.text)

def weighing_bar():
    # invoking 1 bar at each side
    bars = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    bar1 = random.choice(bars)
    bar2 = random.choice([ele for ele in bars if ele != bar1])

    check_bars_1on1(bar1, bar2)
    if check_fake():
        print(fake)
        time.sleep(4)
        driver.close()
    print(ob)
    
    reset_button.click()

    # weighing 2 bars on each side on a loop, in case we don't find the fake bar in the first couple of cycles.
    for i in range(5):
        bar3 = random.choice([ele for ele in bars if ele != bar1 and ele != bar2])
        bar4 = random.choice([ele for ele in bars if ele != bar1 and ele != bar2 and ele != bar3])

        check_bars_2on2(bar1, bar3, bar2, bar4)

        if check_fake():
            print(str(fake) + " is the fake bar.")
            time.sleep(4)
            driver.close()
        reset_button.click()

weighing_bar()
driver.close()
