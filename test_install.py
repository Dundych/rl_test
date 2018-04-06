import logging
from itertools import islice
import pytest
from util import run_cmd

log = logging.getLogger(__name__)


out, rv, err = run_cmd("dpkg --status rolldice | grep ^Status")

class TestInstall:

    def setup_class(self):
        out, rv, err = run_cmd("apt-get --yes --force-yes autoremove --purge rolldice nsnake && apt-get update")

    def setup(self):
        return

    def teardown(self):
        out, rv, err = run_cmd("apt-get -y autoremove --purge rolldice nsnake")


    def test_instal_simple_package(self):
        out, rv, err = run_cmd("apt-get -y install rolldice")
        assert err == None and rv == 0
        out2 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "ok installed" in list(out2)[0]

    def test_instal_simple_package_version(self):
        out, rv, err = run_cmd("apt-get -y install rolldice=1.10-5")
        assert err == None and rv == 0
        out2 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "ok installed" in list(out2)[0]
        out3 = run_cmd("dpkg --status rolldice | grep ^Version")[0]
        assert "1.10-5" in list(out3)[0]

    def test_instal_simple_package_with_another_package(self):
        out, rv, err = run_cmd("apt-get -y install rolldice nsnake")
        assert err == None and rv == 0
        out2 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "ok installed" in list(out2)[0]
        out3 = run_cmd("dpkg --status nsnake | grep ^Status")[0]
        assert "ok installed" in list(out3)[0]

    def test_remove_simple_package(self):
        out, rv, err = run_cmd("apt-get -y install rolldice")
        out2, rv2, err2 = run_cmd("apt-get -y install rolldice-")
        assert err2 == None and rv2 == 0
        out3 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "is not installed" in list(out3)[0]
