locals {
  module_dir      = "../../modules"
  aws = {
    region        = "ap-northeast-2"
    assume_role   = "arn:aws:iam::072548720675:role/terra-admin"
  }
}