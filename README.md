# aws-lambda-userkeycheck

This repo is a full cloudformation deployment of a lambda script to monitor your IAM users secret keys and notify you if they are nearing their date.

## Install/Configure

1. Register an SES Domain and make sure the SES Doamin is not in test mode
    * Record the SES Doamin **ARN** *(sesDomainArn)*, you will need it later
1. Create an S3 bucket to house your python code
    * Record the bucket **Name** *(s3BucketName)*, you will need it later
1. Edit the file python/lambda/lambda_function.py
    1. Set the following variables:
        * AWS_SES_REGION
            * This must be the region as you created your SES topic in
        * SENDER_ADDRESS
            * Use an email address within the SES Domains domain
        * MAIN_RECIPIENT
            * This should be the address of the governing team, **not** the account owner
        * USERTAG_FOROWNEREMAIL
            * This identifies the Tag that houses the email address of the owner of the account
    1. Save the file
1. Zip the file and upload to S3
    * Record the **Path and File Name** as the key *(s3FileKey)*
        * Ex. dir/sub-dir/filename.txt


## Usage

XXX

#### Assumptions

XXX

#### General Usage

XXX

## License

This code is released under the MIT License. See [LICENSE.txt](/LICENSE.txt).

## TODO

XXX