## Quick test framework draft for testing some apt-get install functionality
***

### Usage

    1. Locally
        :: install modules

        $ pip3 install -r requirements.txt

        :: run tests

        $ pytest test_install.py -svl --html=out.html

        :: check html report at out.html

OR

    2. In Docker
        :: Create custom container "install-test"

        $ docker build . -t install-test

        :: Run tests inside custom container and get output

        $ docker run -it --rm --name install-test


OR

    3. Directly in Docker
        :: Create custom container "install-test"

        $ docker build . -t install-test

        :: Run container and leave it openned with bash

        $ docker run -it --rm --name install-test -v $PWD:/root/my_test install-test /bin/bash

        :: Inside container install modules and run tests

        $ cd /root/my_test && pip install -r requirements.txt && pytest test_install.py -svl --html=out.html
