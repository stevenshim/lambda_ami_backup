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

## Configuration
Modify terraform/lambda_ami_backup/variables.tf 

```text
variable "ec2_tag_key_env_var" {
    description = "The EC2's tag key that lambda looking up."
    default = "Backup"
}

variable "ec2_tag_value_env_var" {
    description = "The EC2's tag value that lambda looking up."
    default = "by_lambda"
}

variable "schedule_exp" {
    description = "The cloudwatch event schedule expression."
    default = "cron(0 18 * * ? *)"
}
```