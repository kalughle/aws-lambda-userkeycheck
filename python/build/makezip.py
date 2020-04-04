import sys, os, pathlib
from makezip_fnc import CompressFile, UploadZip

# ---------- CONFIG VARIABLES --------------------------------------------------
PROFILE_NAME = 'test01-build'
BUCKETNAME = 'wolf-test01-lambdacode'
LAMBDAFILENAME = 'lambda_function.py'
ZIPFILENAME = 'userkeycheck_lambda.zip'

# ---------- DERIVED VARIABLES -------------------------------------------------
lambdaFileAbs = os.path.dirname(pathlib.Path(__file__).parent.absolute()) + '\\lambda\\' + LAMBDAFILENAME
zipFileAbs = os.path.dirname(pathlib.Path(__file__).absolute()) + '\\' + ZIPFILENAME
targetKeyName = 'python/' + ZIPFILENAME

# ---------- DECISION SECTION --------------------------------------------------
typeAnswer = input('"(C)ompress", "(U)pload" or "(B)oth"?: ').lower()[0]
if typeAnswer == 'c':
    executeCompress = 'y'
    executeUpload = 'n'
elif typeAnswer == 'u':
    profileAnswer = input('Is ' + PROFILE_NAME + ' the corrct Profile? (Y/N): ').lower()[0]
    if profileAnswer == 'y':
        print('Profile correct')
        executeCompress = 'n'
        executeUpload = 'y'
    elif profileAnswer == 'n':
        print('Profile incorrect')
        newProfileAnswer = input('Select a new Profile? (Y/N): ').lower()[0]
        if newProfileAnswer == 'y':
            PROFILE_NAME = input('Please type new Profile name: ')
            executeCompress = 'n'
            executeUpload = 'y'
        else:
            print('Exiting')
            exit()
elif typeAnswer == 'b':
    profileAnswer = input('Is ' + PROFILE_NAME + ' the corrct Profile? (Y/N): ').lower()[0]
    if profileAnswer == 'y':
        print('Profile correct')
        executeCompress = 'y'
        executeUpload = 'y'
    elif profileAnswer == 'n':
        print('Profile incorrect')
        newProfileAnswer = input('Select a new Profile? (Y/N): ').lower()[0]
        if newProfileAnswer == 'y':
            PROFILE_NAME = input('Please type new Profile name: ')
            executeCompress = 'y'
            executeUpload = 'y'
        else:
            print('Exiting')
            exit()
else:
    print('Exiting')
    exit()

# ---------- EXECUTION SECTION -------------------------------------------------
if executeCompress == 'y':
    print('Compress BABY!')
    CompressFile(zipFileAbs, lambdaFileAbs, LAMBDAFILENAME)

if executeUpload == 'y':
    print('Upload BABY!')
    UploadZip(PROFILE_NAME, lambdaFileAbs, BUCKETNAME, targetKeyName)