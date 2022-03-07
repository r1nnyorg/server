import oci, asyncssh, aiohttp, asyncio

configure = {'user':'ocid1.user.oc1..aaaaaaaalwudh6ys7562qtyfhxl4oji25zn6aapndqfuy2jfroyyielpu3pa', 'key_file':'oci.key', 'fingerprint':'bd:01:98:0d:5d:4a:6f:b2:49:b4:7f:df:43:00:32:39', 'tenancy':'ocid1.tenancy.oc1..aaaaaaaa4h5yoefhbxm4ybqy6gxl6y5cgxmdijira7ywuge3q4cbdaqnyawq', 'region':'us-sanjose-1'}
computeClient = oci.core.ComputeClient(configure)
computeClientCompositeOperations = oci.core.ComputeClientCompositeOperations(computeClient)
virtualNetworkClient = oci.core.VirtualNetworkClient(configure)
vcn = virtualNetworkClient.list_vcns(compartment_id=configure.get('tenancy')).data[0]
subnet = virtualNetworkClient.list_subnets(compartment_id=configure.get('tenancy')).data[0]

async def arm():
    launchInstanceDetails = oci.core.models.LaunchInstanceDetails(availability_domain=oci.identity.IdentityClient(configure).list_availability_domains(compartment_id=vcn.compartment_id).data[0].name, compartment_id=vcn.compartment_id, shape='VM.Standard.A1.Flex', metadata={'ssh_authorized_keys':'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC6HMfczm0N5/R7LRlC0Z8903DNxwlozMWVs7xxS6curdX8xKW/vG7BzboS/nBVCajUR1CwJSKKHIIKBwn+UGvV1Mp/fVCMxZT4IaIqUqxg6Guk85PLhBQMFp/e+EYFyVIL8rPRMgwGwa3nB0ed5y3xDo6gADnwhx4R2A3gFBsMGE9l9PfrzEWTTmwK+wNoLoOp+wkiTYkIPAukvLUJuOB5YmZiPN0ctx2fylyFOunUqL/mDCALS+mkUMtPEfd0RFDjShcQNY8WcN8X/9NS9qYhcjD6f195VmsGqFHS+LqAAuiIeTKgNQB2YcDFDBASrcrVgpLHw8wLKQVemvAk0ruh'}, image_id=computeClient.list_images(compartment_id=vcn.compartment_id, operating_system='Canonical Ubuntu', operating_system_version='20.04').data[0].id, subnet_id=subnet.id, shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(ocpus=4))
    instance = computeClientCompositeOperations.launch_instance_and_wait_for_state(launchInstanceDetails, wait_for_states=[oci.core.models.Instance.LIFECYCLE_STATE_RUNNING]).data
    ip = oci.core.VirtualNetworkClient(configure).get_vnic(computeClient.list_vnic_attachments(compartment_id=vcn.compartment_id, instance_id=instance.id).data[0].vnic_id).data.public_ip
    await asyncio.sleep(45)
    async with asyncssh.connect(ip, username='ubuntu', client_keys=['key'], known_hosts=None) as ssh: await ssh.run('''sudo apt purge -y snapd
sudo apt update
sudo add-apt-repository ppa:saiarcot895/chromium-beta
sudo apt install -y --no-install-recommends docker.io chromium-browser libx11-xcb1 x2goserver-xsession
encrypt=/etc/letsencrypt/live/chaowenguo.eu.org
sudo mkdir -p $encrypt
sudo chmod 757 $encrypt''')
    return ip

print(asyncio.run(arm()))
