import os
import pandas as pd
import pickle
model = pickle.load(open(r"E:\Jupyter Files\RPA Project\loan.bin", 'rb'))

def predict(data):
    final=data.copy(deep=True)
    Semiurban = ['whitefield', 'sarjapur', 'kengeri']
    Urban = ['jayanagar', 'jpnagar','indiranagar']

    data['Property_Area_Semiurban'] = 0
    data['Property_Area_Urban'] = 0
    data['Dependents'] = 0
    
    data = data.drop(['Applicant_Name','Date_of_Birth','Gender->Female','Marital_Status->Single','Education->College_Graduate','Self_Employed->No','Result','File Path',],axis = 1)
    data.columns = ['Gender_Male', 'Married_Yes','Number_of_Dependents->Zero','Number_of_Dependents->One','Number_of_Dependents->Two','Number_of_Dependents->Three_Plus','Education_Not Graduate','Self_Employed_Yes','ApplicantIncome','CoapplicantIncome','Credit_History','Property_Area','LoanAmount','Loan_Amount_Term','Property_Area_Semiurban', 'Property_Area_Urban','Dependents']
    data.replace({'No': 0, 'Yes': 1}, inplace=True)
    data['ApplicantIncome'] = data['ApplicantIncome']//75
    data['LoanAmount'] = data['LoanAmount']//75
    data['CoapplicantIncome'] = data['CoapplicantIncome']//75
    data['Credit_History'] = data['Credit_History']//600
    
    for i, row in data.iterrows():
        if row['Property_Area'].lower() in Semiurban:
            data.loc[i,'Property_Area_Semiurban'] = 1
        elif row['Property_Area'].lower() in Urban:
            data.loc[i,'Property_Area_Urban'] = 1
    for i, row in data.iterrows():
        if row['Number_of_Dependents->Three_Plus'] ==1:
            data.loc[i,'Dependents'] = 3
        elif row['Number_of_Dependents->Two'] ==1:
            data.loc[i,'Dependents'] = 2
        elif row['Number_of_Dependents->One'] ==1:
            data.loc[i,'Dependents'] = 1
    
    data = data.drop(['Number_of_Dependents->Zero','Number_of_Dependents->One','Number_of_Dependents->Two','Number_of_Dependents->Three_Plus','Property_Area'],axis = 1)
    column_names = ['Dependents', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount','Loan_Amount_Term', 'Credit_History', 'Gender_Male', 'Married_Yes','Education_Not Graduate', 'Self_Employed_Yes','Property_Area_Semiurban', 'Property_Area_Urban']
    data = data.reindex(columns=column_names)
    
    result = model.predict(data)
    if result==1:
      final['Loan_Status'] = 'Yes'
    else:
      final['Loan_Status'] = 'No'
    return final
    
    
if __name__=="__main__":
    path=r"E:\RPA\Output\\"
    file_list=[]
    for i in os.listdir(path):
        file_list.append(path+i)
        data = pd.read_csv(path+i)
        f=predict(data)
        f.to_csv(path+i)
    combined_csv = pd.concat([pd.read_csv(f) for f in file_list ])
    combined_csv.to_csv( path+"combined.csv", index=False, encoding='utf-8-sig')
        
        
        

        