"""Regression tests for deployment initialization and BLAST routing."""
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings
from django.urls import resolve

from statistic.models import FiltrationStepsLncRnaIdentificationPipeline as Statistic
from blast_rest.views import blastn
from django.db import OperationalError


@override_settings(SECURE_SSL_REDIRECT=False)
class DeploymentTests(TestCase):
    def test_health_checks_database_with_https_redirect_enabled(self):
        with self.settings(SECURE_SSL_REDIRECT=True):
            response = self.client.get('/healthz/', HTTP_X_FORWARDED_PROTO='https')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'ok'})

    def test_health_returns_503_without_leaking_database_errors(self):
        with patch('brassicaLncWeb.health.connection.cursor',
                   side_effect=OperationalError('private connection details')):
            response = self.client.get('/healthz/')
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {'status': 'unavailable'})

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
