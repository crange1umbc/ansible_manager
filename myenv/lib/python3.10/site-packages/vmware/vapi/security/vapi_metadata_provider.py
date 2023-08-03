"""
Authorization API Provider filter
"""

__author__ = 'VMware, Inc.'
__copyright__ = 'Copyright 2021 VMware, Inc.  All rights reserved. -- VMware Confidential'  # pylint: disable=line-too-long


# TODO Remove hardcoded metadata once it is available in the generated bindings
def get_vapi_metadata():
    return """
{
  "authentication": {
    "component": {
      "name": "com.vmware.vapi",
      "schemes": {
        "NoAuthentication": {
          "type": "SessionLess",
          "authenticationScheme": "com.vmware.vapi.std.security.no_authentication"
        }
      },
      "packages": {
      },
      "services": {
      },
      "operations": {
        "com.vmware.vapi.metadata.routing.component.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.routing.component.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.routing.component.fingerprint": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.routing.service.operation.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.routing.service.operation.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.routing.package.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.routing.package.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.routing.service.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.routing.service.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.cli.command.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.cli.command.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.cli.command.fingerprint": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.cli.namespace.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.cli.namespace.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.cli.namespace.fingerprint": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.privilege.component.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.privilege.component.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.privilege.component.fingerprint": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.privilege.service.operation.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.privilege.service.operation.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.privilege.package.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.privilege.package.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.privilege.service.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.privilege.service.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.authentication.component.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.authentication.component.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.authentication.component.fingerprint": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.authentication.service.operation.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.authentication.service.operation.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.authentication.package.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.authentication.package.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.authentication.service.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.authentication.service.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.component.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.component.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.component.fingerprint": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.enumeration.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.enumeration.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.resource.model.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.service.operation.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.service.operation.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.service.hidden.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.package.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.package.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.resource.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.service.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.service.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.structure.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.metadata.metamodel.structure.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.std.introspection.operation.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.std.introspection.operation.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.std.introspection.provider.get": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.std.introspection.service.list": [
          "NoAuthentication"
        ],
        "com.vmware.vapi.std.introspection.service.get": [
          "NoAuthentication"
        ]
      }
    }
  }
}"""
