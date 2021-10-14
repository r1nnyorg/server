import os
from myproject import testrunner
user_ocid = os.environ["USER_OCID"]
key_file = key_for(user_ocid)

config = {
    "user": user_ocid,
    "key_file": key_file,
    "fingerprint": calc_fingerprint(key_file),
    "tenancy": testrunner.tenancy,
    "region": testrunner.region
}

from oci.config import validate_config
validate_config(config)
