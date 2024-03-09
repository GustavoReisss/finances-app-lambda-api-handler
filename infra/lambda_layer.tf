locals {
  requirements_path = "${local.source_code_path}/requirements.txt"
}


resource "null_resource" "pip_install" {
  triggers = {
    shell_hash = "${sha256(file(local.requirements_path))}"
  }

  provisioner "local-exec" {
    command = "python -m pip install -r ${local.requirements_path} --platform manylinux2014_x86_64 -t ${path.module}/layer/python --only-binary=:all:"
  }
}


data "archive_file" "layer" {
  type        = "zip"
  source_dir  = "${path.module}/layer"
  output_path = "${path.module}/layer.zip"
  depends_on  = [null_resource.pip_install]
}

resource "aws_lambda_layer_version" "dynamo_api_handler_layer" {
  layer_name          = "dynamo-api-handler-layer"
  filename            = data.archive_file.layer.output_path
  source_code_hash    = data.archive_file.layer.output_base64sha256
  compatible_runtimes = ["python3.11"]
}