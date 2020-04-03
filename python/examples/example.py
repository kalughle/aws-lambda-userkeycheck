import boto3, os, time, datetime, sys, json
from datetime import date
from botocore.exceptions import ClientError

iam = boto3.client('iam')
email_list = []
def lambda_handler(event, context):
    print("All IAM user emails that have AccessKeys 90 days or older")
    for userlist in iam.list_users()['Users']:
        userKeys = iam.list_access_keys(UserName=userlist['UserName'])
        for keyValue in userKeys['AccessKeyMetadata']:
                if keyValue['Status'] == 'Active':
                    currentdate = date.today()
                    active_days = currentdate - \
                        keyValue['CreateDate'].date()
                    if active_days >= datetime.timedelta(days=90):
                        userTags = iam.list_user_tags(
                            UserName=keyValue['UserName'])
                        email_tag = list(filter(lambda tag: tag['Key'] == 'email', userTags['Tags']))
                        if(len(email_tag) == 1):
                            email = email_tag[0]['Value']
                            email_list.append(email)
                            print(email)

    email_unique = list(set(email_list))
    print(email_unique)
    RECIPIENTS = email_unique
    SENDER = "AWS SECURITY "
    AWS_REGION = os.environ['region']
    SUBJECT = "IAM Access Key Rotation"
    BODY_TEXT = ("Your IAM Access Key need to be rotated in AWS Account: 123456789 as it is 3 months or older.\r\n"
                "Log into AWS and go to your IAM user to fix: https://console.aws.amazon.com/iam/home?#security_credential"
                )
    BODY_HTML = """
    AWS Security: IAM Access Key Rotation: Your IAM Access Key need to be rotated in AWS Account: 123456789 as it is 3 months or older. Log into AWS and go to your https://console.aws.amazon.com/iam/home?#security_credential to create a new set of keys. Ensure to disable / remove your previous key pair.
                """            
    CHARSET = "UTF-8"
    client = boto3.client('ses',region_name=AWS_REGION)
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENTS,
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
            Source=SENDER,
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])