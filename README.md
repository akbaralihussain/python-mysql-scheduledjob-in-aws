# Python+MySql Scheduled Job using Terraform Modules

This repo explain a Quick, Simple and Easiest way to create a Python + MySQL Scheduled Job in AWS using terraform modules.

This repo contains 
1. Sample Python application which retrieves dummy data from {JSON} Placeholder 
2. Terraform code to create AWS resources and host above application as a Scheduled Job which runs in every 2 minutes.   
   
Following Terraform modules provided by TechieInYou are used to simplify this use case.

1. [**scheduled-job**](https://registry.terraform.io/modules/techieinyou/scheduled-job/aws/latest)
2. [**lambdalayer-python**](https://registry.terraform.io/modules/techieinyou/lambdalayer-python/aws/latest)

# Prerequisites
Below are the prequisites to host this Python code and run as a Scheduled Job
1. AWS Account and IAM User with access to create resources
2. IAM Role with below policies attached (recommended) 
   1. AWSLambdaVPCAccessExecutionRole
   2. CloudWatchEventsFullAccess
   3. CloudWatchLogsFullAccess
3. MySQL Database connection details
4. Subnet and Security Group Ids if this Scheduled Job needs to be created inside a VPC

# Database Connectivty
Creating Lambda in the same VPC where your MySQL database is created, will save time for the connection configuration and troubleshooting. Assign **my_vpc_subnets** and **my_vpc_security_groups** variables with those values.

NOTE: The python source code is taken from [AWS Documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-lambda-tutorial.html#vpc-rds-create-deployment-package) and customized.





