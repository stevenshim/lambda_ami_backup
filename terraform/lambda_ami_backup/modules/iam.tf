resource "aws_iam_role" "iam_for_lambda" {
  name = "lambda_daily_backup_role"
  assume_role_policy = file("${path.module}/iam_policy_file_lambda_assume_role.json")
}

resource "aws_iam_role_policy_attachment" "ami_backup_lambda_ec2_readonly" {
  policy_arn          =   "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
  role                =   aws_iam_role.iam_for_lambda.name
}

resource "aws_iam_role_policy_attachment" "ami_backup_lambda_basic_exec" {
  policy_arn          =   "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role                =   aws_iam_role.iam_for_lambda.name
}

resource "aws_iam_role_policy" "ami_backup_lambda_ami_backup" {
  name                =   "ami_backup_policy"
  role                =   aws_iam_role.iam_for_lambda.name
  policy              =   file("${path.module}/iam_policy_lambda_create_delete_ami.json")
}

resource "aws_iam_role_policy" "kms_key_value_read" {
  name                =   "kms_key_value_read"
  policy              =   file("${path.module}/iam_policy_lambda_kms.json")
  role                =   aws_iam_role.iam_for_lambda.id
}
