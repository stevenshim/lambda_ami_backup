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

variable "kms_key_arn" {
    description = "The managed KMS key for lambda function. You can copy it from KMS Console > AWS Managed keys > aws/lambda."
}