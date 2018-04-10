import logging
from itertools import islice
import re
import pytest
from util import run_cmd, run_cmd_with_interaction

log = logging.getLogger(__name__)

@pytest.fixture()
def full_clean():
    run_cmd("apt-get --yes --force-yes update")
    run_cmd("apt-get --yes --force-yes autoremove rolldice nsnake")
    run_cmd("apt-get --yes --force-yes purge")
    run_cmd("apt-get --yes --force-yes update")

class TestInstall:

    def setup_class(self):
        full_clean()

    def setup(self):
        return

    def teardown(self):
        out, rv, err = run_cmd("apt-get -y autoremove --purge rolldice nsnake")

    def test_get_help_for_installing(self):
        out1, return_code1, err1 = run_cmd("apt-get install -h")
        assert err1 == None and return_code1 == 0
        assert "apt-get [options] install|remove pkg1 [pkg2 ...]" in "\n".join(list(out1)), "Wrong helper message found"

    def test_instal_simple_package(self):
        out1, return_code1, err1 = run_cmd("apt-get -y install rolldice")
        assert err1 == None and return_code1 == 0
        out2 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "ok installed" in "\n".join(list(out2))

    def test_instal_simple_package_latest_version(self):
        out1, return_code1, err1 = run_cmd("apt-cache policy rolldice")
        assert err1 == None and return_code1 == 0
        latest_version = re.findall(re.compile("Candidate: (.+)\n"), "\n".join(list(out1)))[0]
        out2, return_code2, err2 = run_cmd("apt-get -y install rolldice")
        assert err2 == None and return_code2 == 0
        out2 = run_cmd("dpkg --status rolldice | grep ^Version")[0]
        assert str(latest_version) in "\n".join(list(out2)), "Expect that candidate version and installed version has been matched"

    def test_instal_simple_package_version(self):
        out1, return_code1, err1 = run_cmd("apt-get -y install rolldice=1.10-5")
        assert err1 == None and return_code1 == 0
        out2 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "ok installed" in list(out2)[0]
        out3 = run_cmd("dpkg --status rolldice | grep ^Version")[0]
        assert "1.10-5" in list(out3)[0]

    def test_instal_simple_package_with_another_package(self):
        out1, return_code1, err1 = run_cmd("apt-get -y install rolldice nsnake")
        assert err1 == None and return_code1 == 0
        out2 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "ok installed" in "\n".join(list(out2))
        out3 = run_cmd("dpkg --status nsnake | grep ^Status")[0]
        assert "ok installed" in "\n".join(list(out3))

    def test_removing_simple_package(self):
        out1, return_code1, err1 = run_cmd("apt-get -y install rolldice")
        out2, return_code2, err2= run_cmd("apt-get -y install rolldice-")
        assert err2 == None and return_code2 == 0
        out3 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "is not installed" in "\n".join(list(out3)), "Expected 'is not installed' status after success removing package"

    def test_cancel_removing_simple_package(self, full_clean):
        out1, return_code1, err1 = run_cmd("apt-get -y install rolldice")
        out2, err2 = run_cmd_with_interaction("apt-get install rolldice-", "N")
        assert err2 == None
        assert re.search(re.compile("The following packages will be REMOVED:(\s)*\n(\s)*rolldice"), out2.decode()) != None
        out3 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "ok installed" in "\n".join(list(out3)), "Expected 'is not installed' status after cancel removing package"

    def test_confirm_removing_simple_package(self, full_clean):
        out1, return_code1, err1 = run_cmd("apt-get -y install rolldice")
        out2, err2 = run_cmd_with_interaction("apt-get install rolldice-", "Y")
        assert err2 == None
        assert re.search(re.compile("The following packages will be REMOVED:(\s)*\n(\s)*rolldice"), out2.decode()) != None
        out3 = run_cmd("dpkg --status rolldice | grep ^Status")[0]
        assert "is not installed" in "\n".join(list(out3)), "Expected 'is not installed' status after confirm removing package"