def CompressFile (zipFileAbs, lambdaFileAbs, LAMBDAFILENAME):
    import sys
    from zipfile import ZipFile
    
    try:
        # writing files to a zipfile 
        with ZipFile(zipFileAbs,'w') as zip: 
            # writing each file one by one 
            zip.write(lambdaFileAbs, LAMBDAFILENAME)
            zip.close()
    except:
        print("An Unexpected Error Occured!!")
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])


def UploadZip (PROFILE_NAME, zipFileAbs, BUCKETNAME, targetKeyName):
    import sys, boto3
    
    try:
        # Create the session using the designated profile (DELETE FOR LAMBDA!!)
        session = boto3.session.Session(profile_name=PROFILE_NAME)
        s3Client = session.client('s3')

        with open(zipFileAbs, 'rb') as data:
            s3Client.upload_fileobj(data, BUCKETNAME, targetKeyName)
    except:
        print("An Unexpected Error Occured!!")
        print(sys.exc_info()[0])
        print(sys.exc_info()[1])