# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_exam'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam_result',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('grade', models.IntegerField(max_length=3, null=True, verbose_name='\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442', blank=True)),
                ('exam', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='students.Exam', verbose_name='\u0406\u0441\u043f\u0438\u0442')),
                ('student', models.ForeignKey(verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Student')),
            ],
            options={
                'verbose_name': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438 \u0456\u0441\u043f\u0438\u0442\u0443',
                'verbose_name_plural': '\u0420\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442\u0438 \u0456\u0441\u043f\u0438\u0442\u0443',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='exam',
            options={'ordering': ['date'], 'verbose_name': '\u0406\u0441\u043f\u0438\u0442', 'verbose_name_plural': '\u0406\u0441\u043f\u0438\u0442\u0438'},
        ),
        migrations.AlterField(
            model_name='exam',
            name='place',
            field=models.CharField(max_length=256, verbose_name='\u0410\u0443\u0434\u0438\u0442\u043e\u0440\u0456\u044f', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='student',
            name='student_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, verbose_name='\u0421\u0442\u0443\u0434\u0435\u043d\u0442', to='students.Group', null=True),
            preserve_default=True,
        ),
    ]
