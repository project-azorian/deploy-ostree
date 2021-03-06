# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import pytest
import os.path
from .. import deploy_ostree
from ..fixtures import FixtureTestCase, OSTreeFixture, OSTreeCommitFixture

TESTS_DIR = os.path.dirname(__file__)


@pytest.mark.needs_isolation
class TestKernelArgs(FixtureTestCase):
    FIXTURES = [OSTreeFixture(), OSTreeCommitFixture()]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deploy_ostree([os.path.join(TESTS_DIR, 'kernel-args.json')])

    def test_should_add_root_kernel_argument(self):
        options = self.find_line(self.bootloader_entry, 'options')
        self.assertIn('root=', options)

    def test_should_add_custom_kernel_args(self):
        options = self.find_line(self.bootloader_entry, 'options')
        self.assertIn('quiet', options)
        self.assertIn('splash', options)
        self.assertIn('arg=1', options)
        self.assertIn('arg=2', options)

    @property
    def bootloader_entry(self):
        entries_dir = '/boot/loader/entries'
        conf = os.listdir(entries_dir)[0]
        return os.path.join(entries_dir, conf)

    def find_line(self, path, prefix):
        with open(path, 'r') as f:
            for line in f:
                if line.startswith(prefix):
                    return line
        self.fail()
