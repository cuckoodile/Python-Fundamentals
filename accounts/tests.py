import io
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from PIL import Image
from rest_framework.test import APITestCase

from .models import BaseUser, ContactType

TEMP_MEDIA = tempfile.mkdtemp()


def make_image(name='avatar.png'):
    buffer = io.BytesIO()
    Image.new('RGB', (20, 20), (255, 0, 0)).save(buffer, 'PNG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class ApiFlowTests(APITestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA, ignore_errors=True)

    def register(self, username='user01', **extra):
        data = {
            'username': username, 'email': '', 'first_name': 'Ian', 'last_name': 'Sube',
            'password': 'S3cure!pass99', 'confirm_password': 'S3cure!pass99', **extra,
        }
        return self.client.post('/api/users/', data, format='multipart')

    def test_register_without_avatar_uses_default(self):
        res = self.register()
        self.assertEqual(res.status_code, 201, res.data)
        self.assertTrue(res.data['profile'].endswith('users/default.jfif'))
        self.assertNotIn('password', res.data)

    def test_register_with_avatar(self):
        res = self.register(profile=make_image())
        self.assertEqual(res.status_code, 201, res.data)
        self.assertIn('/media/users/avatar', res.data['profile'])

    def test_register_password_mismatch(self):
        res = self.client.post('/api/users/', {
            'username': 'x', 'password': 'S3cure!pass99', 'confirm_password': 'nope',
        }, format='multipart')
        self.assertEqual(res.status_code, 400)
        self.assertIn('confirm_password', res.data)

    def test_login_me_logout(self):
        self.register()

        bad = self.client.post('/api/auth/login/', {'username': 'user01', 'password': 'wrong'}, format='json')
        self.assertEqual(bad.status_code, 400)
        self.assertIn('detail', bad.data)

        res = self.client.post('/api/auth/login/', {'username': 'user01', 'password': 'S3cure!pass99'}, format='json')
        self.assertEqual(res.status_code, 200, res.data)
        token = res.data['token']
        self.assertEqual(res.data['user']['username'], 'user01')

        me = self.client.get('/api/auth/me/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.data['username'], 'user01')

        self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)

        out = self.client.post('/api/auth/logout/', HTTP_AUTHORIZATION=f'Token {token}')
        self.assertEqual(out.status_code, 204)
        self.assertEqual(self.client.get('/api/auth/me/', HTTP_AUTHORIZATION=f'Token {token}').status_code, 401)

    def test_patch_user_multipart_with_avatar(self):
        uid = self.register().data['id']
        res = self.client.patch(
            f'/api/users/{uid}/',
            {'first_name': 'Changed', 'email': 'a@b.co', 'profile': make_image('new.png')},
            format='multipart',
        )
        self.assertEqual(res.status_code, 200, res.data)
        self.assertEqual(res.data['first_name'], 'Changed')
        self.assertIn('/media/users/new', res.data['profile'])

    def test_soft_delete_blocks_login_and_listing(self):
        uid = self.register().data['id']
        self.assertEqual(self.client.delete(f'/api/users/{uid}/').status_code, 204)
        self.assertEqual(self.client.get(f'/api/users/{uid}/').status_code, 404)
        self.assertEqual(self.client.get('/api/users/').data, [])
        res = self.client.post('/api/auth/login/', {'username': 'user01', 'password': 'S3cure!pass99'}, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertTrue(BaseUser.objects.filter(pk=uid, is_active=False).exists())

    def test_contact_types_and_contacts_crud(self):
        uid = self.register().data['id']

        ct = self.client.post('/api/contact-types/', {'name': 'Github'}, format='json')
        self.assertEqual(ct.status_code, 201)
        ct_id = ct.data['id']
        self.client.patch(f'/api/contact-types/{ct_id}/', {'name': 'GitHub'}, format='json')
        self.assertEqual(ContactType.objects.get(pk=ct_id).name, 'GitHub')

        # React sends type_id as a string from the <select>
        c = self.client.post('/api/contacts/', {'owner': uid, 'type_id': str(ct_id), 'value': 'https://github.com/x'}, format='json')
        self.assertEqual(c.status_code, 201, c.data)
        cid = c.data['id']

        user = self.client.get(f'/api/users/{uid}/').data
        self.assertEqual(user['contacts'][0]['type']['name'], 'GitHub')

        p = self.client.patch(f'/api/contacts/{cid}/', {'value': 'https://github.com/y'}, format='json')
        self.assertEqual(p.data['value'], 'https://github.com/y')

        self.assertEqual(self.client.delete(f'/api/contacts/{cid}/').status_code, 204)
        self.assertEqual(self.client.get(f'/api/users/{uid}/').data['contacts'], [])

        # deleting a type cascades to its contacts
        c2 = self.client.post('/api/contacts/', {'owner': uid, 'type_id': ct_id, 'value': 'z'}, format='json')
        self.assertEqual(c2.status_code, 201)
        self.assertEqual(self.client.delete(f'/api/contact-types/{ct_id}/').status_code, 204)
        self.assertEqual(self.client.get('/api/contacts/').data, [])
