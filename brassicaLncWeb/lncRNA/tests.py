"""Regression tests for deployment initialization and BLAST routing."""
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command, CommandError
from django.test import TestCase
from django.urls import resolve

from statistic.models import FiltrationStepsLncRnaIdentificationPipeline as Statistic
from blast_rest.views import blastn


class DeploymentTests(TestCase):
    def test_blast_api_routes_use_local_view(self):
        for path in ('/blast/blastn', '/blast/blastn/'):
            self.assertIs(resolve(path).func.view_class, blastn)

    def test_partial_reference_database_is_not_overwritten(self):
        row = Statistic.objects.create(name='existing', data={})
        with self.assertRaisesMessage(CommandError, 'partially populated'):
            call_command('seed_database', stdout=StringIO())
        self.assertTrue(Statistic.objects.filter(pk=row.pk).exists())

    def test_failed_seed_rolls_back_inserted_records(self):
        def failing_import(*args, **kwargs):
            Statistic.objects.create(name='incomplete', data={})
            raise CommandError('fixture failed')

        with patch('lncRNA.management.commands.seed_database.call_command',
                   side_effect=failing_import):
            with self.assertRaisesMessage(CommandError, 'fixture failed'):
                call_command('seed_database', stdout=StringIO())
        self.assertFalse(Statistic.objects.exists())
