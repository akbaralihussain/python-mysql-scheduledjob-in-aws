variable "aws_region" {
  type = string
}

variable "aws_access_key" {
  type = string
}

variable "aws_secret_key" {
  type = string
}

variable "db_host" {
  type = string
}

variable "db_userid" {
  type = string
}

variable "db_password" {
  type = string
}

variable "my_vpc_subnets" {
  type = list(string)
}

variable "my_vpc_security_groups" {
  type = list(string)
}

variable "iam_role_arn" {
  type = string
}
