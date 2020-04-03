import sys, os, pathlib
from zipfile import ZipFile

SOURCEFILENAME = 'lambda\\lambda_function.py'
TARGETFILENAME = 'finalzip\\userkeycheck_lambda.zip'

parentDir = os.path.dirname(pathlib.Path(__file__).parent.absolute()) + '\\'
sourceFile = parentDir + SOURCEFILENAME
targetFile = parentDir + TARGETFILENAME

try:
    # writing files to a zipfile 
    with ZipFile(targetFile,'w') as zip: 
        # writing each file one by one 
        zip.write(sourceFile)
except:
   print("An Unexpected Error Occured!!")
   print(sys.exc_info()[0])
   print(sys.exc_info()[1])