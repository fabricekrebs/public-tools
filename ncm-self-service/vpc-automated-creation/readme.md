# VPC creation and Calm Project creation.
This example will create a VPC and define a new Calm project, assigning the new ressource to it. It is required to have a bastion / jumphost deployed, in order to be able to execute Calm DSL script and Terraform as well.

## Jumphost / Bastion Creation
The jumphot should be deployed, with terraform installed
Install the calm DSL in the current directory
```
cd ~//calm-dsl
python3 -m venv venv
. venv/bin/activate
pip3 install wheel
make dev
```
Then initialize the Calm DSL
calm init dsl

#PC
Create a customer Role in PC (for example Customer-User), and ensure to have at least the following permissions set:
- App / Basic Access
- Blueprint / View Project

##Calm Preparation
A default project need to be created, with local cluster specify
A endpoint needs to be registered, pointing to the Jumphost.
Check the variable define on the Blueprint matches the current environment
Runbook named msp_blueprint.json need to be uploaded to Calm.
Ensure to have Nutanix Marketplace Apps enabled under Calm Settings / General

##VPC Preparation
MSP needs to be enabled on PC
Advanced Flow networking needs to be enable. If needed, for demo purpose, gflag can be set to allow it to be deployed on small PC size
```curl http://127.0.0.1:2060/h/gflags?atlas_msp_cmsp_allowed_pc_sizes=kSmall,kLarge,kXLarge```
A network, tagged as External Connectivity for VPCs, needs to be created.

#New marketplace item publication
To publish a new appliction on the marketplace, the Runbook runbook-publish-marketplace-item.json can be used.

#Cleanup
To cleanup execute the Runbook name runbook-vpc-deletion.json
