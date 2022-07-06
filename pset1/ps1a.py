#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 15:01:53 2022

@author: amanda
"""

##prompt user for inputs

annual_salary = float(input("Enter your annual salary: "))
portion_saved = float(input("Enter the percent of your salary to save, " 
                            "as a decimal: "))
total_cost = float(input("Enter the cost of your dream home: "))

##variables

portion_down_payment = 0.25
current_savings = 0
r = 0.04
monthly_salary = (annual_salary / 12.0)

##function

months = 0

while current_savings < (portion_down_payment * total_cost):
    current_savings = current_savings + (current_savings*r/12.0) + (portion_saved * monthly_salary)
    months += 1
   
print ("Number of months:", months)
    

    
    
    
