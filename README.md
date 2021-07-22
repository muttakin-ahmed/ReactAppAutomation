# React App Automation with Python 3 and Selenium WebDriver

This repository contains an automation script for the following balancing game, hosted in http://ec2-54-208-152-154.compute-1.amazonaws.com/.
Python 3 is used to write the Selenium WebDriver automation code, so to run this code, the user must have both Python 3.x.x and selenium library installed in the intended system. For browser, I have used Chrome. For Selenium to access chrome, chromedriver is required. Please check the following links for the installation and setup.
1. Installing Python: https://www.python.org/downloads/
2. Installing Selenium: https://selenium-python.readthedocs.io/
3. Chromedriver: https://sites.google.com/a/chromium.org/chromedriver/downloads

For chromedriver to work, the correct path of it should be mentioned in the code. I have written a comment where the user should enter the correct path of chromedriver in the machine.

### Solution observations:
I have a couple of possible solutions for this game. I will write my observations of these solutions in this section.

**1. Basic Solution:** In this solution, I have not used the weighing feature at all. I did that because it is simpler to just look for a fake bar on the list of bars, rather than weighing and calculating. It is a linear solution, so the runtime will increase once the list size is increased. It is a good solution in terms of runtime, but it misses the important features and not a smart solution if we are thinking of test coverage. The method name of this solution is "basicSolution()"

**2. Intermediate solution:** I have used the feature of weighing the bars in this solution. After testin, I came up with the ways of weighing multiple bars each side. In the automation script, however, 1 each side and 2 each side has been implemented.
One of the ways to solve this game is to check all the bars in a 1-on-1 combination, but it will have a runtime of n^2 in the worst case. Instead, I tried a different approach to solve this game, which I can describe in the following manner.

  1. Check 1 bar each side the first time. If they are unequal, then we have the fake bar (the one which is lighter)
  2. If they are equal, I have checked 2 bars each side *in a loop*, where I used the 1-on-1 bars each side and weighed other bars from the list. All equal results are added in a database so that we keep track of the original bars.
  3. If any of these 2-on-2 results are inequal, we have to check which bar is not on the list of original bars.
  4. I have clicked on these bars to find out the fake bar.
