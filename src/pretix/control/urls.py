#
# This file is part of pretix (Community Edition).
#
# Copyright (C) 2014-2020 Raphael Michel and contributors
# Copyright (C) 2020-2021 rami.io GmbH and contributors
#
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General
# Public License as published by the Free Software Foundation in version 3 of the License.
#
# ADDITIONAL TERMS APPLY: Pursuant to Section 7 of the GNU Affero General Public License, additional terms are
# applicable granting you additional permissions and placing additional restrictions on your usage of this software.
# Please refer to the pretix LICENSE file to obtain the full terms applicable to this work. If you did not receive
# this file, see <https://pretix.eu/about/en/license>.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more
# details.
#
# You should have received a copy of the GNU Affero General Public License along with this program.  If not, see
# <https://www.gnu.org/licenses/>.
#

# This file is based on an earlier version of pretix which was released under the Apache License 2.0. The full text of
# the Apache License 2.0 can be obtained at <http://www.apache.org/licenses/LICENSE-2.0>.
#
# This file may have since been changed and any changes are released under the terms of AGPLv3 as described above. A
# full history of changes and contributors is available at <https://github.com/pretix/pretix>.
#
# This file contains Apache-licensed contributions copyrighted by: Daniel, Enrique Saez, Jahongir, Mason Mohkami,
# Sohalt, Tobias Kunze, jasonwaiting@live.hk, luto, oocf
#
# Unless required by applicable law or agreed to in writing, software distributed under the Apache License 2.0 is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under the License.

from django.conf.urls import include, re_path
from django.views.generic.base import RedirectView

from pretix.control.views import (
    auth, checkin, dashboards, discounts, event, geo, global_settings, item,
    main, oauth, orderimport, orders, organizer, pdf, search, shredder,
    subevents, typeahead, user, users, vouchers, waitinglist,
)

urlpatterns = [
    re_path(r'^logout$', auth.logout, name='auth.logout'),
    re_path(r'^login$', auth.login, name='auth.login'),
    re_path(r'^login/2fa$', auth.Login2FAView.as_view(), name='auth.login.2fa'),
    re_path(r'^register$', auth.register, name='auth.register'),
    re_path(r'^invite/(?P<token>[a-zA-Z0-9]+)$', auth.invite, name='auth.invite'),
    re_path(r'^forgot$', auth.Forgot.as_view(), name='auth.forgot'),
    re_path(r'^forgot/recover$', auth.Recover.as_view(), name='auth.forgot.recover'),
    re_path(r'^$', dashboards.user_index, name='index'),
    re_path(r'^widgets.json$', dashboards.user_index_widgets_lazy, name='index.widgets'),
    re_path(r'^global/settings/$', global_settings.GlobalSettingsView.as_view(), name='global.settings'),
    re_path(r'^global/update/$', global_settings.UpdateCheckView.as_view(), name='global.update'),
    re_path(r'^global/license/$', global_settings.LicenseCheckView.as_view(), name='global.license'),
    re_path(r'^global/message/$', global_settings.MessageView.as_view(), name='global.message'),
    re_path(r'^logdetail/$', global_settings.LogDetailView.as_view(), name='global.logdetail'),
    re_path(r'^logdetail/payment/$', global_settings.PaymentDetailView.as_view(), name='global.paymentdetail'),
    re_path(r'^logdetail/refund/$', global_settings.RefundDetailView.as_view(), name='global.refunddetail'),
    re_path(r'^geocode/$', geo.GeoCodeView.as_view(), name='global.geocode'),
    re_path(r'^reauth/$', user.ReauthView.as_view(), name='user.reauth'),
    re_path(r'^sudo/$', user.StartStaffSession.as_view(), name='user.sudo'),
    re_path(r'^sudo/stop/$', user.StopStaffSession.as_view(), name='user.sudo.stop'),
    re_path(r'^sudo/(?P<id>\d+)/$', user.EditStaffSession.as_view(), name='user.sudo.edit'),
    re_path(r'^sudo/sessions/$', user.StaffSessionList.as_view(), name='user.sudo.list'),
    re_path(r'^users/$', users.UserListView.as_view(), name='users'),
    re_path(r'^users/select2$', typeahead.users_select2, name='users.select2'),
    re_path(r'^users/add$', users.UserCreateView.as_view(), name='users.add'),
    re_path(r'^users/impersonate/stop', users.UserImpersonateStopView.as_view(), name='users.impersonate.stop'),
    re_path(r'^users/(?P<id>\d+)/$', users.UserEditView.as_view(), name='users.edit'),
    re_path(r'^users/(?P<id>\d+)/reset$', users.UserResetView.as_view(), name='users.reset'),
    re_path(r'^users/(?P<id>\d+)/impersonate', users.UserImpersonateView.as_view(), name='users.impersonate'),
    re_path(r'^users/(?P<id>\d+)/anonymize', users.UserAnonymizeView.as_view(), name='users.anonymize'),
    re_path(r'^pdf/editor/webfonts.css', pdf.FontsCSSView.as_view(), name='pdf.css'),
    re_path(r'^settings/?$', user.UserSettings.as_view(), name='user.settings'),
    re_path(r'^settings/history/$', user.UserHistoryView.as_view(), name='user.settings.history'),
    re_path(r'^settings/notifications/$', user.UserNotificationsEditView.as_view(), name='user.settings.notifications'),
    re_path(r'^settings/notifications/off/(?P<id>\d+)/(?P<token>[^/]+)/$', user.UserNotificationsDisableView.as_view(),
            name='user.settings.notifications.off'),
    re_path(r'^settings/oauth/authorized/$', oauth.AuthorizationListView.as_view(),
            name='user.settings.oauth.list'),
    re_path(r'^settings/oauth/authorized/(?P<pk>\d+)/revoke$', oauth.AuthorizationRevokeView.as_view(),
            name='user.settings.oauth.revoke'),
    re_path(r'^settings/oauth/apps/$', oauth.OAuthApplicationListView.as_view(),
            name='user.settings.oauth.apps'),
    re_path(r'^settings/oauth/apps/add$', oauth.OAuthApplicationRegistrationView.as_view(),
            name='user.settings.oauth.apps.register'),
    re_path(r'^settings/oauth/apps/(?P<pk>\d+)/$', oauth.OAuthApplicationUpdateView.as_view(),
            name='user.settings.oauth.app'),
    re_path(r'^settings/oauth/apps/(?P<pk>\d+)/disable$', oauth.OAuthApplicationDeleteView.as_view(),
            name='user.settings.oauth.app.disable'),
    re_path(r'^settings/oauth/apps/(?P<pk>\d+)/roll$', oauth.OAuthApplicationRollView.as_view(),
            name='user.settings.oauth.app.roll'),
    re_path(r'^settings/2fa/$', user.User2FAMainView.as_view(), name='user.settings.2fa'),
    re_path(r'^settings/2fa/add$', user.User2FADeviceAddView.as_view(), name='user.settings.2fa.add'),
    re_path(r'^settings/2fa/enable', user.User2FAEnableView.as_view(), name='user.settings.2fa.enable'),
    re_path(r'^settings/2fa/disable', user.User2FADisableView.as_view(), name='user.settings.2fa.disable'),
    re_path(r'^settings/2fa/regenemergency', user.User2FARegenerateEmergencyView.as_view(),
            name='user.settings.2fa.regenemergency'),
    re_path(r'^settings/2fa/totp/(?P<device>[0-9]+)/confirm', user.User2FADeviceConfirmTOTPView.as_view(),
            name='user.settings.2fa.confirm.totp'),
    re_path(r'^settings/2fa/webauthn/(?P<device>[0-9]+)/confirm', user.User2FADeviceConfirmWebAuthnView.as_view(),
            name='user.settings.2fa.confirm.webauthn'),
    re_path(r'^settings/2fa/(?P<devicetype>[^/]+)/(?P<device>[0-9]+)/delete', user.User2FADeviceDeleteView.as_view(),
            name='user.settings.2fa.delete'),
    re_path(r'^organizers/$', organizer.OrganizerList.as_view(), name='organizers'),
    re_path(r'^organizers/add$', organizer.OrganizerCreate.as_view(), name='organizers.add'),
    re_path(r'^organizers/select2$', typeahead.organizer_select2, name='organizers.select2'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/$', organizer.OrganizerDetail.as_view(), name='organizer'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/edit$', organizer.OrganizerUpdate.as_view(), name='organizer.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/settings/email$',
            organizer.OrganizerMailSettings.as_view(), name='organizer.settings.mail'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/settings/email/setup$',
            organizer.MailSettingsSetup.as_view(), name='organizer.settings.mail.setup'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/settings/email/preview$',
            organizer.MailSettingsPreview.as_view(), name='organizer.settings.mail.preview'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/delete$', organizer.OrganizerDelete.as_view(), name='organizer.delete'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/settings/display$', organizer.OrganizerDisplaySettings.as_view(),
            name='organizer.display'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/properties$', organizer.EventMetaPropertyListView.as_view(), name='organizer.properties'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/property/add$', organizer.EventMetaPropertyCreateView.as_view(),
            name='organizer.property.add'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/property/(?P<property>[^/]+)/edit$', organizer.EventMetaPropertyUpdateView.as_view(),
            name='organizer.property.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/property/(?P<property>[^/]+)/delete$', organizer.EventMetaPropertyDeleteView.as_view(),
            name='organizer.property.delete'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/membershiptypes$', organizer.MembershipTypeListView.as_view(), name='organizer.membershiptypes'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/membershiptype/add$', organizer.MembershipTypeCreateView.as_view(),
            name='organizer.membershiptype.add'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/membershiptype/(?P<type>[^/]+)/edit$', organizer.MembershipTypeUpdateView.as_view(),
            name='organizer.membershiptype.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/membershiptype/(?P<type>[^/]+)/delete$', organizer.MembershipTypeDeleteView.as_view(),
            name='organizer.membershiptype.delete'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/customers$', organizer.CustomerListView.as_view(), name='organizer.customers'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/customers/select2$', typeahead.customer_select2, name='organizer.customers.select2'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/customer/add$',
            organizer.CustomerCreateView.as_view(), name='organizer.customer.create'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/customer/(?P<customer>[^/]+)/$',
            organizer.CustomerDetailView.as_view(), name='organizer.customer'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/customer/(?P<customer>[^/]+)/edit$',
            organizer.CustomerUpdateView.as_view(), name='organizer.customer.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/customer/(?P<customer>[^/]+)/membership/add$',
            organizer.MembershipCreateView.as_view(), name='organizer.customer.membership.add'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/customer/(?P<customer>[^/]+)/membership/(?P<id>[^/]+)/edit$',
            organizer.MembershipUpdateView.as_view(), name='organizer.customer.membership.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/customer/(?P<customer>[^/]+)/membership/(?P<id>[^/]+)/delete$',
            organizer.MembershipDeleteView.as_view(), name='organizer.customer.membership.delete'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/customer/(?P<customer>[^/]+)/anonymize$',
            organizer.CustomerAnonymizeView.as_view(), name='organizer.customer.anonymize'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/giftcards$', organizer.GiftCardListView.as_view(), name='organizer.giftcards'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/giftcard/add$', organizer.GiftCardCreateView.as_view(), name='organizer.giftcard.add'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/giftcard/(?P<giftcard>[^/]+)/$', organizer.GiftCardDetailView.as_view(), name='organizer.giftcard'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/giftcard/(?P<giftcard>[^/]+)/edit$', organizer.GiftCardUpdateView.as_view(),
            name='organizer.giftcard.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/webhooks$', organizer.WebHookListView.as_view(), name='organizer.webhooks'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/webhook/add$', organizer.WebHookCreateView.as_view(),
            name='organizer.webhook.add'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/webhook/(?P<webhook>[^/]+)/edit$', organizer.WebHookUpdateView.as_view(),
            name='organizer.webhook.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/webhook/(?P<webhook>[^/]+)/logs$', organizer.WebHookLogsView.as_view(),
            name='organizer.webhook.logs'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/devices$', organizer.DeviceListView.as_view(), name='organizer.devices'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/device/add$', organizer.DeviceCreateView.as_view(),
            name='organizer.device.add'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/device/bulk_edit$', organizer.DeviceBulkUpdateView.as_view(),
            name='organizer.device.bulk_edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/device/(?P<device>[^/]+)/edit$', organizer.DeviceUpdateView.as_view(),
            name='organizer.device.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/device/(?P<device>[^/]+)/connect$', organizer.DeviceConnectView.as_view(),
            name='organizer.device.connect'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/device/(?P<device>[^/]+)/revoke$', organizer.DeviceRevokeView.as_view(),
            name='organizer.device.revoke'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/device/(?P<device>[^/]+)/logs$', organizer.DeviceLogView.as_view(),
            name='organizer.device.logs'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/gates$', organizer.GateListView.as_view(), name='organizer.gates'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/gate/add$', organizer.GateCreateView.as_view(), name='organizer.gate.add'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/gate/(?P<gate>[^/]+)/edit$', organizer.GateUpdateView.as_view(),
            name='organizer.gate.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/gate/(?P<gate>[^/]+)/delete$', organizer.GateDeleteView.as_view(),
            name='organizer.gate.delete'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/teams$', organizer.TeamListView.as_view(), name='organizer.teams'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/team/add$', organizer.TeamCreateView.as_view(), name='organizer.team.add'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/team/(?P<team>[^/]+)/$', organizer.TeamMemberView.as_view(),
            name='organizer.team'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/team/(?P<team>[^/]+)/edit$', organizer.TeamUpdateView.as_view(),
            name='organizer.team.edit'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/team/(?P<team>[^/]+)/delete$', organizer.TeamDeleteView.as_view(),
            name='organizer.team.delete'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/slugrng', main.SlugRNG.as_view(), name='events.add.slugrng'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/logs', organizer.LogView.as_view(), name='organizer.log'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/export/$', organizer.ExportView.as_view(), name='organizer.export'),
    re_path(r'^organizer/(?P<organizer>[^/]+)/export/do$', organizer.ExportDoView.as_view(), name='organizer.export.do'),
    re_path(r'^nav/typeahead/$', typeahead.nav_context_list, name='nav.typeahead'),
    re_path(r'^events/$', main.EventList.as_view(), name='events'),
    re_path(r'^events/add$', main.EventWizard.as_view(), name='events.add'),
    re_path(r'^events/typeahead/$', typeahead.event_list, name='events.typeahead'),
    re_path(r'^events/typeahead/meta/$', typeahead.meta_values, name='events.meta.typeahead'),
    re_path(r'^search/orders/$', search.OrderSearch.as_view(), name='search.orders'),
    re_path(r'^search/payments/$', search.PaymentSearch.as_view(), name='search.payments'),
    re_path(r'^event/(?P<organizer>[^/]+)/(?P<event>[^/]+)/', include([
        re_path(r'^$', dashboards.event_index, name='event.index'),
        re_path(r'^widgets.json$', dashboards.event_index_widgets_lazy, name='event.index.widgets'),
        re_path(r'^logs/embed$', dashboards.event_index_log_lazy, name='event.index.logs'),
        re_path(r'^live/$', event.EventLive.as_view(), name='event.live'),
        re_path(r'^logs/$', event.EventLog.as_view(), name='event.log'),
        re_path(r'^delete/$', event.EventDelete.as_view(), name='event.delete'),
        re_path(r'^comment/$', event.EventComment.as_view(),
                name='event.comment'),
        re_path(r'^quickstart/$', event.QuickSetupView.as_view(), name='event.quick'),
        re_path(r'^settings/$', event.EventUpdate.as_view(), name='event.settings'),
        re_path(r'^settings/plugins$', event.EventPlugins.as_view(), name='event.settings.plugins'),
        re_path(r'^settings/payment/(?P<provider>[^/]+)$', event.PaymentProviderSettings.as_view(),
                name='event.settings.payment.provider'),
        re_path(r'^settings/payment$', event.PaymentSettings.as_view(), name='event.settings.payment'),
        re_path(r'^settings/tickets$', event.TicketSettings.as_view(), name='event.settings.tickets'),
        re_path(r'^settings/tickets/preview/(?P<output>[^/]+)$', event.TicketSettingsPreview.as_view(),
                name='event.settings.tickets.preview'),
        re_path(r'^settings/email$', event.MailSettings.as_view(), name='event.settings.mail'),
        re_path(r'^settings/email/setup$', event.MailSettingsSetup.as_view(), name='event.settings.mail.setup'),
        re_path(r'^settings/email/preview$', event.MailSettingsPreview.as_view(), name='event.settings.mail.preview'),
        re_path(r'^settings/email/layoutpreview$', event.MailSettingsRendererPreview.as_view(),
                name='event.settings.mail.preview.layout'),
        re_path(r'^settings/cancel', event.CancelSettings.as_view(), name='event.settings.cancel'),
        re_path(r'^settings/invoice$', event.InvoiceSettings.as_view(), name='event.settings.invoice'),
        re_path(r'^settings/invoice/preview$', event.InvoicePreview.as_view(), name='event.settings.invoice.preview'),
        re_path(r'^settings/display', event.DisplaySettings.as_view(), name='event.settings.display'),
        re_path(r'^settings/tax/$', event.TaxList.as_view(), name='event.settings.tax'),
        re_path(r'^settings/tax/(?P<rule>\d+)/$', event.TaxUpdate.as_view(), name='event.settings.tax.edit'),
        re_path(r'^settings/tax/add$', event.TaxCreate.as_view(), name='event.settings.tax.add'),
        re_path(r'^settings/tax/(?P<rule>\d+)/delete$', event.TaxDelete.as_view(), name='event.settings.tax.delete'),
        re_path(r'^settings/widget$', event.WidgetSettings.as_view(), name='event.settings.widget'),
        re_path(r'^pdf/editor/webfonts.css', pdf.FontsCSSView.as_view(), name='pdf.css'),
        re_path(r'^pdf/editor/(?P<filename>[^/]+).pdf$', pdf.PdfView.as_view(), name='pdf.background'),
        re_path(r'^subevents/$', subevents.SubEventList.as_view(), name='event.subevents'),
        re_path(r'^subevents/select2$', typeahead.subevent_select2, name='event.subevents.select2'),
        re_path(r'^subevents/(?P<subevent>\d+)/$', subevents.SubEventUpdate.as_view(), name='event.subevent'),
        re_path(r'^subevents/(?P<subevent>\d+)/delete$', subevents.SubEventDelete.as_view(),
                name='event.subevent.delete'),
        re_path(r'^subevents/add$', subevents.SubEventCreate.as_view(), name='event.subevents.add'),
        re_path(r'^subevents/bulk_add$', subevents.SubEventBulkCreate.as_view(), name='event.subevents.bulk'),
        re_path(r'^subevents/bulk_action$', subevents.SubEventBulkAction.as_view(), name='event.subevents.bulkaction'),
        re_path(r'^subevents/bulk_edit$', subevents.SubEventBulkEdit.as_view(), name='event.subevents.bulkedit'),
        re_path(r'^items/$', item.ItemList.as_view(), name='event.items'),
        re_path(r'^items/add$', item.ItemCreate.as_view(), name='event.items.add'),
        re_path(r'^items/(?P<item>\d+)/$', item.ItemUpdateGeneral.as_view(), name='event.item'),
        re_path(r'^items/(?P<item>\d+)/up$', item.item_move_up, name='event.items.up'),
        re_path(r'^items/(?P<item>\d+)/down$', item.item_move_down, name='event.items.down'),
        re_path(r'^items/reorder$', item.reorder_items, name='event.items.reorder'),
        re_path(r'^items/(?P<item>\d+)/delete$', item.ItemDelete.as_view(), name='event.items.delete'),
        re_path(r'^items/typeahead/meta/$', typeahead.item_meta_values, name='event.items.meta.typeahead'),
        re_path(r'^items/select2$', typeahead.items_select2, name='event.items.select2'),
        re_path(r'^items/select2/variation$', typeahead.variations_select2, name='event.items.variations.select2'),
        re_path(r'^categories/$', item.CategoryList.as_view(), name='event.items.categories'),
        re_path(r'^categories/select2$', typeahead.category_select2, name='event.items.categories.select2'),
        re_path(r'^categories/(?P<category>\d+)/delete$', item.CategoryDelete.as_view(),
                name='event.items.categories.delete'),
        re_path(r'^categories/(?P<category>\d+)/up$', item.category_move_up, name='event.items.categories.up'),
        re_path(r'^categories/(?P<category>\d+)/down$', item.category_move_down,
                name='event.items.categories.down'),
        re_path(r'^categories/reorder$', item.reorder_categories, name='event.items.categories.reorder'),
        re_path(r'^categories/(?P<category>\d+)/$', item.CategoryUpdate.as_view(),
                name='event.items.categories.edit'),
        re_path(r'^categories/add$', item.CategoryCreate.as_view(), name='event.items.categories.add'),
        re_path(r'^questions/$', item.QuestionList.as_view(), name='event.items.questions'),
        re_path(r'^questions/reorder$', item.reorder_questions, name='event.items.questions.reorder'),
        re_path(r'^questions/(?P<question>\d+)/delete$', item.QuestionDelete.as_view(),
                name='event.items.questions.delete'),
        re_path(r'^questions/(?P<question>\d+)/$', item.QuestionView.as_view(),
                name='event.items.questions.show'),
        re_path(r'^questions/(?P<question>\d+)/change$', item.QuestionUpdate.as_view(),
                name='event.items.questions.edit'),
        re_path(r'^questions/add$', item.QuestionCreate.as_view(), name='event.items.questions.add'),
        re_path(r'^quotas/$', item.QuotaList.as_view(), name='event.items.quotas'),
        re_path(r'^quotas/(?P<quota>\d+)/$', item.QuotaView.as_view(), name='event.items.quotas.show'),
        re_path(r'^quotas/select$', typeahead.quotas_select2, name='event.items.quotas.select2'),
        re_path(r'^quotas/(?P<quota>\d+)/change$', item.QuotaUpdate.as_view(), name='event.items.quotas.edit'),
        re_path(r'^quotas/(?P<quota>\d+)/delete$', item.QuotaDelete.as_view(),
                name='event.items.quotas.delete'),
        re_path(r'^quotas/add$', item.QuotaCreate.as_view(), name='event.items.quotas.add'),
        re_path(r'^discounts/$', discounts.DiscountList.as_view(), name='event.items.discounts'),
        re_path(r'^discounts/(?P<discount>\d+)/delete$', discounts.DiscountDelete.as_view(),
                name='event.items.discounts.delete'),
        re_path(r'^discounts/(?P<discount>\d+)/up$', discounts.discount_move_up, name='event.items.discounts.up'),
        re_path(r'^discounts/(?P<discount>\d+)/down$', discounts.discount_move_down,
                name='event.items.discounts.down'),
        re_path(r'^discounts/reorder$', discounts.reorder_discounts, name='event.items.discounts.reorder'),
        re_path(r'^discounts/(?P<discount>\d+)/$', discounts.DiscountUpdate.as_view(),
                name='event.items.discounts.edit'),
        re_path(r'^discounts/add$', discounts.DiscountCreate.as_view(), name='event.items.discounts.add'),
        re_path(r'^vouchers/$', vouchers.VoucherList.as_view(), name='event.vouchers'),
        re_path(r'^vouchers/tags/$', vouchers.VoucherTags.as_view(), name='event.vouchers.tags'),
        re_path(r'^vouchers/rng$', vouchers.VoucherRNG.as_view(), name='event.vouchers.rng'),
        re_path(r'^vouchers/item_select$', typeahead.itemvarquota_select2, name='event.vouchers.itemselect2'),
        re_path(r'^vouchers/(?P<voucher>\d+)/$', vouchers.VoucherUpdate.as_view(), name='event.voucher'),
        re_path(r'^vouchers/(?P<voucher>\d+)/delete$', vouchers.VoucherDelete.as_view(),
                name='event.voucher.delete'),
        re_path(r'^vouchers/(?P<voucher>\d+)/deletecarts$', vouchers.VoucherDeleteCarts.as_view(),
                name='event.voucher.deletecarts'),
        re_path(r'^vouchers/add$', vouchers.VoucherCreate.as_view(), name='event.vouchers.add'),
        re_path(r'^vouchers/go$', vouchers.VoucherGo.as_view(), name='event.vouchers.go'),
        re_path(r'^vouchers/bulk_add$', vouchers.VoucherBulkCreate.as_view(), name='event.vouchers.bulk'),
        re_path(r'^vouchers/bulk_action$', vouchers.VoucherBulkAction.as_view(), name='event.vouchers.bulkaction'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/transition$', orders.OrderTransition.as_view(),
                name='event.order.transition'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/resend$', orders.OrderResendLink.as_view(),
                name='event.order.resendlink'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/(?P<position>\d+)/resend$', orders.OrderResendLink.as_view(),
                name='event.order.resendlink'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/invoice$', orders.OrderInvoiceCreate.as_view(),
                name='event.order.geninvoice'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/invoices/(?P<id>\d+)/regenerate$', orders.OrderInvoiceRegenerate.as_view(),
                name='event.order.regeninvoice'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/invoices/(?P<id>\d+)/reissue$', orders.OrderInvoiceReissue.as_view(),
                name='event.order.reissueinvoice'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/download/(?P<position>\d+)/(?P<output>[^/]+)/$',
                orders.OrderDownload.as_view(),
                name='event.order.download.ticket'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/answer/(?P<answer>[^/]+)/$',
                orders.AnswerDownload.as_view(),
                name='event.order.download.answer'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/checkvatid', orders.OrderCheckVATID.as_view(),
                name='event.order.checkvatid'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/extend$', orders.OrderExtend.as_view(),
                name='event.order.extend'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/reactivate$', orders.OrderReactivate.as_view(),
                name='event.order.reactivate'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/contact$', orders.OrderContactChange.as_view(),
                name='event.order.contact'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/locale', orders.OrderLocaleChange.as_view(),
                name='event.order.locale'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/comment$', orders.OrderComment.as_view(),
                name='event.order.comment'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/change$', orders.OrderChange.as_view(),
                name='event.order.change'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/approve', orders.OrderApprove.as_view(),
                name='event.order.approve'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/deny$', orders.OrderDeny.as_view(),
                name='event.order.deny'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/delete$', orders.OrderDelete.as_view(),
                name='event.order.delete'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/info', orders.OrderModifyInformation.as_view(),
                name='event.order.info'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/sendmail$', orders.OrderSendMail.as_view(),
                name='event.order.sendmail'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/(?P<position>[0-9A-Z]+)/sendmail$', orders.OrderPositionSendMail.as_view(),
                name='event.order.position.sendmail'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/mail_history$', orders.OrderEmailHistory.as_view(),
                name='event.order.mail_history'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/payments/(?P<payment>\d+)/cancel$', orders.OrderPaymentCancel.as_view(),
                name='event.order.payments.cancel'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/payments/(?P<payment>\d+)/confirm$', orders.OrderPaymentConfirm.as_view(),
                name='event.order.payments.confirm'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/refund$', orders.OrderRefundView.as_view(),
                name='event.order.refunds.start'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/refunds/(?P<refund>\d+)/cancel$', orders.OrderRefundCancel.as_view(),
                name='event.order.refunds.cancel'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/refunds/(?P<refund>\d+)/process$', orders.OrderRefundProcess.as_view(),
                name='event.order.refunds.process'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/refunds/(?P<refund>\d+)/done$', orders.OrderRefundDone.as_view(),
                name='event.order.refunds.done'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/cancellationrequests/(?P<req>\d+)/delete$',
                orders.OrderCancellationRequestDelete.as_view(),
                name='event.order.cancellationrequests.delete'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/transactions/$', orders.OrderTransactions.as_view(), name='event.order.transactions'),
        re_path(r'^orders/(?P<code>[0-9A-Z]+)/$', orders.OrderDetail.as_view(), name='event.order'),
        re_path(r'^invoice/(?P<invoice>[^/]+)$', orders.InvoiceDownload.as_view(),
                name='event.invoice.download'),
        re_path(r'^orders/overview/$', orders.OverView.as_view(), name='event.orders.overview'),
        re_path(r'^orders/import/$', orderimport.ImportView.as_view(), name='event.orders.import'),
        re_path(r'^orders/import/(?P<file>[^/]+)/$', orderimport.ProcessView.as_view(), name='event.orders.import.process'),
        re_path(r'^orders/export/$', orders.ExportView.as_view(), name='event.orders.export'),
        re_path(r'^orders/export/do$', orders.ExportDoView.as_view(), name='event.orders.export.do'),
        re_path(r'^orders/refunds/$', orders.RefundList.as_view(), name='event.orders.refunds'),
        re_path(r'^orders/go$', orders.OrderGo.as_view(), name='event.orders.go'),
        re_path(r'^orders/$', orders.OrderList.as_view(), name='event.orders'),
        re_path(r'^orders/search$', orders.OrderSearch.as_view(), name='event.orders.search'),
        re_path(r'^dangerzone/$', event.DangerZone.as_view(), name='event.dangerzone'),
        re_path(r'^cancel/$', orders.EventCancel.as_view(), name='event.cancel'),
        re_path(r'^shredder/$', shredder.StartShredView.as_view(), name='event.shredder.start'),
        re_path(r'^shredder/export$', shredder.ShredExportView.as_view(), name='event.shredder.export'),
        re_path(r'^shredder/download/(?P<file>[^/]+)/$', shredder.ShredDownloadView.as_view(), name='event.shredder.download'),
        re_path(r'^shredder/shred', shredder.ShredDoView.as_view(), name='event.shredder.shred'),
        re_path(r'^waitinglist/$', waitinglist.WaitingListView.as_view(), name='event.orders.waitinglist'),
        re_path(r'^waitinglist/action$', waitinglist.WaitingListActionView.as_view(), name='event.orders.waitinglist.action'),
        re_path(r'^waitinglist/auto_assign$', waitinglist.AutoAssign.as_view(), name='event.orders.waitinglist.auto'),
        re_path(r'^waitinglist/(?P<entry>\d+)/delete$', waitinglist.EntryDelete.as_view(),
                name='event.orders.waitinglist.delete'),
        re_path(r'^waitinglist/(?P<entry>\d+)/update$', waitinglist.EntryUpdate.as_view(),
                name='event.orders.waitinglist.update'),

        re_path(r'^checkins/$', checkin.CheckinListView.as_view(), name='event.orders.checkins'),
        re_path(r'^checkinlists/$', checkin.CheckinListList.as_view(), name='event.orders.checkinlists'),
        re_path(r'^checkinlists/add$', checkin.CheckinListCreate.as_view(), name='event.orders.checkinlists.add'),
        re_path(r'^checkinlists/select2$', typeahead.checkinlist_select2, name='event.orders.checkinlists.select2'),
        re_path(r'^checkinlists/(?P<list>\d+)/$', checkin.CheckInListShow.as_view(), name='event.orders.checkinlists.show'),
        re_path(r'^checkinlists/(?P<list>\d+)/bulk_action$', checkin.CheckInListBulkActionView.as_view(), name='event.orders.checkinlists.bulk_action'),
        re_path(r'^checkinlists/(?P<list>\d+)/change$', checkin.CheckinListUpdate.as_view(),
                name='event.orders.checkinlists.edit'),
        re_path(r'^checkinlists/(?P<list>\d+)/delete$', checkin.CheckinListDelete.as_view(),
                name='event.orders.checkinlists.delete'),
    ])),
    re_path(r'^event/(?P<organizer>[^/]+)/$', RedirectView.as_view(pattern_name='control:organizer'), name='event.organizerredirect'),
]
