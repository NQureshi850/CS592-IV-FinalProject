import pandas as pd

frackingData = pd.read_csv('FracFocusRegistry_20171004.csv')
#frackingData = pd.read_csv('subsetFracking.csv')
#print(frackingData['JobStartDate'])
combinedFracking = pd.DataFrame()
subsetData1 = frackingData[70:500]
#print(subsetData1['JobStartDate'])
subsetData2 = frackingData[700:40000]
#print(subsetData2['JobStartDate'])
subsetData3 = frackingData[100000:140000]
#print(subsetData3['JobStartDate'])
subsetData4 = frackingData[1100000:1140000]
#print(subsetData4['JobStartDate'])
subsetData5 = frackingData[2000000:2040000]
#print(subsetData5['JobStartDate'])
subsetData6 = frackingData[2800000:2840000]
#print(subsetData6['JobStartDate'])

combinedFracking = pd.concat([subsetData1, subsetData2, subsetData3, subsetData4, subsetData5, subsetData6], ignore_index=True)
#print(combinedFracking)
#subsetData.to_csv('subsetFracking2.csv')

combinedFracking = combinedFracking.drop(columns=['UploadKey', 'APINumber', 'Projection', 'TVD', 'TotalBaseNonWaterVolume',
                            'FFVersion', 'FederalWell', 'IndianWell', 'Source', 'DTMOD', 'PurposeKey',
                            'TradeName', 'Supplier', 'Purpose', 'SystemApproach', 'IsWater', 'PurposePercentHFJob',
                            'PurposeIngredientMSDS', 'IngredientKey', 'IngredientName', 'CASNumber', 'PercentHighAdditive',
                            'PercentHFJob', 'IngredientComment', 'IngredientMSDS', 'MassIngredient', 'ClaimantCompany', 'DisclosureKey',
                            'tox_recognized', 'tox_suspected'])
combinedFracking = combinedFracking.dropna()
print(combinedFracking)

combinedFracking.to_csv('subsetFracking.csv')
