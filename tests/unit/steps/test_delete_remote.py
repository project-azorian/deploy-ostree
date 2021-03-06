# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import os.path
from unittest import mock, TestCase
from deploy_ostree.config import Config, Source
from deploy_ostree.steps.delete_remote import DeleteRemote


class TestDeleteRemote(TestCase):
    @mock.patch('deploy_ostree.steps.delete_remote.run')
    def test_should_delete_ostree_remote(self, mock_run: mock.Mock):
        cfg = Config(Source.url('url'), 'ref', remote='remote-name')

        DeleteRemote(cfg).run()

        mock_run.assert_called_once_with([
            'ostree', 'remote', 'delete',
            '--repo=%s' % os.path.join('/ostree', 'repo'),
            '--if-exists',
            'remote-name',
        ], check=True)

    def test_title_should_be_str(self):
        self.assertIsInstance(DeleteRemote(mock.Mock()).title, str)
