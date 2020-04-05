import json

def lambda_handler(event, context):
    import boto3, datetime
    from datetime import timedelta, date
    from botocore.exceptions import ClientError
    
    # ---------- CONFIG VARIABLES --------------------------------------------------
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_SES_REGION = "us-west-2"
    
    # Email sender information
    SENDER_ADDRESS = "Lambda Alert <lambdaalert@wolfbrigade.org>"
    
    # This should be the common IAM or Cloud alert address
    MAIN_RECIPIENT = "kalughle@gmail.com"

    # This should be the name of the AWS Tag that houses the IAM account owners email
    USERTAG_FOROWNEREMAIL = "OwnerEmail"

    # Xxx
    DAYSBEFOREWARN = 14

    # Xxx
    DAYSTOEXPIRE = 90
    
    # ---------- DERIVED VARIABLES -------------------------------------------------
    # Xxx
    daysToWarn = DAYSTOEXPIRE - DAYSBEFOREWARN

    # ---------- ALL FUNCTIONS -----------------------------------------------------
    # Send Simple Email Service Email Function
    def sendSesEmail(USERNAME, ACCESSKEY, CREATEDON, EXPIRESON, DAYSLEFT, OWNEREMAIL):
        # The character encoding for the email
        CHARSET = "UTF-8"
        
        # The subject line for the email
        SUBJECT = "AWS IAM Expiring User Alert!"
                    
        # The HTML body of the email
        BODY_HTML = """<html>
        <head></head>
        <body>
            <h1>The IAM AccessKey for the user {USERNAME} will expire in {DAYSLEFT} days</h1>
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
    
        # The email body for recipients with non-HTML email clients
        BODY_TEXT = (
            "The IAM AccessKey for the user {USERNAME} will expire in {DAYSLEFT} days\r"
            "\r"
            "UserName:  {USERNAME}\r"
            "AccessKey: {ACCESSKEY}\r"
            "CreatedOn: {CREATEDON}\r"
            "ExpiresOn: {EXPIRESON}\r"
            "DaysLeft:  {DAYSLEFT}"
        ).format(USERNAME=USERNAME, ACCESSKEY=ACCESSKEY, CREATEDON=CREATEDON, EXPIRESON=EXPIRESON, DAYSLEFT=DAYSLEFT)
                    
        # Create a new SES resource and specify the region of the SES service in use
        sesClient = boto3.client('ses',region_name=AWS_SES_REGION)

        # Provide the contents of the email, and send
        sesClient.send_email(
            Destination={
                'ToAddresses': [
                    MAIN_RECIPIENT,
                    OWNEREMAIL
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
    
    # ========== EXECUTION SECTION =================================================
    # Set the client. Should be "boto3.client('iam') for Lambda
    iamClient = boto3.client('iam')
    
    # Loop through the user list and their keys. Pull keys if active and...
    for userList in iamClient.list_users()['Users']:
        userKeys = iamClient.list_access_keys(UserName=userList['UserName'])
        for keyValue in userKeys['AccessKeyMetadata']:
            if keyValue['Status'] == 'Active':
                # Check them. If older than daysToWarn...
                currentDate = date.today()
                activeDays = currentDate - keyValue['CreateDate'].date()
                
                if activeDays >= datetime.timedelta(days=daysToWarn):
                    # Find the actual expiration date
                    expirationDate = keyValue['CreateDate'].date() + timedelta(days=DAYSTOEXPIRE)
                    
                    # Set the email variables to send
                    USERNAME  = userList['UserName']
                    ACCESSKEY = keyValue['AccessKeyId']
                    CREATEDON = str(keyValue['CreateDate'].date())
                    EXPIRESON = str(expirationDate)
                    DAYSLEFT  = str(expirationDate - currentDate).split()[0]

                    # Pull the user tags for this user
                    userTags = iamClient.list_user_tags(UserName=keyValue['UserName'])
                    
                    # Filter out the owner email address keypair we're looking for
                    ownerEmailObj = list(filter(lambda tag: tag['Key'] == USERTAG_FOROWNEREMAIL, userTags['Tags']))
                    if not ownerEmailObj:
                        print("empty")
                        OWNEREMAIL = ''
                    else:
                        OWNEREMAIL = ownerEmailObj[0]['Value']
    
                    # Send the email to the appropriate people
                    sendSesEmail(USERNAME, ACCESSKEY, CREATEDON, EXPIRESON, DAYSLEFT, OWNEREMAIL)