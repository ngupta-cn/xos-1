
from core.admin import ReadOnlyAwareAdmin, SliceInline
from core.middleware import get_request
from core.models import User
from django import forms
from django.contrib import admin
from subprocess import Popen, PIPE
from services.vpn.models import VPNService, VPNTenant, VPN_KIND

class VPNServiceAdmin(ReadOnlyAwareAdmin):
    model = VPNService
    verbose_name = "VPN Service"

    list_display = ("backend_status_icon", "name", "enabled")

    list_display_links = ('backend_status_icon', 'name', )

    fieldsets = [(None, {'fields': ['backend_status_text', 'name', 'enabled',
                                    'versionNumber', 'description', "view_url"],
                         'classes':['suit-tab suit-tab-general']})]

    readonly_fields = ('backend_status_text', )

    inlines = [SliceInline]

    extracontext_registered_admins = True

    user_readonly_fields = ["name", "enabled", "versionNumber", "description"]

    suit_form_tabs = (('general', 'VPN Service Details'),
                      ('administration', 'Tenants'),
                      ('slices', 'Slices'),)

    suit_form_includes = (('vpnserviceadmin.html',
                           'top',
                           'administration'),)

    def queryset(self, request):
        return VPNService.get_service_objects_by_user(request.user)

class VPNTenantForm(forms.ModelForm):
    creator = forms.ModelChoiceField(queryset=User.objects.all())
    server_key = forms.CharField(required=False, widget=forms.Textarea)
    client_conf = forms.CharField(required=False, widget=forms.Textarea)
    server_address = forms.GenericIPAddressField(protocol='IPv4', required=True)
    client_address = forms.GenericIPAddressField(protocol='IPv4', required=True)

    def __init__(self, *args, **kwargs):
        super(VPNTenantForm, self).__init__(*args, **kwargs)
        self.fields['kind'].widget.attrs['readonly'] = True
        self.fields['server_key'].widget.attrs['readonly'] = True
        self.fields['client_conf'].widget.attrs['readonly'] = True
        self.fields[
            'provider_service'].queryset = VPNService.get_service_objects().all()

        self.fields['kind'].initial = VPN_KIND

        if self.instance:
            self.fields['creator'].initial = self.instance.creator
            self.fields['server_key'].initial = self.instance.server_key
            self.fields['client_conf'].initial = self.instance.client_conf
            self.fields['server_address'].initial = self.instance.server_address
            self.fields['client_address'].initial = self.instance.client_address

        if (not self.instance) or (not self.instance.pk):
            self.fields['creator'].initial = get_request().user
            self.fields['server_key'].initial = self.generate_VPN_key()
            self.fields['server_address'].initial = "10.8.0.1"
            self.fields['client_address'].initial = "10.8.0.2"
            if VPNService.get_service_objects().exists():
                self.fields["provider_service"].initial = VPNService.get_service_objects().all()[0]

    def save(self, commit=True):
        self.instance.creator = self.cleaned_data.get("creator")
        self.instance.server_key = self.cleaned_data.get("server_key")
        self.instance.server_address = self.cleaned_data.get("server_address")
        self.instance.client_address = self.cleaned_data.get("client_address")
        self.instance.client_conf = self.generate_client_conf()
        return super(VPNTenantForm, self).save(commit=commit)

    def generate_VPN_key(self):
        proc = Popen("openvpn --genkey --secret /dev/stdout", shell=True, stdout=PIPE)
        (stdout, stderr) = proc.communicate()
        return stdout

    def generate_client_conf(self):
        conf = "remote " + self.instance.nat_ip + "\n"
        conf += "dev tun\n"
        conf += "ifconfig " + self.instance.client_address + " " + self.instance.server_address + "\n"
        conf += "secret static.key\n"
        conf += "keepalive 10 60\n"
        conf += "ping-timer-rem\n"
        conf += "persist-tun\n"
        conf += "persist-key"
        return conf

    class Meta:
        model = VPNTenant

class VPNTenantAdmin(ReadOnlyAwareAdmin):
    verbose_name = "VPN Tenant Admin"
    list_display = ('id', 'backend_status_icon', 'instance')
    list_display_links = ('id', 'backend_status_icon', 'instance')
    fieldsets = [(None, {'fields': ['backend_status_text', 'kind',
                                    'provider_service', 'instance', 'creator',
                                    'server_key', 'client_conf',
                                    'server_address', 'client_address'],
                         'classes': ['suit-tab suit-tab-general']})]
    readonly_fields = ('backend_status_text', 'instance')
    form = VPNTenantForm

    suit_form_tabs = (('general', 'Details'),)

    def queryset(self, request):
        return VPNTenant.get_tenant_objects_by_user(request.user)

# Associate the admin forms with the models.
admin.site.register(VPNService, VPNServiceAdmin)
admin.site.register(VPNTenant, VPNTenantAdmin)
