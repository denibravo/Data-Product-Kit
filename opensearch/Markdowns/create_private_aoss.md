### How to create a working private instance of OpenSearch Serverless

**`Note`**: This guide is subject to change as knowledge of OpenSearch Serverless continues to grow as the project progresses.

#### Step 1: Create a VPC
- Go to the VPC console in the AWS Management Console
- Click on `"Create VPC"`
- For the VPC settings enter the following:
    - Select `VPC and more`
    - Name tag: `Enter the VPC name`
    - IPv4 CIDR block: `Leave as default`
    - IPv6 CIDR block: `Leave as default`
    - Tenancy: `Default`
    - Number of Availability Zones: `1`
    - Number of public subnets: `1`
    - Number of private subnets: `1`
    - NAT Gateway: `None`
    - VPC endpoint: `s3 Gateway`
    - DNS options: `Default`
- Click on `"Create VPC"`

#### Step 2: Create a Security Group
- Go to ec2 console in the AWS Management Console
- On the left hand side under Network & Security, click on `"Security Groups"`
- Click on `"Create Security Group"`
- For the Security Group settings enter the following:
    - Security group name: `Enter the security group name`
    - Description: `Enter the security group description`
    - VPC: `Select the VPC you created in Step 1`
    - Create two inbound rules: 
        - Rule 1:
            - Type: `SSH`
            - Protocol: `TCP`
            - Port Range: `22`
            - Source: `0.0.0.0/0`
            - Description: `Enter a description`
        - Rule 2:
            - Type: `HTTPS`
            - Protocol: `TCP`
            - Port Range: `443`
            - Source: `10.0.0.0/16`
            - Description: `Enter a description`
    - Outbound rules:
        - Type: `HTTPS`
        - Protocol: `TCP`
        - Port Range: `443`
        - Destination type: `anywhere-IPv4`
        -Destination: `0.0.0.0/0`
    - Click on `"Create Security Group"`

#### Step 3: Create a Key Pair
- Go to the EC2 console in the AWS Management Console
- On the left hand side under Network & Security, click on `"Key Pairs"`
- Click on `"Create Key Pair"`
- For the Key Pair settings enter the following:
    - Key pair name: `Enter the key pair name`
    - Type: `ED25519`
    - File format: `.pem`
    - Click on `"Create Key Pair"`
- Save the key pair in a secure location
    - Make sure that the key has the correct permission. It can only be accessible by the user. For example use `chmod 600 <key-name>.pem` to set proper permissions.

#### Step 4: Create a VPC Endpoint
- Go to Opensearch service in the AWS Management Console
- Click on `"VPC Endpoints"` under OpenSearch Serverless
- Click on `"Create VPC endpoint"`
- For the VPC endpoint settings enter the following:
    - Name: `Enter the VPC endpoint name`
    - VPC: `Select the VPC you created in Step 1`
    - Subnet: `Select the public subnet you created in Step 1`
    - Security group: `Select the security group you created in Step 2`
    - Click on `"Create VPC endpoint"`

#### Step 5: Create an OpenSearch Serverless Instance
- Go to the OpenSearch service in the AWS Management Console
- Click on Collections under OpenSearch Serverless
- Click on `"Create collection"`
- Settings:
  - Collection name: `Enter a name for your collection`
  - Type: `Search`
  - Uncheck `"Enable redundancy"`
  - Click `"Standard create"`
  - For Ecryption, leave it as `"Use AWS owned key"`(This will be changed in the future)
  - For "Access collections from", select `"Private network"`
    - For "VPC endpoint", `select the VPC endpoint you created in Step 4`
  - Enable access to `OpenSearch Endpoint`
- Then click `"Next"`

#### Step 6: Configure Data Access
**`Note`**: This section is where you give permissions to perform actions on the collection. This is dependent on the permissions you would like to give to the user. For this example, we will give full access to the user.

- Name your rule
- click `"Add principals"`
    - Select `"IAM users and roles"`
    - Click on the search bar and select `"Users"` in the dropdown
    - `Select your IAM user`
    - Click `"Save"`
- Under "Grant permissions", `select all that apply` (For now, select all)
- Click `"Next"`
- You can add this rule as a new policy or add to an existing policy.
- Click `"Next"`
- Finally, click `"Submit"`

#### Step 7: Spin up an EC2 instance
- Go to the EC2 console in the AWS Management Console
- Click on `"Launch Instance"`
- Enter these configurations:
    - AMI: `Amazon Linux 2023 AMI`
    - Instance type: `t2.micro`
    - Key pair: `Select the key pair you created in Step 3`
    - Configure Instance Details:
        - Network: `Select the VPC you created in Step 1`
        - Subnet: `Select the public subnet you created in Step 1`
        - Auto-assign Public IP: `Enable`
        - Firewall: `Select the security group you created in Step 2`
    - Add Storage: `Leave as default`
    - Add Tags: `Leave as default`
  
    - Review then click `"Launch Instance"`
- After the instance is launched, click on the `instance ID`
- Copy the public IP address of the instance
- Open a terminal and SSH into the instance using the public IP address 
    ```
    ssh -i <path to key pair> ec2-user@<public IP address>
    ```
- Once you are in the instance, install Git
    ```
    sudo yum install git
    ```
- Configure your AWS credentials
    ```
    aws configure
    ```

- Clone the repository
    ```
    git clone <repository link>
    ```
- Change directory to the repository
    ```
    cd <repository name>
    ```

#### Step 8: Begin the setup process in the Cloud Deployment section of the README.md file




