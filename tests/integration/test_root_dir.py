# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
import tempfile
from .. import deploy_ostree, ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


class TestRootDir(FixtureTestCase):
    ROOT_DIR = tempfile.mktemp('ostree-root')
    REPO_DIR = os.path.join(ROOT_DIR, 'ostree', 'repo')
    STATEROOT_DIR = os.path.join(ROOT_DIR, 'ostree', 'deploy', 'test-stateroot')
    BOOTENTRIES_DIR = os.path.join(ROOT_DIR, 'boot', 'loader', 'entries')
    FIXTURES = [OSTreeFixture(root_dir=ROOT_DIR), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        result = deploy_ostree([
            '--root=%s' % cls.ROOT_DIR,
            os.path.join(TESTS_DIR, 'provisioner.json')
        ])
        print(result.stdout_str)

    def test_should_not_modify_system_ostree_root(self):
        self.assertEqual(len(os.listdir('/ostree')), 0)

    def test_should_not_add_system_ostree_remotes(self):
        self.assertEqual(len(os.listdir('/etc/ostree/remotes.d')), 0)

    def test_should_add_randomly_named_remote(self):
        remote = ostree(['remote', 'list', '--repo=%s' % self.REPO_DIR]).stdout_str.strip()
        url = ostree(['remote', 'show-url', remote, '--repo=%s' % self.REPO_DIR]).stdout_str.strip()
        self.assertEqual(url, 'http://localhost:8000/')

    def test_should_create_stateroot(self):
        self.assertTrue(os.path.isdir(os.path.join(self.STATEROOT_DIR, 'var')))

    def test_should_deploy_commit(self):
        self.assertTrue(os.path.isdir(self.deployment()))
        self.assertTrue(os.path.isfile(self.deployment('etc', 'os-release')))

    def test_should_create_bootloader_entry(self):
        entries = os.listdir(self.BOOTENTRIES_DIR)
        self.assertEqual(1, len(entries))
        self.assertIn('test-stateroot', entries[0])

    def test_should_set_correct_path_in_bootloader_entry(self):
        entry_name = os.listdir(self.BOOTENTRIES_DIR)[0]
        entry_file = os.path.join(self.BOOTENTRIES_DIR, entry_name)
        self.assert_file_contains(entry_file, 'linux /ostree/test-stateroot-')

    def test_should_run_provisioner_and_create_file_in_deployment(self):
        path = self.deployment('etc', 'network', 'interfaces.d', 'enp0s3')
        self.assertTrue(os.path.isfile(path))
        self.assert_file_contains(path, 'iface enp0s3 inet dhcp')

    def deployment(self, *args):
        deployments_dir = os.path.join(self.STATEROOT_DIR, 'deploy')
        elems = [elem for elem in os.listdir(deployments_dir) if not elem.endswith('.origin')]
        self.assertEqual(1, len(elems))
        return os.path.join(deployments_dir, elems[0], *args)

    def assert_file_contains(self, path, expected_content):
        with open(path, 'r') as f:
            content = f.read()
        self.assertIn(expected_content, content)
