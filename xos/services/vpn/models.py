from core.models import Service, TenantWithContainer
from django.db import transaction

VPN_KIND = "vpn"

class VPNService(Service):
    KIND = VPN_KIND

    class Meta:
        proxy = True
        # The name used to find this service, all directories are named this
        app_label = "vpn"
        verbose_name = "VPN Service"

class VPNTenant(TenantWithContainer):

    class Meta:
        proxy = True
        verbose_name = "VPN Tenant"

    KIND = VPN_KIND

    sync_attributes = ("nat_ip", "nat_mac",)

    default_attributes = {'server_key': 'Error key not found',
                          'client_conf': 'Configuration not found',
                          'server_address': '10.8.0.1',
                          'client_address': '10.8.0.2'}

    def __init__(self, *args, **kwargs):
        vpn_services = VPNService.get_service_objects().all()
        if vpn_services:
            self._meta.get_field(
                "provider_service").default = vpn_services[0].id
        super(VPNTenant, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(VPNTenant, self).save(*args, **kwargs)
        model_policy_vpn_tenant(self.pk)

    def delete(self, *args, **kwargs):
        self.cleanup_container()
        super(VPNTenant, self).delete(*args, **kwargs)

    @property
    def server_key(self):
        return self.get_attribute(
            "server_key",
            self.default_attributes['server_key'])

    @server_key.setter
    def server_key(self, value):
        self.set_attribute("server_key", value)

    @property
    def addresses(self):
        if (not self.id) or (not self.instance):
            return {}

        addresses = {}
        # The ports field refers to networks for the instance.
        # This loop stores the details for the NAT network that will be
        # necessary for ansible.
        for ns in self.instance.ports.all():
            if "nat" in ns.network.name.lower():
                addresses["nat"] = (ns.ip, ns.mac)
        return addresses

    # This getter is necessary because nat_ip is a sync_attribute
    @property
    def nat_ip(self):
        return self.addresses.get("nat", (None, None))[0]

    # This getter is necessary because nat_mac is a sync_attribute
    @property
    def nat_mac(self):
        return self.addresses.get("nat", (None, None))[1]

    @property
    def server_address(self):
        return self.get_attribute(
            'server_address',
            self.default_attributes['server_address'])

    @server_address.setter
    def server_address(self, value):
        self.set_attribute("server_address", value)

    @property
    def client_address(self):
        return self.get_attribute(
            'client_address',
            self.default_attributes['client_address'])

    @client_address.setter
    def client_address(self, value):
        self.set_attribute("client_address", value)

    @property
    def client_conf(self):
        return self.get_attribute(
            "client_conf",
            self.default_attributes['client_conf'])

    @client_conf.setter
    def client_conf(self, value):
        self.set_attribute("client_conf", value)


def model_policy_vpn_tenant(pk):
    # This section of code is atomic to prevent race conditions
    with transaction.atomic():
        # We find all of the tenants that are waiting to update
        tenant = VPNTenant.objects.select_for_update().filter(pk=pk)
        if not tenant:
            return
        # Since this code is atomic it is safe to always use the first tenant
        tenant = tenant[0]
        tenant.manage_container()
