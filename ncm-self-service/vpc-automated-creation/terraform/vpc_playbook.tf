terraform {
  required_providers {
    nutanix = {
      source = "nutanix/nutanix"
      version = "1.8.0-beta.1"
    }
  }
}

provider "nutanix" {
  username     = var.pc_user
  password     = var.pc_password
  endpoint     = var.pc_address
  port         = var.pc_port
  insecure     = true
  wait_timeout = 10
}

data "nutanix_subnet" "external_network" {
  subnet_name = var.external_network
}

resource "nutanix_vpc" "vpc" {
  name = var.vpc_name

  external_subnet_reference_name = [
    var.external_network
  ]

  common_domain_name_server_ip_list{
          ip = "8.8.8.8"
  }
  common_domain_name_server_ip_list{
          ip = "8.8.8.9"
  }
}

#create the internal subnet
resource "nutanix_subnet" "internal_subnet" {
	name        = "${each.value.name}"
	description = "${each.value.description}"
	vpc_reference_uuid = resource.nutanix_vpc.vpc.id
	subnet_type = "${each.value.subnet_type}"
	subnet_ip          = "${each.value.subnet_ip}"
	default_gateway_ip = "${each.value.default_gateway_ip}"
	ip_config_pool_list_ranges = "${each.value.ip_config_pool_list_ranges}"
	prefix_length = "${each.value.prefix_length}"
  for_each = {for internal_subnet in var.internal_subnet: internal_subnet.name => internal_subnet}
}

#create one static route for vpc with external subnet
resource "nutanix_static_routes" "scn" {
  vpc_uuid = resource.nutanix_vpc.vpc.id

  static_routes_list{
    destination= "0.0.0.0/0"
    # required ext subnet uuid for next hop
    external_subnet_reference_uuid = data.nutanix_subnet.external_network.id
  }
}