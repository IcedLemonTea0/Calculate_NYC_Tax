import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd
import os 
import sys
import pandas as pd 

#~~~~~~~~~~~~~~~~~~~~~~ TAX INFO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#Federal Tax 
fed_taxRate= [10,12,22,24,32,35,37]

singleFiler = [0,9700,39475,84200,160725,204100,510300,100000000]
marriedFiler = [0,19400,78950,168400,321450,408200,612350,100000000]

# New York State Tax
NY_SingleTaxRate = [4,4.5,5.25,5.9,6.21,6.49,6.85,8.82]
NY_MarriedTaxRate = [4,4.5,5.25,5.9,6.09,6.41,6.85,8.82]

NY_SingleTaxBracket = [0,8500,11700,13900,21400,80650,215400,1077550,100000000]
NY_MarriedTaxBracket = [0,17150,23600,279000,43000,161550,323200,2155350,100000000]

# New York City Tax
NYC_TaxRate = [3.078,3.762,3.819,3.876]

NYC_SingleTaxBracket = [0,12000,25000,50000,100000000]
NYC_MarriedTaxBracket = [0,21600,45000,90000,100000000]

# Social Security and Medicare Tax (FICA)
ficaSingle = 200000
ficaMarried = 250000

# Dicts
status = {'s':'Single','m':'Married'}
taxBalance = {'Federal Income Tax':0,'Fica':0,'NY State':0,'NYC Tax':0}

#~~~~~~~~~~~~~~~~~~~ CHECK INPUT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def checkInput(grossIncome,filingStatus,retirementContribution):
    
    if filingStatus not in status: #['s','m']:
        raise Exception('Please enter "s" for single filer or "m" for married filer.')

    if isinstance(grossIncome,int) is not True:
        raise Exception('Your income is not numeric.')
        
    if grossIncome < 0:
        raise Exception('Please enter income greater than 0.')
        
    if isinstance(grossIncome, str):
        raise Exception('Please enter a numeric value.')
        
    if isinstance(retirementContribution, str):
        raise Exception('Please enter a numeric value.')
        
    if retirementContribution <0:
        raise Exception('Please enter value greater than 0')

#~~~~~~~~~~~~~~~~~~~~~~~~ USER INPUTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
userInput = sys.argv

print('Hi, we\'ll estimate the taxes you owe for 2019-2020 season.')

if len(userInput) >1:
    filingStatus = userInput[1]
    grossIncome = int(userInput[2])
    retirementContribution = int(userInput[3])
else:
    print('Are you a single or married filer? (s/m): ')
    filingStatus = str(input())
    
    print('What is your gross income?: ')
    grossIncome = int(input())
    
    print('Enter any retirement contribution for this year: ')
    retirementContribution = int(input() or 0)
    
checkInput(grossIncome,filingStatus,retirementContribution)


#~~~~~ DETERMINES USER'S DEDUCTION, TAXABLE INCOME, AND TAX BRACKET ~~~~~~~~~~~

if filingStatus == 's':
    status = status[filingStatus]
    #Federal
    deduction = 12000 + retirementContribution
    taxBracket = singleFiler
    
    #State
    stateDeduction = 8000 + retirementContribution
    stateBracket = NY_SingleTaxBracket
    stateTaxRate = NY_SingleTaxRate
    
    #NYC
    cityBracket = NYC_SingleTaxBracket
    
    #Fica 
    ficaLimit = ficaSingle
    
    
elif filingStatus == 'm':
    status = status[filingStatus]
    #Federal
    deduction = 24400 + retirementContribution
    taxBracket = marriedFiler
    
    #State
    stateDeduction = 16050 + retirementContribution
    
    stateBracket = NY_MarriedTaxBracket
    stateTaxRate = NY_MarriedTaxRate
    
    #NYC 
    cityBracket = NYC_SingleTaxBracket
    
    #Fica
    ficaLimit = ficaMarried

#~~~~~~~~~~~~~~~~~~~~~~~~ CALCULATE TAXES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def calculate_tax(deduction,taxRate,taxBracket,name):
    taxOwe = []
    taxableIncome = grossIncome - deduction
    
    try:
        
        for i in range(len(taxBracket)):
            lowIncome = taxBracket[i]
            highIncome = taxBracket[i+1]
            
            if taxableIncome < 0: # UPDATED 
                taxOwe.append(0)
                break
            
            if taxableIncome > lowIncome and taxableIncome > highIncome:
                taxPaid = (highIncome - lowIncome) * taxRate[i]/100
                taxOwe.append(taxPaid)
                
            if taxableIncome > lowIncome and taxableIncome < highIncome:
                taxPaid = (taxableIncome - lowIncome) * taxRate[i]/100
                taxOwe.append(taxPaid)
                break
            
    except:
        print('Error: 140')
        
    taxOwed = np.round(np.sum(taxOwe),0)
    totalTax = np.round(taxOwed,2)

    return totalTax

def FICA(income):
    
    global ficaLimit
    
    ficaTax = []
    #Calculating Social Security
    if income <= 137700:
        ficaTax.append(income*.062)
    elif income > 137700:
        ficaTax.append(137700*.062)
        
    #Calculating Medicare Tax
    if income < ficaLimit:
        ficaTax.append(income*.0145)
    elif income >= ficaLimit:
        medicareTax = income*.0145
        additionalMedicareTax = (income - ficaLimit) * .009 + medicareTax
        
        ficaTax.append(additionalMedicareTax)
        
    ficaTax = np.sum(ficaTax)
    return ficaTax


taxBalance['Federal Income Tax'] = calculate_tax(deduction,fed_taxRate,taxBracket,'Federal Income Tax')
taxBalance['Fica'] = FICA(grossIncome)
taxBalance['NY State'] = calculate_tax(stateDeduction, stateTaxRate,stateBracket, 'NY State')
taxBalance['NYC Tax'] = calculate_tax(stateDeduction,NYC_TaxRate,cityBracket,'NYC Tax')

# Total tax owed
totalTaxOwed = np.sum(list(taxBalance.values()))

# Effective tax rate
effectiveTaxRate = np.round(totalTaxOwed/grossIncome*100,2) # Effective tax rate

# Creating table
inputTable = pd.DataFrame(data=[filingStatus,grossIncome,retirementContribution],index = ['Filing Status:','Gross Income:','Contribution:'],
                          columns = [' '])
taxBalanceTable = pd.DataFrame(data=list(taxBalance.values()),index=list(taxBalance.keys()),columns=['Tax'])
totalTaxBalanceTable = pd.DataFrame(data=[totalTaxOwed,effectiveTaxRate],index=['Total:','Effective Tax Rate (%):'],columns =[' '])
#~~~~~~~~~~~~~~~~~~~~~~~~ OUTPUT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
print('\n')
print('******** Your estimated tax for the year 2019 - 2020 season ********')
print(inputTable)
print('\n')
print(taxBalanceTable)
print(totalTaxBalanceTable)














