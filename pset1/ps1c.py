#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 16:14:55 2022

@author: amanda
"""

##define function##

def calculate_savings(portion_saved, current_savings, monthly_salary):
    for months in range (0, 36):
        current_savings = current_savings + (current_savings*r/12.0) + \
            (portion_saved * monthly_salary) 
          
        ##provides raise every 6 mos##   
        if ((months + 1) % 6 == 0) :
            monthly_salary = monthly_salary + (monthly_salary * semi_annual_raise)
    
    return current_savings

##define variables##
annual_salary = float(input("Enter your annual salary: "))
portion_saved = 0
total_cost = 1000000.0
semi_annual_raise = 0.07
portion_down_payment = 0.25
current_savings = 0
r = 0.04
monthly_salary = (annual_salary / 12.0)
goal = portion_down_payment * total_cost
steps = 0
high = 10000
low = 0
portion_saved_bisection = ((high + low) / 2) / 10000



##check if it's possible to save in 36 mos##
max_savings = calculate_savings(1.0, current_savings, monthly_salary)

if max_savings < goal:
    print("It is not possible to pay the down payment in three years.")   
    
##function runs until you are within 100 of goal##
while abs(current_savings - goal) >= 100 :
    current_savings = 0.0
    monthly_salary = (annual_salary / 12.0)
    
    current_savings = calculate_savings(portion_saved_bisection, current_savings, monthly_salary)
    print("portion_saved:", portion_saved_bisection)
    
    if (current_savings < goal):
        low = int(portion_saved_bisection * 10000)
    elif (current_savings > goal):
        high = int(portion_saved_bisection * 10000)
    else:
        break
        
    portion_saved_bisection = ((high + low) / 2) / 10000
    steps += 1
    
   
print ("Best savings rate:", portion_saved_bisection)
print ("Steps in bisection search:", steps)
