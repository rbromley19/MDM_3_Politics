import pandas as pd
import numpy as np
import itertools

def listoverlap(list1,list2):
    for i in list1:
        if i in list2:
            
            return True
    return False

df = pd.read_spss('data.sav')
print("extracted")

economy_list = ['deficitReduce','overseasAid','changeEconomy','econGenRetro','econPersonalRetro','economyResponsible','selfPriorities_econ']
enviornment_list = ['climateChange','enviroGrowth','selfPriorities_environment']
immig_list = ['immigCultural','immigSelf','changeImmig','immigEcon','controlImmig']
health_list = ['selfPriorities_nhs','effectsEUNHS','changeNHS']
brexit_list = ['EUIntegrationSelf','cantLiveWithEU_1','cantLiveWithEU_2','cantLiveWithEU_3','cantLiveWithEU_4','selfPriorities_brexit','euRefVote','dealVremain','remainVnodeal','effectsEUUnemployment','effectsEUTrade','effectsEUImmigration','effectsEUTerror','effectsEUEcon','dealGoodBad','happyEULeave','euID','euRefDoOver','cancelBrexit']


total_list = [economy_list,enviornment_list,immig_list,health_list,brexit_list]
flat_list = [item for l in total_list for item in l]
flat_list.insert(0,'partyId')

extracted_data = df.loc[:,flat_list]
extracted_data.columns= extracted_data.columns.str.strip().str.lower()

for col in extracted_data.columns:
    try:
        extracted_data[col] = extracted_data[col].fillna("Don't know")#we should centre our numerical stuff about 0
    except:
        print(col)
extracted_data['remainvnodeal'] = extracted_data['remainvnodeal'].replace(9999.0, "Don't know") 
extracted_data['remainvnodeal'] = extracted_data['remainvnodeal'].fillna("Don't know")
originaldata = extracted_data  

linguisticprefixes = ['Strongly',"much","lot","little","bad","good","very","extremely","neither","higher","lower","moderate","absolutely", 'worse', 'better', 'about the same','A little',"Enriches","Undermines"]
problemwords = ["not","disagree"]

extracted_data = originaldata

colnames = []
for i in originaldata.columns:
    colnames.append(str(i))
#print(colnames)

orderedcolumns = []
columnsneedmanualsorting = []
onehotable = colnames#assumes all can be 1 hotted in beggining
    

alreadynumeric = []
onehotablec = onehotable
#checks if answers already in numerical form
for col in onehotable:
   
    count = 0
    for i in extracted_data[col]:
        i=str(i)
        if i.isdigit() or "."  in i:#is digit removes ints . removes floats if someones put a . in there written answer fuckem
            #print(i)
            onehotablec.remove(col)
            alreadynumeric.append(col)
            
            break
        count+=1
        if count > 300:
            break

onehotable = onehotablec
numericandtext = []

"""
print("------------------------------------------------\n\n")
n=0
for col in alreadynumeric:
    #print(col)
    for data in extracted_data[col]:
        data = str(data)
        n+=1
        if not data.isdigit and not "." in data:
            print(n)
            break
            print("reeeeeeee")
"""
print("------------------------------------------------\n\n")
n=0

print(alreadynumeric)
alreadynumericc = alreadynumeric
listtoremove = []
for col in list(alreadynumericc):#col colnames of collums with numbers
    print(col)
    #print(n)
    n+=1
    col =col.lower().strip()
    count = 0

    
    for i in extracted_data[col]:
        i=str(i)
        print("iter: "+str(count))
        if not i.isdigit() and not "."  in i:#if not digit must contain both
            #print(col)
            print(i)
            alreadynumeric.remove(col)
            
            numericandtext.append(col)
            #print(col)
            break
            
            
        count+=1
        
        

#alreadynumeric = alreadynumericc

print("------------------------------------------------\n\n")





for col in numericandtext:
    numericcol = []
    textcol = []
    for i in extracted_data[col]:
        i=str(i)
        if i.isdigit() or "."  in i:
            #print(i)
            
            numericcol.append(i)
            textcol.append("Don't know")
        else:
            numericcol.append("5")
            textcol.append(i)
    #print(extracted_data.columns)
    extracted_data.drop(columns = col)
    onehotable.append(col+"_text")
    extracted_data[col+"_text"]=textcol
    alreadynumeric.append(col+"_numeric")
    extracted_data[col+"_numeric"] = numericcol
    
    


for col in colnames:
    
    count=0
    for i in extracted_data[col]:
        i=str(i).lower()
        
        if(listoverlap(i.split(),linguisticprefixes)):#checks for overlap between lists
            
            orderedcolumns.append(col)
            onehotable.remove(col)#if needs sorting cannot be 1 hotted
            break#break if found atleast one instance of words that need ordering
        count+=1
        if count> 1000:
            break

orderedcolumnsc = orderedcolumns
for col in orderedcolumns:
    for k in extracted_data[col]:
        k=str(k).lower()
        if listoverlap(k.split(),problemwords):
            orderedcolumnsc.remove(str(col))
            columnsneedmanualsorting.append(col)
            break
        
            #if data contains problem words algorithm wont work so we need to sort it manually
            #simplest example is not
            #very very good > very good
            #but very very very not good > very very good
            #could maybe solve with a -1 term somwhere seems to complicated though
                
orderedcolumns = orderedcolumnsc             

print("can probably be sorted:")
print(orderedcolumns)
print("gonna require manual sorting:")
print(columnsneedmanualsorting)
print("can be 1 hot encoded:")
print(onehotable)
print("already numeric")
print(alreadynumeric)


        