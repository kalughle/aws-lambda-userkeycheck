import sys, os, pathlib
from zipfile import ZipFile

# ---------- CONFIG VARIABLES --------------------------------------------------
LAMBDAFILENAME = 'lambda_function.py'
ZIPFILENAME = 'userkeycheck_lambda.zip'

# ---------- DERIVED VARIABLES -------------------------------------------------
lambdaFileAbs = os.path.dirname(pathlib.Path(__file__).parent.absolute()) + '\\lambda\\' + LAMBDAFILENAME
zipFileAbs = os.path.dirname(pathlib.Path(__file__).absolute()) + '\\' + ZIPFILENAME

# ---------- EXECUTION SECTION -------------------------------------------------
try:
    # writing files to a zipfile 
    with ZipFile(zipFileAbs,'w') as zip: 
        # writing each file one by one 
        zip.write(lambdaFileAbs, LAMBDAFILENAME)
        zip.close()
    
    print('File "' + LAMBDAFILENAME + '" compressed as "' + ZIPFILENAME + '" and copied to "' + zipFileAbs + '"')
except:
    print("An Unexpected Error Occured!!")
    print(sys.exc_info()[0])
    print(sys.exc_info()[1])