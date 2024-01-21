locals {
  db_conn_vars = {
    database_host : var.db_host,
    database_uid : var.db_userid,
    database_pwd : var.db_password
  }
}

module "lambdalayer-python-pymysql" {
  source       = "techieinyou/lambdalayer-python/aws"
  version      = "1.0.0"
  library_name = "pymysql"
}

module "lambdalayer-python-requests" {
  source       = "techieinyou/lambdalayer-python/aws"
  version      = "1.0.0"
  library_name = "requests"
}

module "scheduled-job" {
  source  = "techieinyou/scheduled-job/aws"
  version = "1.0.2"

  lambda_name        = "collect-todos"
  lambda_language    = "python"
  source_code_folder = "./source-code"
  lambda_handler     = "lambda_function.lambda_handler"

  lambda_execution_role = var.iam_role_arn
  lambda_layers         = [module.lambdalayer-python-pymysql.arn, module.lambdalayer-python-requests.arn]
  lambda_env_vars       = local.db_conn_vars
  vpc_subnets           = var.my_vpc_subnets
  vpc_security_groups   = var.my_vpc_security_groups
}

output "lambda_arn" {
  value = module.scheduled-job.lambda_arn
}
