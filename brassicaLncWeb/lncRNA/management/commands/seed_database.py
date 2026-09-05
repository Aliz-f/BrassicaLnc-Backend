from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.management import BaseCommand, CommandError, call_command
from django.db import transaction


FIXTURES = (
    'lnc', 'gtf', 'genetics_fpkm', 'chemical_fpkm', 'abiotic_fpkm',
    'biotic_fpkm', 'developmental_fpkm', 'premirna', 'smallrna', 'etms',
    'filteration', 'relationship', 'subdivision', 'target_downgene',
    'target_downgenes_description', 'target_upgene', 'target_upgenes_description',
)


class Command(BaseCommand):
    help = 'Load bundled reference data atomically into an empty database.'

    @transaction.atomic
    def handle(self, *args, **options):
        # Transposon has no bundled fixture and may legitimately remain empty.
        models = [model for label in ('lncRNA', 'statistic')
                  for model in apps.get_app_config(label).get_models()
                  if model._meta.label != 'lncRNA.Transposon']
        populated = [model.objects.exists() for model in models]
        if all(populated):
            self.stdout.write('Reference tables already populated; skipping seed.')
            return
        if any(populated):
            raise CommandError(
                'Reference database is partially populated. Restore a complete backup '
                'or inspect it before proceeding. Set SEED_DATABASE=false only for '
                'an intentionally managed dataset.'
            )
        directory = settings.BASE_DIR / 'data_initialization'
        fixtures = [str(directory / (name + '.json')) for name in FIXTURES]
        for fixture in fixtures:
            if not Path(fixture).is_file():
                raise CommandError('Missing fixture: ' + fixture)
        call_command('loaddata', *fixtures, verbosity=options['verbosity'])
        self.stdout.write(self.style.SUCCESS('Reference data loaded successfully.'))
