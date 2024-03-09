resource "aws_lambda_function" "lambda" {
  function_name    = "lambda-api-handler"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.11"
  filename         = data.archive_file.code.output_path
  source_code_hash = data.archive_file.code.output_base64sha256
  role             = aws_iam_role.lambda_api_handler_role.arn
  layers           = [aws_lambda_layer_version.dynamo_api_handler_layer.arn]
  timeout          = 29
  
  environment {
    variables = {
      "ENV" = "dev"
    }
  }
}

data "archive_file" "code" {
  type        = "zip"
  source_dir  = "${local.source_code_path}"
  output_path = "${path.module}/code.zip"
}