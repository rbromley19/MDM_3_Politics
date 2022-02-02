from numpy import extract
import pandas as pd



def extract_data(input_name,output_name,output_or_return):   
    #create_file_names
    input_file = str(input_name)+'.sav'
    output_file = str(output_name)+'.csv'
    
    #open the whole data set + must be spss
    df = pd.read_spss(input_file)
    
    #lists of questions, more can be added or taken away easily - be careful when adding that the name exists in the text file
    economy_list = ['deficitReduce','overseasAid','changeEconomy','econGenRetro','econPersonalRetro','economyResponsible','selfPriorities_econ']
    enviornment_list = ['climateChange','enviroGrowth','selfPriorities_environment']
    immig_list = ['immigCultural','immigSelf','changeImmig','immigEcon','controlImmig']
    health_list = ['selfPriorities_nhs','effectsEUNHS','changeNHS']
    brexit_list = ['EUIntegrationSelf','cantLiveWithEU_1','cantLiveWithEU_2','cantLiveWithEU_3','cantLiveWithEU_4','selfPriorities_brexit','euRefVote','dealVremain','remainVnodeal','effectsEUUnemployment','effectsEUTrade','effectsEUImmigration','effectsEUTerror','effectsEUEcon','dealGoodBad','happyEULeave','euID','euRefDoOver','cancelBrexit']
    
    #join list together and flaten for use in pandas, adding the partyiD as a label
    total_list = [economy_list,enviornment_list,immig_list,health_list,brexit_list]
    flat_list = [item for l in total_list for item in l]
    flat_list.insert(0,'partyId')
  
    
    extracted_data = df.loc[:,flat_list]
    
    #cleaning the data, removing the null values and replacing with 'Don't know', this was checked properly and so there are no additional values
    extracted_data['remainVnodeal'] = extracted_data['remainVnodeal'].replace(9999.0, "Don't know") 
    extracted_data['remainVnodeal'] = extracted_data['remainVnodeal'].fillna("Don't know")
    extracted_data['dealVremain'] = extracted_data['dealVremain'].fillna("Don't know")
    extracted_data['euRefVote'] = extracted_data['euRefVote'].fillna("Don't know")
    extracted_data['selfPriorities_nhs'] = extracted_data['selfPriorities_nhs'].fillna("Don't know")
    extracted_data['selfPriorities_brexit']=extracted_data['selfPriorities_brexit'].fillna("Don't know")
    extracted_data['deficitReduce'] = extracted_data['deficitReduce'].fillna("Don't know")
    extracted_data['selfPriorities_econ'] = extracted_data['selfPriorities_econ'].fillna("Don't know")
    extracted_data['climateChange'] =  extracted_data['climateChange'].fillna("Don't know")
    extracted_data['selfPriorities_environment'] = extracted_data['selfPriorities_environment'].fillna("Don't know")
    
    
    #0 for file output 1 for return
    if output_or_return ==0:
        extracted_data.to_csv(output_file)
    elif output_or_return == 1:
        return extracted_data
    else:
         raise Exception("Input should be 0 for file output or 1 for return")
     
#example usage
#make sure you have the sav file downlaoded
#extract_data('data','extracted_data',0)
    
    