# @Author: Fabrice Krebs
# @Last Modified by:   Fabrice Krebs
# @Last Modified time: 10-03-2022 09:50:49

variable "nutanix_cluster_name" {
  type = string
}
variable "pc_address" {
  type = string
}
variable "pc_port" {
  type      = string
}
variable "pc_password" {
  type      = string
  sensitive = true
}
variable "pc_user" {
  type = string
}
variable "vpc_name" {
  type = string
}
variable "external_network" {
  type = string
}
variable "internal_subnet"{
  type = list
}