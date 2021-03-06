# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.pull_ref import PullRef


class TestPullRef(TestCase):
    @mock.patch('deploy_ostree.steps.pull_ref.run')
    def test_should_pull_ref(self, run_mock: mock.Mock):
        cfg = Config(Source.url('url'), 'fedora/28/x86_64/workstation', remote='ostree-remote')

        PullRef(cfg).run()

        run_mock.assert_called_once_with([
            'ostree', 'pull',
            '--repo=%s' % os.path.join('/ostree', 'repo'),
            'ostree-remote', 'fedora/28/x86_64/workstation'
        ], check=True)

    def test_title_should_be_str(self):
        self.assertIsInstance(PullRef(mock.Mock()).title, str)
