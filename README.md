# Daily EC2 AMI Backup by lambda

This project using `Terraform` to help you deploy a AWS `Lambda` function with `IAM Role` and `Cloudwatch Event`.  

![simple darchitecture](./img/simple-architecture.png)


## Deployment guide
```bash
# Archive your python code.
$ ./build.py


$ cd terraform/lambda_ami_backup

$ terraform plan
$ terraform apply 
```