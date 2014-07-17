# -*- coding:utf-8 -*-

""" Cogenda Common Constants """


class Const:
    """
    Cogenda Common Constants
    refer: http://code.activestate.com/recipes/65207-constants-in-python
    """

    class ConstError(TypeError):
        pass  # base exception class

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const.%s" % name)
        if not name.isupper():
            raise self.ConstCaseError('const name %r is not all uppercase' % name)
        self.__dict__[name] = value

    # Vendor type
    VENDOR_TYPE_OOS = 'oss'
    VENDOR_TYPE_S3 = 's3'

    # Vendor display name
    VENDOR_OOS_DISPLAY_NAME = 'AliYun'
    VENDOR_S3_DISPLAY_NAME = 'AWS S3'

    # Resource type
    RESOURCE_TYPE_PUBLIC_PUBLICATIONS = '1'
    RESOURCE_TYPE_PUBLIC_DOCUMENTATION = '2'
    RESOURCE_TYPE_PUBLIC_EXAMPLES = '3'
    RESOURCE_TYPE_ALLUSER_SOFTWARE_PACKAGES = '4'
    RESOURCE_TYPE_ALLUSER_INSTALLER = '5'
    RESOURCE_TYPE_PRIVATE = '6'

    # User type
    USER_TYPE_RESOURCE = '1'
    USER_TYPE_RESOURCE_OWNER = '2'
    USER_TYPE_ADMINISTRATOR = '3'

    # Security
    CLIENT_TYPE_WEB = 'web'
    CLIENT_TYPE_ADMIN = 'admin'
    PROTECTED_RESOURCES = ['/admin/user-mgmt', '/admin/resources']

"""
Replace module entry in sys.modules[__name__] with instance of Const
"""
import sys
_ref, sys.modules[__name__] = sys.modules[__name__], Const()
