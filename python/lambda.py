import json

def lambda_handler(event, context):
    import boto3, datetime
    from datetime import timedelta, date
    from botocore.exceptions import ClientError
    
    # ---------- GLOBAL VARIABLES ----------------------------------------------------------------------
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_SES_REGION = "us-west-2"
    
    # Email sender information
    SENDER_ADDRESS = "Lambda Alert <lambdaalert@wolfbrigade.org>"
    
    # This should be the common IAM or Cloud alert address
    MAIN_RECIPIENT = "kalughle@gmail.com"
    
    # ==================================================================================================
    # Define the email function
    def sendSesEmail(USERNAME, ACCESSKEY, CREATEDON, EXPIRESON, DAYSLEFT):
        # The character encoding for the email.
        CHARSET = "UTF-8"
        
        # The subject line for the email.
        SUBJECT = "Expired User Alert!"
    
        # The email body for recipients with non-HTML email clients.
        BODY_TEXT = (
            "The AccessKey for the user {USERNAME} will expire in {DAYSLEFT} days\r"
            "\r"
            "UserName:  {USERNAME}\r"
            "AccessKey: {ACCESSKEY}\r"
            "CreatedOn: {CREATEDON}\r"
            "ExpiresOn: {EXPIRESON}\r"
            "DaysLeft:  {DAYSLEFT}"
                    ).format(USERNAME=USERNAME, ACCESSKEY=ACCESSKEY, CREATEDON=CREATEDON, EXPIRESON=EXPIRESON, DAYSLEFT=DAYSLEFT)
                    
        # The HTML body of the email.
        BODY_HTML = """<html>
        <head></head>
        <body>
            <h1>The AccessKey for the user {USERNAME} will expire in {DAYSLEFT} days</h1>
            <p>
            <br><b>UserName</b>:  {USERNAME}
            <br><b>AccessKey</b>: {ACCESSKEY}
            <br><b>CreatedOn</b>: {CREATEDON}
            <br><b>ExpiresOn</b>: {EXPIRESON}
            <br><b>DaysLeft</b>:  {DAYSLEFT}
            </p>
        </body>
        </html>
                    """.format(USERNAME=USERNAME, ACCESSKEY=ACCESSKEY, CREATEDON=CREATEDON, EXPIRESON=EXPIRESON, DAYSLEFT=DAYSLEFT)
    
        # Create a new SES resource and specify a region.
        sesClient = boto3.client('ses',region_name=AWS_SES_REGION)

        #Provide the contents of the email.
        response = sesClient.send_email(
            Destination={
                'ToAddresses': [
                    MAIN_RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER_ADDRESS,
        )
    
    # ==================================================================================================
    # Execution
    # Set the client. Should be "boto3.client('iam') for Lambda
    iamClient = boto3.client('iam')
    
    # Loop through the user list and pull keys. Check them, and add em to an array if over 90 days
    for userList in iamClient.list_users()['Users']:
        userKeys = iamClient.list_access_keys(UserName=userList['UserName'])
        for keyValue in userKeys['AccessKeyMetadata']:
            if keyValue['Status'] == 'Active':
                currentDate = date.today()
                activeDays = currentDate - keyValue['CreateDate'].date()
                
                if activeDays >= datetime.timedelta(days=75):
                    # Find the actual expiration date
                    expirationDate = keyValue['CreateDate'].date() + timedelta(days=89)
                    
                    # Set the email variables
                    USERNAME  = userList['UserName']
                    ACCESSKEY = keyValue['AccessKeyId']
                    CREATEDON = str(keyValue['CreateDate'].date())
                    EXPIRESON = str(expirationDate)
                    DAYSLEFT  = str(expirationDate - currentDate).split()[0]
    
                    # Sent the email
                    sendSesEmail(USERNAME, ACCESSKEY, CREATEDON, EXPIRESON, DAYSLEFT)