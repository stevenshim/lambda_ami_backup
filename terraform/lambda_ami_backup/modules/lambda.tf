variable "tag_key" {}
variable "tag_value" {}

resource "aws_lambda_function" "ami_backup_lambda" {
  function_name = "lambda_ec2_ami_backup"
  filename      = "${path.module}/code.zip"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "code.lambda_handler"
  kms_key_arn   = "arn:aws:kms:ap-northeast-2:072548720675:key/904f40e2-d04e-499e-99c0-59c9a5734033"

  source_code_hash = filebase64sha256("${path.module}/code.zip")

  runtime = "python3.7"

  environment {
    variables = {
      "${var.tag_key}" = var.tag_value
    }
  }
}

resource "aws_lambda_permission" "ami_backup_lambda_permission" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.ami_backup_lambda.id
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.daily_utc_6pm.arn
}
