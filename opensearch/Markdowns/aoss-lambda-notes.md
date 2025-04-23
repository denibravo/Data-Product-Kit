## Things to Note for AWS OpenSearch Serverless, Post GreSQL, and Lambda Connection 

### Lambda Function Specifics
- Create a new lambda function in AWS console:
    - Name the lambda function
    - Choose the runtime as Python 3.13
    - Choose the role as one that has access to the opensearch serverless policies
    - For additional configurations, choose the VPC that the opensearch serverless instance and the postgreSQL instance are in
        - Choose appropriate subnets and security groups that are associated with the VPC and database instances

- For any imports that are not included in the default lambda environment, you will need to include them in a lambda layer.
    - First create a new zip file with the necessary imports
    - To create a lambda layer, create a new lambda layer in the AWS console
    - In the lambda layer console enter:
        - the name of the layer
        - upload the zip file that you created
        - for compatible architectures, choose x86_64
        - for compatible runtimes, choose python3.13
        - then click create
    - attach the lambda layer to the lambda function
        - this can be found in the lambda function console under the layers section

### Opensearch Serverless Connection Specifics
- Create a new opensearch serverless instance in AWS console
- For the data access policy, you will need to include the same role that you used for the lambda function
    - This will allow the lambda function to access the opensearch instance

### Overall Connection to Opensearch Serverless, Post GreSQL, and Lambda
- Make sure that all the instances are in the same VPC
- Make sure that all the instances are in the same security group