# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_student_student_group'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['title'], 'verbose_name': '\u0413\u0440\u0443\u043f\u0430', 'verbose_name_plural': '\u0413\u0440\u0443\u043f\u0438'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'ordering': ['last_name'], 'verbose_name': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442', 'verbose_name_plural': '\u0421\u0442\u0443\u0434\u0435\u043d\u0442\u0438'},
        ),
        migrations.RemoveField(
            model_name='student',
            name='student_group',
        ),
    ]
