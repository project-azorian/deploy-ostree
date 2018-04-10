# Copyright 2018 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

from unittest import TestCase
from util import deploy_ostree


class TestHelp(TestCase):
    def test_should_print_error_and_exit_if_called_with_no_arguments(self):
        result = deploy_ostree([])

        self.assertIn(b'the following arguments are required', result.stderr)
        self.assertEqual(2, result.returncode)

    def test_should_print_help_and_exit_if_called_with_help_flag(self):
        result = deploy_ostree(['--help'])

        self.assertIn(b'deploy-ostree', result.stdout)
        self.assertIn(b'deploy and configure an OSTree commit', result.stdout)
        self.assertEqual(0, result.returncode)

    def test_should_print_help_and_exit_if_called_with_h_flag(self):
        result = deploy_ostree(['-h'])

        self.assertIn(b'deploy-ostree', result.stdout)
        self.assertIn(b'deploy and configure an OSTree commit', result.stdout)
        self.assertEqual(0, result.returncode)
