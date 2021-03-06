import datetime
import math
import sys

inFile_percent = sys.argv[1]
inFile_data = sys.argv[2]
outFile = sys.argv[3]

CMTE_ID = 0  #Set columns for input
NAME = 7
ZIP_CODE = 10
TRANSACTION_DT = 13
TRANSACTION_AMT = 14
OTHER_ID = 15
YEAR = 2018 #change for calendar year desired

contributions = {}  
recipient_cont = {}
pr = {}
percentile = 0

with open(inFile_percent, 'r') as percentile_file:
    percentile = int(percentile_file.read())

output = open(outFile, 'w')    

with open(inFile_data, 'r') as input_file:
    for line in input_file.readlines():
        contents = line.split('|')

        
        if contents[OTHER_ID]:
            continue 
        if not contents[CMTE_ID]:
            continue
        if not contents[NAME]:
            continue
        if not contents[TRANSACTION_DT]:
            continue
        if not contents[TRANSACTION_AMT]:
            continue
        if not contents[ZIP_CODE] or contents[ZIP_CODE]<5:
            continue

        cmte_id = contents[CMTE_ID]
        name = contents[NAME]
        zip_code = contents[ZIP_CODE]
        zip_code = zip_code[:5]
        transaction_dt = contents[TRANSACTION_DT]
        transaction_amt = float(contents[TRANSACTION_AMT])
        
        if not transaction_dt:
            continue
        try:
            month = int(transaction_dt[:2])
            day = int(transaction_dt[2:4])
            year = int(transaction_dt[4:])
            transaction_dt = datetime.date(year, month, day)
        except:
            continue
      
        unique_id = name + zip_code
        cmte_zip = cmte_id+zip_code
        if unique_id not in contributions:
            contributions[unique_id] = []
            contributions[unique_id].append((cmte_id, transaction_amt, transaction_dt))
        else:
            contributions[unique_id].append((cmte_id, transaction_amt, transaction_dt))
            if cmte_zip not in recipient_cont:
                recipient_cont[cmte_zip] = []
            if transaction_dt.year==YEAR:
                recipient_cont[cmte_zip].append(transaction_amt)
                percentile_index = (percentile / 100.0) * len(recipient_cont[cmte_zip])
                percentile_index = int(percentile_index)  #not rounding up as our index starts at 0
              
                output.writelines(cmte_zip + '|'+ zip_code + "|"+ str(transaction_dt.year) +"|"+ str(sorted(recipient_cont[cmte_zip])[percentile_index]) + "|" + str(sum(recipient_cont[cmte_zip])) + '|'+ str(len(recipient_cont[cmte_zip])) + '\n')
      
output.close()


