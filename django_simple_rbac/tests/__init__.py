from os import path
from django.test.testcases import TestCase
from ..registry import load_registry_from_yaml
from models import Member, Moderator, Admin, ResourceAdapter, RoleAdapter


class RegistryTestCase(TestCase):

    def get_registry(self, name):
        acl_path = path.realpath(path.dirname(__file__) + '/acl')
        return load_registry_from_yaml('{}/{}.yaml'.format(acl_path, name))

    def test_yaml_registry1(self):
        """
        Test a simple registry
        """
        registry = self.get_registry('registry1')
        # undefined role
        self.assertRaises(AssertionError, lambda: registry.is_allowed('bob', 'view', 'post'))
        # undefined operation
        self.assertIsNone(registry.is_allowed('anonymous', 'eat', 'post'))
        # undefined resource
        self.assertRaises(AssertionError, lambda: registry.is_allowed('anonymous', 'view', 'comment'))
        # anonymous
        self.assertTrue(registry.is_allowed('anonymous', 'list', 'post'))
        self.assertTrue(registry.is_allowed('anonymous', 'view', 'post'))
        self.assertFalse(registry.is_allowed('anonymous', 'create', 'post'))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', 'post'))
        self.assertFalse(registry.is_allowed('anonymous', 'list', 'member'))
        self.assertFalse(registry.is_allowed('anonymous', 'view', 'member'))
        self.assertFalse(registry.is_allowed('anonymous', 'update', 'member'))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', 'member'))
        # member
        self.assertTrue(registry.is_allowed('member', 'list', 'post'))
        self.assertTrue(registry.is_allowed('member', 'view', 'post'))
        self.assertTrue(registry.is_allowed('member', 'create', 'post'))
        self.assertFalse(registry.is_allowed('member', 'delete', 'post'))
        self.assertTrue(registry.is_allowed('member', 'list', 'member'))
        self.assertTrue(registry.is_allowed('member', 'view', 'member'))
        self.assertFalse(registry.is_allowed('member', 'update', 'member'))
        self.assertFalse(registry.is_allowed('member', 'delete', 'member'))
        # moderator
        self.assertTrue(registry.is_allowed('moderator', 'list', 'post'))
        self.assertTrue(registry.is_allowed('moderator', 'view', 'post'))
        self.assertTrue(registry.is_allowed('moderator', 'create', 'post'))
        self.assertTrue(registry.is_allowed('moderator', 'delete', 'post'))
        self.assertTrue(registry.is_allowed('moderator', 'list', 'member'))
        self.assertTrue(registry.is_allowed('moderator', 'view', 'member'))
        self.assertFalse(registry.is_allowed('moderator', 'update', 'member'))
        self.assertFalse(registry.is_allowed('moderator', 'delete', 'member'))
        # admin
        self.assertTrue(registry.is_allowed('admin', 'list', 'post'))
        self.assertTrue(registry.is_allowed('admin', 'view', 'post'))
        self.assertTrue(registry.is_allowed('admin', 'create', 'post'))
        self.assertTrue(registry.is_allowed('admin', 'delete', 'post'))
        self.assertTrue(registry.is_allowed('admin', 'list', 'member'))
        self.assertTrue(registry.is_allowed('admin', 'view', 'member'))
        self.assertTrue(registry.is_allowed('admin', 'update', 'member'))
        self.assertTrue(registry.is_allowed('admin', 'delete', 'member'))

    def test_yaml_registry2(self):
        """
        Test a more complex registry with an assertion
        """
        registry = self.get_registry('registry2')
        # undefined role
        self.assertRaises(AssertionError, lambda: registry.is_allowed('bob', 'view', 'post'))
        # undefined operation
        self.assertIsNone(registry.is_allowed('anonymous', 'eat', 'post'))
        # undefined resource
        self.assertRaises(AssertionError, lambda: registry.is_allowed('anonymous', 'view', 'comment'))
        # anonymous
        self.assertTrue(registry.is_allowed('anonymous', 'list', 'post'))
        self.assertTrue(registry.is_allowed('anonymous', 'view', 'post'))
        self.assertFalse(registry.is_allowed('anonymous', 'create', 'post'))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', 'post'))
        self.assertFalse(registry.is_allowed('anonymous', 'list', 'member'))
        self.assertFalse(registry.is_allowed('anonymous', 'view', 'member'))
        self.assertFalse(registry.is_allowed('anonymous', 'update', 'member'))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', 'member'))
        self.assertFalse(registry.is_allowed('anonymous', 'list', 'moderator'))
        self.assertFalse(registry.is_allowed('anonymous', 'view', 'moderator'))
        self.assertFalse(registry.is_allowed('anonymous', 'update', 'moderator'))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', 'moderator'))
        self.assertFalse(registry.is_allowed('anonymous', 'list', 'admin'))
        self.assertFalse(registry.is_allowed('anonymous', 'view', 'admin'))
        self.assertFalse(registry.is_allowed('anonymous', 'update', 'admin'))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', 'admin'))
        # member
        self.assertTrue(registry.is_allowed('member', 'list', 'post'))
        self.assertTrue(registry.is_allowed('member', 'view', 'post'))
        self.assertTrue(registry.is_allowed('member', 'create', 'post'))
        self.assertFalse(registry.is_allowed('member', 'delete', 'post'))
        self.assertTrue(registry.is_allowed('member', 'list', 'member'))
        self.assertTrue(registry.is_allowed('member', 'view', 'member'))
        self.assertFalse(registry.is_allowed('member', 'update', 'member'))
        self.assertFalse(registry.is_allowed('member', 'delete', 'member'))
        self.assertTrue(registry.is_allowed('member', 'list', 'moderator'))
        self.assertTrue(registry.is_allowed('member', 'view', 'moderator'))
        self.assertFalse(registry.is_allowed('member', 'update', 'moderator'))
        self.assertFalse(registry.is_allowed('member', 'delete', 'moderator'))
        self.assertTrue(registry.is_allowed('member', 'list', 'admin'))
        self.assertTrue(registry.is_allowed('member', 'view', 'admin'))
        self.assertFalse(registry.is_allowed('member', 'update', 'admin'))
        self.assertFalse(registry.is_allowed('member', 'delete', 'admin'))
        # moderator
        self.assertTrue(registry.is_allowed('moderator', 'list', 'post'))
        self.assertTrue(registry.is_allowed('moderator', 'view', 'post'))
        self.assertTrue(registry.is_allowed('moderator', 'create', 'post'))
        self.assertTrue(registry.is_allowed('moderator', 'delete', 'post'))
        self.assertTrue(registry.is_allowed('moderator', 'list', 'member'))
        self.assertTrue(registry.is_allowed('moderator', 'view', 'member'))
        self.assertFalse(registry.is_allowed('moderator', 'update', 'member'))
        self.assertFalse(registry.is_allowed('moderator', 'delete', 'member'))
        self.assertTrue(registry.is_allowed('moderator', 'list', 'moderator'))
        self.assertTrue(registry.is_allowed('moderator', 'view', 'moderator'))
        self.assertFalse(registry.is_allowed('moderator', 'update', 'moderator'))
        self.assertFalse(registry.is_allowed('moderator', 'delete', 'moderator'))
        self.assertTrue(registry.is_allowed('moderator', 'list', 'admin'))
        self.assertTrue(registry.is_allowed('moderator', 'view', 'admin'))
        self.assertFalse(registry.is_allowed('moderator', 'update', 'admin'))
        self.assertFalse(registry.is_allowed('moderator', 'delete', 'admin'))
        # admin
        self.assertTrue(registry.is_allowed('admin', 'list', 'post'))
        self.assertTrue(registry.is_allowed('admin', 'view', 'post'))
        self.assertTrue(registry.is_allowed('admin', 'create', 'post'))
        self.assertTrue(registry.is_allowed('admin', 'delete', 'post'))
        self.assertTrue(registry.is_allowed('admin', 'list', 'member'))
        self.assertTrue(registry.is_allowed('admin', 'view', 'member'))
        self.assertTrue(registry.is_allowed('admin', 'update', 'member'))
        self.assertTrue(registry.is_allowed('admin', 'delete', 'member'))
        self.assertTrue(registry.is_allowed('admin', 'list', 'moderator'))
        self.assertTrue(registry.is_allowed('admin', 'view', 'moderator'))
        self.assertTrue(registry.is_allowed('admin', 'update', 'moderator'))
        self.assertTrue(registry.is_allowed('admin', 'delete', 'moderator'))
        self.assertTrue(registry.is_allowed('admin', 'list', 'admin'))
        self.assertTrue(registry.is_allowed('admin', 'view', 'admin'))
        self.assertFalse(registry.is_allowed('admin', 'update', 'admin'))
        self.assertFalse(registry.is_allowed('admin', 'delete', 'admin'))

    def test_yaml_registry3(self):
        """
        Test a more complex registry with adapters
        """
        registry = self.get_registry('registry3')
        karl = Member('Karl')
        simon = Moderator('Simon')
        nizar = Admin('Nizar')
        albin = Admin('Albin')

        # anonymous
        self.assertTrue(registry.is_allowed('anonymous', 'list', 'post'))
        self.assertTrue(registry.is_allowed('anonymous', 'view', 'post'))
        self.assertFalse(registry.is_allowed('anonymous', 'create', 'post'))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', 'post'))
        self.assertFalse(registry.is_allowed('anonymous', 'list', ResourceAdapter(karl)))
        self.assertFalse(registry.is_allowed('anonymous', 'view', ResourceAdapter(karl)))
        self.assertFalse(registry.is_allowed('anonymous', 'update', ResourceAdapter(karl)))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', ResourceAdapter(karl)))
        self.assertFalse(registry.is_allowed('anonymous', 'list', ResourceAdapter(simon)))
        self.assertFalse(registry.is_allowed('anonymous', 'view', ResourceAdapter(simon)))
        self.assertFalse(registry.is_allowed('anonymous', 'update', ResourceAdapter(simon)))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', ResourceAdapter(simon)))
        self.assertFalse(registry.is_allowed('anonymous', 'list', ResourceAdapter(albin)))
        self.assertFalse(registry.is_allowed('anonymous', 'view', ResourceAdapter(albin)))
        self.assertFalse(registry.is_allowed('anonymous', 'update', ResourceAdapter(albin)))
        self.assertFalse(registry.is_allowed('anonymous', 'delete', ResourceAdapter(albin)))
        # member
        self.assertTrue(registry.is_allowed(RoleAdapter(karl), 'list', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(karl), 'view', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(karl), 'create', 'post'))
        self.assertFalse(registry.is_allowed(RoleAdapter(karl), 'delete', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(karl), 'list', ResourceAdapter(karl)))
        self.assertTrue(registry.is_allowed(RoleAdapter(karl), 'view', ResourceAdapter(karl)))
        self.assertFalse(registry.is_allowed(RoleAdapter(karl), 'update', ResourceAdapter(karl)))
        self.assertFalse(registry.is_allowed(RoleAdapter(karl), 'delete', ResourceAdapter(karl)))
        self.assertTrue(registry.is_allowed(RoleAdapter(karl), 'list', ResourceAdapter(simon)))
        self.assertTrue(registry.is_allowed(RoleAdapter(karl), 'view', ResourceAdapter(simon)))
        self.assertFalse(registry.is_allowed(RoleAdapter(karl), 'update', ResourceAdapter(simon)))
        self.assertFalse(registry.is_allowed(RoleAdapter(karl), 'delete', ResourceAdapter(simon)))
        self.assertTrue(registry.is_allowed(RoleAdapter(karl), 'list', ResourceAdapter(albin)))
        self.assertTrue(registry.is_allowed(RoleAdapter(karl), 'view', ResourceAdapter(albin)))
        self.assertFalse(registry.is_allowed(RoleAdapter(karl), 'update', ResourceAdapter(albin)))
        self.assertFalse(registry.is_allowed(RoleAdapter(karl), 'delete', ResourceAdapter(albin)))
        # moderator
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'list', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'view', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'create', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'delete', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'list', ResourceAdapter(karl)))
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'view', ResourceAdapter(karl)))
        self.assertFalse(registry.is_allowed(RoleAdapter(simon), 'update', ResourceAdapter(karl)))
        self.assertFalse(registry.is_allowed(RoleAdapter(simon), 'delete', ResourceAdapter(karl)))
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'list', ResourceAdapter(simon)))
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'view', ResourceAdapter(simon)))
        self.assertFalse(registry.is_allowed(RoleAdapter(simon), 'update', ResourceAdapter(simon)))
        self.assertFalse(registry.is_allowed(RoleAdapter(simon), 'delete', ResourceAdapter(simon)))
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'list', ResourceAdapter(albin)))
        self.assertTrue(registry.is_allowed(RoleAdapter(simon), 'view', ResourceAdapter(albin)))
        self.assertFalse(registry.is_allowed(RoleAdapter(simon), 'update', ResourceAdapter(albin)))
        self.assertFalse(registry.is_allowed(RoleAdapter(simon), 'delete', ResourceAdapter(albin)))
        # admin
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'list', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'view', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'create', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'delete', 'post'))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'list', ResourceAdapter(karl)))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'view', ResourceAdapter(karl)))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'update', ResourceAdapter(karl)))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'delete', ResourceAdapter(karl)))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'list', ResourceAdapter(simon)))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'view', ResourceAdapter(simon)))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'update', ResourceAdapter(simon)))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'delete', ResourceAdapter(simon)))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'list', ResourceAdapter(albin)))
        self.assertTrue(registry.is_allowed(RoleAdapter(nizar), 'view', ResourceAdapter(albin)))
        self.assertFalse(registry.is_allowed(RoleAdapter(nizar), 'update', ResourceAdapter(albin)))
        self.assertFalse(registry.is_allowed(RoleAdapter(nizar), 'delete', ResourceAdapter(albin)))

