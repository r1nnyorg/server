import oci, asyncssh
configure = {'user':'ocid1.user.oc1..aaaaaaaalwudh6ys7562qtyfhxl4oji25zn6aapndqfuy2jfroyyielpu3pa', 'key_file':'oci.key', 'fingerprint':'bd:01:98:0d:5d:4a:6f:b2:49:b4:7f:df:43:00:32:39', 'tenancy':'ocid1.tenancy.oc1..aaaaaaaa4h5yoefhbxm4ybqy6gxl6y5cgxmdijira7ywuge3q4cbdaqnyawq', 'region':'us-sanjose-1'}
oci.config.validate_config(configure)
virtualNetworkClient = oci.core.VirtualNetworkClient(configure)
virtualNetworkClientCompositeOperations = oci.core.VirtualNetworkClientCompositeOperations(virtualNetworkClient)
createVcnDetails = oci.core.models.CreateVcnDetails(compartment_id='ocid1.tenancy.oc1..aaaaaaaa4h5yoefhbxm4ybqy6gxl6y5cgxmdijira7ywuge3q4cbdaqnyawq',cidr_block='10.0.0.0/16')
vcn = virtualNetworkClientCompositeOperations.create_vcn_and_wait_for_state(createVcnDetails, wait_for_states=[oci.core.models.Vcn.LIFECYCLE_STATE_AVAILABLE]).data
createSubnetDetails = oci.core.models.CreateSubnetDetails(compartment_id=vcn.compartment_id,vcn_id=vcn.id,cidr_block=vcn.cidr_block)
subnet = virtualNetworkClientCompositeOperations.create_subnet_and_wait_for_state(createSubnetDetails,wait_for_states=[oci.core.models.Subnet.LIFECYCLE_STATE_AVAILABLE]).data
computeClientCompositeOperations = oci.core.ComputeClientCompositeOperations(oci.core.ComputeClient(configure))
key = asyncssh.generate_private_key('ssh-rsa')
key.write_private_key('oracle')
#launchInstanceDetails = oci.core.models.LaunchInstanceDetails(compartment_id=vcn.compartment_id, shape='VM.Standard.E2.1.Micro', metadata={'ssh_authorized_keys':key.export_public_key().decode()},
#        source_details=instance_source_via_image_details, create_vnic_details=oci.core.models.CreateVnicDetails(subnet_id=subnet.id))
#instance = computeClientCompositeOperations.launch_instance_and_wait_for_state(launchInstanceDetails, wait_for_states=[oci.core.models.Instance.LIFECYCLE_STATE_RUNNING]).data
#print('Launched Instance: {}'.format(instance.id))
#print('{}'.format(instance))
print(oci.core.ComputeClient(configure).list_images(compartment_id=vcn.compartment_id, operating_system='Canonical Ubuntu').data[0].get('id'))
