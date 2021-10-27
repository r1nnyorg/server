import oci

configure = {'user':'ocid1.user.oc1..aaaaaaaalwudh6ys7562qtyfhxl4oji25zn6aapndqfuy2jfroyyielpu3pa', 'key_file':'oci.key', 'fingerprint':'bd:01:98:0d:5d:4a:6f:b2:49:b4:7f:df:43:00:32:39', 'tenancy':'ocid1.tenancy.oc1..aaaaaaaa4h5yoefhbxm4ybqy6gxl6y5cgxmdijira7ywuge3q4cbdaqnyawq', 'region':'us-sanjose-1'}
databaseClient = oci.database.DatabaseClient(configure)
databaseClientCompositeOperations = oci.database.DatabaseClientCompositeOperations(databaseClient)
createAutonomousDatabaseBase = oci.database.models.CreateAutonomousDatabaseBase(compartment_id=configure.get('tenancy'), db_name='dataWarehouse', admin_password='ora1cle+ORAC', cpu_core_count=1, data_storage_size_in_gbs=20)
databaseClientCompositeOperations.create_autonomous_database_and_wait_for_state(createAutonomousDatabaseBase, wait_for_states=[oci.database.models.AutonomousDatabase.LIFECYCLE_STATE_AVAILABLE])
