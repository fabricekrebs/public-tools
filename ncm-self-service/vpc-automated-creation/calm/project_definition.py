import os
import json

#import calm required functions
from calm.dsl.builtins import Project
from calm.dsl.builtins import Provider, Ref
from calm.dsl.builtins import read_local_file
from calm.dsl.builtins import basic_cred
from calm.dsl.builtins import Environment
from calm.dsl.builtins import Substrate
from calm.dsl.builtins import readiness_probe
from calm.dsl.builtins import AhvVm
from calm.dsl.builtins import AhvVmResources
from calm.dsl.builtins import AhvVmDisk
from calm.dsl.builtins import AhvVmGC
from calm.dsl.builtins import AhvVmNic
from calm.dsl.builtins import NetworkGroupTunnel

from calm.dsl.builtins.models.network_group_tunnel_vm_spec import ahv_network_group_tunnel_vm_spec

#retrieve variable defin in varaibles file, under .local folder
var_json = json.loads(read_local_file("variables"))

LINUX_KEY = read_local_file(var_json["LINUX_KEY_PATH"])
LINUX_PUBLIC_KEY = read_local_file(var_json["LINUX_PUBLIC_KEY_PATH"])
ACCOUNT = var_json["ACCOUNT"]
INTERNAL_SUBNET = var_json["INTERNAL_SUBNET"]
EXTERNAL_NETWORK = var_json["EXTERNAL_NETWORK"]
CLUSTER = var_json["CLUSTER"]
USER = var_json["USER"]
GROUP = var_json["GROUP"]
VCPUS = var_json["VCPUS"]
STORAGE = var_json["STORAGE"]
MEMORY = var_json["MEMORY"]
CLOUD_INIT_PATH = var_json["CLOUD_INIT_PATH"]
VPC = var_json["VPC"]

linux = basic_cred("linux", LINUX_KEY, name="linux", type="KEY", default=True)

subnets = []
#loop through subnets, and create the list
for subnet_item in INTERNAL_SUBNET:
    subnets.append(Ref.Subnet(name=subnet_item, vpc=VPC))

#Define AHV Linux Machine resource
class MyAhvLinuxVmResources(AhvVmResources):

    memory = 4
    vCPUs = 2
    cores_per_vCPU = 1
    disks = [
        AhvVmDisk.Disk.Scsi.cloneFromImageService("ubuntu-22.04", bootable=True),
    ]
    
    #define the first subnet as default one.
    nics = [AhvVmNic(str(subnets[0]), vpc=VPC)]

    guest_customization = AhvVmGC.CloudInit(
        filename=os.path.join(".local", CLOUD_INIT_PATH)
    )

#define specific category to attach
class MyAhvLinuxVm(AhvVm):

    resources = MyAhvLinuxVmResources
    categories = {"AppFamily": "Backup", "AppType": "Default"}
    cluster = Ref.Cluster(CLUSTER)


#define the substrate
class AhvVmSubstrate(Substrate):

    provider_spec = MyAhvLinuxVm
    readiness_probe = readiness_probe(disabled=True)


#linking together both Environment and Project
class DefaultEnvironment(Environment):
    substrates = [AhvVmSubstrate]
    credentials = [linux]

    providers = [
        Provider.Ntnx(
            account=Ref.Account(ACCOUNT),
            subnets=subnets,
            vpcs=[Ref.Vpc(VPC)],
            clusters=[Ref.Cluster(CLUSTER)]
        )
    ]

#define the Project
class CustomerProject(Project):

    providers = [
        Provider.Ntnx(
            account=Ref.Account(ACCOUNT),
            subnets=subnets,
            vpcs=[Ref.Vpc(name=VPC, account_name=ACCOUNT)],
            clusters=[Ref.Cluster(name=CLUSTER, account_name=ACCOUNT)],
        )
    ]

    users = [
        Ref.User(name=USER),
    ]

    #groups = [Ref.Group(name=GROUP)]

    quotas = {"vcpus": VCPUS, "storage": STORAGE, "memory": MEMORY}

    #set the previously define environment to this project
    envs = [DefaultEnvironment]

class NewNetworkGroupTunnel2(NetworkGroupTunnel):
    """Network group tunnel for test"""
    account = Ref.Account(ACCOUNT)
    platform_vpcs = [Ref.Vpc(VPC, account_name=ACCOUNT)] # Resolve account name from parent.
    tunnel_vm_spec = ahv_network_group_tunnel_vm_spec(CLUSTER, INTERNAL_SUBNET[0])
