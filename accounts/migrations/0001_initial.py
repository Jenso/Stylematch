# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Service'
        db.create_table('accounts_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('length', self.gf('django.db.models.fields.IntegerField')(max_length=3)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('price', self.gf('django.db.models.fields.IntegerField')(max_length=6)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('display_on_profile', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('accounts', ['Service'])

        # Adding model 'OpenHours'
        db.create_table('accounts_openhours', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('mon', self.gf('django.db.models.fields.IntegerField')(default=480)),
            ('mon_closed', self.gf('django.db.models.fields.IntegerField')(default=1020)),
            ('tues', self.gf('django.db.models.fields.IntegerField')(default=480)),
            ('tues_closed', self.gf('django.db.models.fields.IntegerField')(default=1020)),
            ('wed', self.gf('django.db.models.fields.IntegerField')(default=480)),
            ('wed_closed', self.gf('django.db.models.fields.IntegerField')(default=1020)),
            ('thurs', self.gf('django.db.models.fields.IntegerField')(default=480)),
            ('thurs_closed', self.gf('django.db.models.fields.IntegerField')(default=1020)),
            ('fri', self.gf('django.db.models.fields.IntegerField')(default=480)),
            ('fri_closed', self.gf('django.db.models.fields.IntegerField')(default=1020)),
            ('sat', self.gf('django.db.models.fields.IntegerField')(default=480)),
            ('sat_closed', self.gf('django.db.models.fields.IntegerField')(default=1020)),
            ('sun', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('sun_closed', self.gf('django.db.models.fields.IntegerField')(default=-1)),
            ('reviewed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('accounts', ['OpenHours'])

        # Adding model 'Speciality'
        db.create_table('accounts_speciality', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('accounts', ['Speciality'])

        # Adding model 'ProfileImage'
        db.create_table('accounts_profileimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=250, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('cropped', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('accounts', ['ProfileImage'])

        # Adding model 'GalleryImage'
        db.create_table('accounts_galleryimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.ImageField')(max_length=250, blank=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('upload_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('display_on_profile', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('accounts', ['GalleryImage'])

        # Adding model 'UserProfile'
        db.create_table('accounts_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('profile_text', self.gf('django.db.models.fields.CharField')(max_length=500, blank=True)),
            ('profile_url', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
            ('temporary_profile_url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('number_on_profile', self.gf('django.db.models.fields.BooleanField')(default=False, max_length=1)),
            ('personal_phone_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('salon_phone_number', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('salon_name', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('salon_city', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('salon_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('salon_adress', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('zip_adress', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=18, decimal_places=10, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=18, decimal_places=10, blank=True)),
            ('url_online_booking', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('show_booking_url', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('profile_image_cropped', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profile_image_cropped', unique=True, null=True, to=orm['accounts.ProfileImage'])),
            ('profile_image_uncropped', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='profile_image_uncropped', unique=True, null=True, to=orm['accounts.ProfileImage'])),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('visible_message_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('approved_message_read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('picture_upload_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('accounts', ['UserProfile'])

        # Adding M2M table for field specialities on 'UserProfile'
        db.create_table('accounts_userprofile_specialities', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm['accounts.userprofile'], null=False)),
            ('speciality', models.ForeignKey(orm['accounts.speciality'], null=False))
        ))
        db.create_unique('accounts_userprofile_specialities', ['userprofile_id', 'speciality_id'])

        # Adding model 'InviteCode'
        db.create_table('accounts_invitecode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('used', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('invite_code', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('inviter', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='invitecode_inviter', null=True, to=orm['auth.User'])),
            ('reciever', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='invitecode_reciever', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('accounts', ['InviteCode'])

        # Adding model 'Featured'
        db.create_table('accounts_featured', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accounts.UserProfile'])),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal('accounts', ['Featured'])

        # Adding unique constraint on 'Featured', fields ['user', 'city']
        db.create_unique('accounts_featured', ['user_id', 'city'])

        # Adding model 'ScheduledCheck'
        db.create_table('accounts_scheduledcheck', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('notification_sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('accounts', ['ScheduledCheck'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'Featured', fields ['user', 'city']
        db.delete_unique('accounts_featured', ['user_id', 'city'])

        # Deleting model 'Service'
        db.delete_table('accounts_service')

        # Deleting model 'OpenHours'
        db.delete_table('accounts_openhours')

        # Deleting model 'Speciality'
        db.delete_table('accounts_speciality')

        # Deleting model 'ProfileImage'
        db.delete_table('accounts_profileimage')

        # Deleting model 'GalleryImage'
        db.delete_table('accounts_galleryimage')

        # Deleting model 'UserProfile'
        db.delete_table('accounts_userprofile')

        # Removing M2M table for field specialities on 'UserProfile'
        db.delete_table('accounts_userprofile_specialities')

        # Deleting model 'InviteCode'
        db.delete_table('accounts_invitecode')

        # Deleting model 'Featured'
        db.delete_table('accounts_featured')

        # Deleting model 'ScheduledCheck'
        db.delete_table('accounts_scheduledcheck')


    models = {
        'accounts.featured': {
            'Meta': {'unique_together': "(('user', 'city'),)", 'object_name': 'Featured'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accounts.UserProfile']"})
        },
        'accounts.galleryimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'GalleryImage'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'display_on_profile': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'accounts.invitecode': {
            'Meta': {'object_name': 'InviteCode'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invitecode_inviter'", 'null': 'True', 'to': "orm['auth.User']"}),
            'reciever': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invitecode_reciever'", 'null': 'True', 'to': "orm['auth.User']"}),
            'used': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'accounts.openhours': {
            'Meta': {'object_name': 'OpenHours'},
            'fri': ('django.db.models.fields.IntegerField', [], {'default': '480'}),
            'fri_closed': ('django.db.models.fields.IntegerField', [], {'default': '1020'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mon': ('django.db.models.fields.IntegerField', [], {'default': '480'}),
            'mon_closed': ('django.db.models.fields.IntegerField', [], {'default': '1020'}),
            'reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sat': ('django.db.models.fields.IntegerField', [], {'default': '480'}),
            'sat_closed': ('django.db.models.fields.IntegerField', [], {'default': '1020'}),
            'sun': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'sun_closed': ('django.db.models.fields.IntegerField', [], {'default': '-1'}),
            'thurs': ('django.db.models.fields.IntegerField', [], {'default': '480'}),
            'thurs_closed': ('django.db.models.fields.IntegerField', [], {'default': '1020'}),
            'tues': ('django.db.models.fields.IntegerField', [], {'default': '480'}),
            'tues_closed': ('django.db.models.fields.IntegerField', [], {'default': '1020'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'wed': ('django.db.models.fields.IntegerField', [], {'default': '480'}),
            'wed_closed': ('django.db.models.fields.IntegerField', [], {'default': '1020'})
        },
        'accounts.profileimage': {
            'Meta': {'object_name': 'ProfileImage'},
            'cropped': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '250', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'accounts.scheduledcheck': {
            'Meta': {'object_name': 'ScheduledCheck'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notification_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'accounts.service': {
            'Meta': {'ordering': "['order']", 'object_name': 'Service'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'display_on_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.IntegerField', [], {'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'max_length': '6'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'accounts.speciality': {
            'Meta': {'object_name': 'Speciality'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'approved_message_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '10', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '18', 'decimal_places': '10', 'blank': 'True'}),
            'number_on_profile': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'max_length': '1'}),
            'personal_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'picture_upload_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'profile_image_cropped': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profile_image_cropped'", 'unique': 'True', 'null': 'True', 'to': "orm['accounts.ProfileImage']"}),
            'profile_image_uncropped': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'profile_image_uncropped'", 'unique': 'True', 'null': 'True', 'to': "orm['accounts.ProfileImage']"}),
            'profile_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'blank': 'True'}),
            'profile_url': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'salon_adress': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'salon_city': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'salon_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'salon_phone_number': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'salon_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'show_booking_url': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'specialities': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['accounts.Speciality']", 'null': 'True', 'blank': 'True'}),
            'temporary_profile_url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'url_online_booking': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'visible_message_read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zip_adress': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['accounts']
