import boto3, datetime

# ---------- GLOBAL VARIABLES ----------------------------------------------------------------------
# The name of the profile to execute under (DELETE FOR LAMBDA!!)
PROFILE_NAME = 'sso-sandbox_m1'

# ==================================================================================================
# Execution
# # Create the session using the designated profile (DELETE FOR LAMBDA!!)
ident = boto3.session.Session(profile_name=PROFILE_NAME).client('sts').get_caller_identity().get('Account')

name = boto3.session.Session(profile_name=PROFILE_NAME).client('organizations').describe_account(AccountId=ident).get('Account').get('Name')

print(ident)
print(name)