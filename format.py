# Formatting df value to numerical



def format(list):
    newlist=[]
    posornegnumber = 1
    for text in list:
        if text.endswith(')'):
            text = text[1:-1] # remove the parentheses
            posornegnumber = -1
            
        if text.endswith('%'):
#             Then please make it into comma float
            endtext = float(text[:-1].replace(",",""))/100.0 * posornegnumber 
        elif text.endswith('B'):
#             Then please times 1000000000
#             Change it into integer
            endtext = int(float(text[:-1].replace(",",""))*1000000000)* posornegnumber 
        elif text.endswith('M'):
#             Then please times 1000000
#             Change it into integer
            endtext = int(float(text[:-1].replace(",",""))*1000000)* posornegnumber 
        elif ',' in text:
#             Then please remove the ,
#             Then change it into int
            endtext = int(float(text.replace(",","")))* posornegnumber 

        elif text.endswith('-'):
#             Insert 0
            endtext = 0
        else:
#             change to float
            endtext = float(text)* posornegnumber 
        newlist.append(endtext)
    return newlist   
