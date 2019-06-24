variable "tag_key" {}
variable "tag_value" {}
variable "kms_key_arn" {}
variable "max_images" {}

resource "aws_lambda_function" "ami_backup_lambda" {
  function_name = "lambda_ec2_ami_backup"
  filename      = "${path.module}/code.zip"
  role          = aws_iam_role.iam_for_lambda.arn
  handler       = "handler.lambda_handler"
  kms_key_arn   = var.kms_key_arn
  timeout       = 10

  source_code_hash = filebase64sha256("${path.module}/code.zip")

  runtime = "python3.7"

  environment {
    variables = {
      "TAG_KEY" = var.tag_key
      "TAG_VALUE" = var.tag_value
      "MAX_RESERVED_COUNT" = var.max_images
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
