import boto3, datetime
from datetime import timedelta, date
from botocore.exceptions import ClientError

# ---------- GLOBAL VARIABLES ----------------------------------------------------------------------
# The name of the profile to execute under (DELETE FOR LAMBDA!!)
PROFILE_NAME = 'test01-build'

# If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
AWS_SES_REGION = "us-west-2"

# Email sender information
SENDER_ADDRESS = "Lambda Alert <lambdaalert2@wolfbrigade.org>"

# This should be the common IAM or Cloud alert address
MAIN_RECIPIENT = "kalughle@gmail.com"

# This should be the common IAM or Cloud alert address
USERTAG_FOROWNEREMAIL = "OwnerEmail"

# ==================================================================================================
# Define the email function
def sendSesEmail(USERNAME, ACCESSKEY, CREATEDON, EXPIRESON, DAYSLEFT, OWNEREMAIL):
    # Create the session using the designated profile (DELETE FOR LAMBDA!!)
    session = boto3.session.Session(profile_name=PROFILE_NAME)
    sesClient = session.client('ses',region_name=AWS_SES_REGION)
    
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
        <br>UserName:  {USERNAME}
        <br>AccessKey: {ACCESSKEY}
        <br>CreatedOn: {CREATEDON}
        <br>ExpiresOn: {EXPIRESON}
        <br>DaysLeft:  {DAYSLEFT}
        </p>
    </body>
    </html>
                """.format(USERNAME=USERNAME, ACCESSKEY=ACCESSKEY, CREATEDON=CREATEDON, EXPIRESON=EXPIRESON, DAYSLEFT=DAYSLEFT)

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Try to send the email.
    try:
        # Create a new SES resource and specify a region (UNCOMMENT FOR LAMBDA!!)
        #sesClient = boto3.client('ses',region_name=AWS_SES_REGION)
        
        if not OWNEREMAIL:
            finalToEmail = MAIN_RECIPIENT
        else:
            finalToEmail = MAIN_RECIPIENT + ', ' + OWNEREMAIL

        #Provide the contents of the email.
        response = sesClient.send_email(
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
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message']),

# ==================================================================================================
# Execution
# # Create the session using the designated profile (DELETE FOR LAMBDA!!)
session = boto3.session.Session(profile_name=PROFILE_NAME)
iamClient = session.client('iam')

# Set the client. Should be "boto3.client('iam') for Lambda (UNCOMMENT FOR LAMBDA!!)
#iamClient = boto3.client('iam')
   
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

                # Pull the designated email tag
                userTags = iamClient.list_user_tags(UserName=keyValue['UserName'])
                step2 = list(filter(lambda tag: tag['Key'] == USERTAG_FOROWNEREMAIL, userTags['Tags']))
                if not step2:
                    print("empty")
                    OWNEREMAIL = ''
                else:
                    OWNEREMAIL = step2[0]['Value']

                # Send the email
                sendSesEmail(USERNAME, ACCESSKEY, CREATEDON, EXPIRESON, DAYSLEFT, OWNEREMAIL)