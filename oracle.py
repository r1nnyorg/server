import oci
configure = {'user':'ocid1.user.oc1..aaaaaaaalwudh6ys7562qtyfhxl4oji25zn6aapndqfuy2jfroyyielpu3pa', 'key_file':'oci.key', 'fingerprint':'bd:01:98:0d:5d:4a:6f:b2:49:b4:7f:df:43:00:32:39', 'tenancy':'ocid1.tenancy.oc1..aaaaaaaa4h5yoefhbxm4ybqy6gxl6y5cgxmdijira7ywuge3q4cbdaqnyawq', 'region':'us-sanjose-1'}
oci.config.validate_config(configure)
virtualNetworkClient = oci.core.VirtualNetworkClient(configure)
virtualNetworkClientCompositeOperations = oci.core.VirtualNetworkClientCompositeOperations(virtualNetworkClient)
createVcnDetails = oci.core.models.CreateVcnDetails(compartment_id='chaowenguo1')
vnc = virtualNetworkClientCompositeOperations.create_vcn_and_wait_for_state(createVcnDetails, wait_for_states=[oci.core.models.Vcn.LIFECYCLE_STATE_AVAILABLE]).data
print('Created VCN: {}'.format(vcn.id))
print('{}'.format(vcn))
