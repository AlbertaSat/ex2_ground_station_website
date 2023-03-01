import os
import sys
import signal
import json
from datetime import datetime, timezone
from groundstation.backend_api.ftp import FTPUploadAPI

FTP_UPLOAD = FTPUploadAPI()

# TODO: TIDY THIS UP
if __name__ == '__main__':
    sys.path.append(os.path.join(
        sys.path[0], 'ex2_ground_station_software', 'src'
    ))
    from groundStation import GroundStation
    from options import optionsFactory
    import ftp
    opts = optionsFactory("ftp").getOptions()
    print(opts.file_id)
    ftpRunner = ftp.ftpFactory(opts)
    signal.signal(signal.SIGINT, ftpRunner.shutdown)
    try:
        ftpRunner.run()
    except Exception as e:
        print(e)
    print("Hi")
    patch_data = {
        'uploaded': True,
        'upload_date': datetime.utcnow().isoformat()
    }
    print(FTP_UPLOAD.patch(opts.file_id, local_data=json.dumps(patch_data)))
    ftpRunner.shutdown(None, None)
