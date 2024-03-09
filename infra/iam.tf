resource "aws_iam_role" "lambda_api_handler_role" {
  name_prefix                = "lambda-api-handler-role"
  # assume_role_policy  = data.aws_iam_policy_document.instance_assume_role_policy.json # (not shown)
 
  managed_policy_arns = [
    aws_iam_policy.dynamo_policy.arn
  ]

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "sts:AssumeRole"
        Sid    = ""
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "dynamo_policy" {
  name_prefix        = "dynamo-policy"
  path        = "/"
  description = "Grant access to dynamo tables"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "dynamodb:BatchGetItem",
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:BatchWriteItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
    ]
  })
}