#!/bin/bash
docker run --rm -it --network=host -e FLASK_APP=groundstation/__init__.py -e FLASK_ENV=development -e APP_SETTINGS=groundstation.config.DevelopmentConfig -e SECRET_KEY="\xffY\x8dG\xfbu\x96S\x86\xdfu\x98\xe8S\x9f\x0e\xc6\xde\xb6$\xab:\x9d\x8b" ground_website:latest
