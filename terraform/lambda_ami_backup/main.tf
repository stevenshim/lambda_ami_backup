provider "template" {
    version             = "~> 2.1"
}

provider "aws"{
    version             = "~> 2.14"
    region              = local.aws.region
}

module "lambda_ami_backup" {
    source              =   "./modules"
    schedule_exp        =   var.schedule_exp
    tag_key             =   var.ec2_tag_key_env_var
    tag_value           =   var.ec2_tag_value_env_var
    kms_key_arn         =   data.aws_kms_alias.lambda.target_key_arn
}