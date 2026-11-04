import Vue from 'vue'
import Vuetify from 'vuetify'
import VueRouter from 'vue-router'
import { shallowMount, createLocalVue } from '@vue/test-utils'
import App from '@/App.vue'
import {
  AffiliationErrorDialog, CancelDialog, ConditionsDialog, ErrorDialog, ExitDialog, HelpMeChooseDialog,
  MrasSearchInfoDialog, NrNotRequiredDialog, ConfirmNrDialog, PaymentCompleteDialog,
  PickEntityOrConversionDialog, RenewDialog, ReceiptsDialog, RefundDialog, ResubmitDialog,
  RetryDialog, StaffPaymentErrorDialog, UpgradeDialog, ExitIncompletePaymentDialog
} from '@/components/dialogs'
import SbcHeader from 'sbc-common-components/src/components/SbcHeader.vue'
import SbcFooter from 'sbc-common-components/src/components/SbcFooter.vue'
// import mockRouter from './MockRouter'

const vuetify = new Vuetify()

const KEYCLOAK_TOKEN = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJUbWdtZUk0MnVsdUZ0N3' +
  'FQbmUtcTEzdDUwa0JDbjF3bHF6dHN0UGdUM1dFIn0.eyJqdGkiOiIzZDQ3YjgwYy01MTAzLTRjMTYtOGNhZC0yMjU4NDMwZGYwZTciLCJle' +
  'HAiOjE1Njg0ODk1NTksIm5iZiI6MCwiaWF0IjoxNTY4NDAzMTYwLCJpc3MiOiJodHRwczovL3Nzby1kZXYucGF0aGZpbmRlci5nb3YuYmMuY2' +
  'EvYXV0aC9yZWFsbXMvZmNmMGtwcXIiLCJhdWQiOlsic2JjLWF1dGgtd2ViIiwicmVhbG0tbWFuYWdlbWVudCIsImJyb2tlciIsImFjY291bnQ' +
  'iXSwic3ViIjoiZDRjNTBiZTAtYWM2OC00MDIyLTkxMGQtMzE2NzQ4NGFkOWU0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoic2JjLWF1dGgtd2Vi' +
  'Iiwibm9uY2UiOiJkMjljZTZlNS0xNzZhLTRkMTUtODUzZS05NWUzZmUwZmYwZjgiLCJhdXRoX3RpbWUiOjE1Njg0MDMxNTksInNlc3Npb25fc' +
  '3RhdGUiOiJiOTEwMzQxZi0xNzVjLTRkMTktYWI1Yy1iM2QxNTBiYjk0NjYiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbImh0dHA6Ly' +
  '8xOTIuMTY4LjAuMTM6ODA4MC8iLCIxOTIuMTY4LjAuMTMiLCIqIiwiaHR0cDovLzE5Mi4xNjguMC4xMzo4MDgwIl0sInJlYWxtX2FjY2VzcyI' +
  '6eyJyb2xlcyI6WyJ2aWV3IiwiZWRpdCIsIm9mZmxpbmVfYWNjZXNzIiwic3RhZmYiLCJ1bWFfYXV0aG9yaXphdGlvbiIsImJhc2ljIl19LCJy' +
  'ZXNvdXJjZV9hY2Nlc3MiOnsicmVhbG0tbWFuYWdlbWVudCI6eyJyb2xlcyI6WyJ2aWV3LWlkZW50aXR5LXByb3ZpZGVycyIsInZpZXctcmVhb' +
  'G0iLCJtYW5hZ2UtaWRlbnRpdHktcHJvdmlkZXJzIiwiaW1wZXJzb25hdGlvbiIsInJlYWxtLWFkbWluIiwiY3JlYXRlLWNsaWVudCIsIm1hbm' +
  'FnZS11c2VycyIsInF1ZXJ5LXJlYWxtcyIsInZpZXctYXV0aG9yaXphdGlvbiIsInF1ZXJ5LWNsaWVudHMiLCJxdWVyeS11c2VycyIsIm1hbmF' +
  'nZS1ldmVudHMiLCJtYW5hZ2UtcmVhbG0iLCJ2aWV3LWV2ZW50cyIsInZpZXctdXNlcnMiLCJ2aWV3LWNsaWVudHMiLCJtYW5hZ2UtYXV0aG9y' +
  'aXphdGlvbiIsIm1hbmFnZS1jbGllbnRzIiwicXVlcnktZ3JvdXBzIl19LCJicm9rZXIiOnsicm9sZXMiOlsicmVhZC10b2tlbiJdfSwiYWNjb' +
  '3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwic2NvcGUiOi' +
  'JvcGVuaWQiLCJmaXJzdG5hbWUiOiJTdW1lc2giLCJyb2xlcyI6WyJ2aWV3IiwiZWRpdCIsIm9mZmxpbmVfYWNjZXNzIiwic3RhZmYiLCJ1bWF' +
  'fYXV0aG9yaXphdGlvbiIsImJhc2ljIl0sIm5hbWUiOiJTdW1lc2ggS2FyaXlpbCIsInByZWZlcnJlZF91c2VybmFtZSI6InNrYXJpeWlsQGlk' +
  'aXIiLCJlbWFpbCI6InN1bWVzaC5wLmthcml5aWxAZ292LmJjLmNhIiwibGFzdG5hbWUiOiJLYXJpeWlsIiwidXNlcm5hbWUiOiJza2FyaXlpb' +
  'EBpZGlyIn0.MSPSakOnCUia4qd-fUpvP2PB3k977Eyhjxn-ykjadsUTEK4f2R3c8vozxaIIMH0-qUwduyQmdZCl3tQnXYQ9Ttf1PE9eMLS4sX' +
  'JiIUlDmKZ2ow7GmmDabic8igHnEDYD6sI7OFYnCJhRdgVEHN-_4KUk2YsAVl5XUr6blJKMuYDPeMyNreGTXU7foE4AT-93FwlyTyFzQGddrDv' +
  'c6kkQr7mgJNTtgg87DdYbVGbEtIetyVfvwEF0rU8JH2N-j36XIebo33FU3-gJ5Y5S69EHPqQ37R9H4d8WUrHO-4QzJQih3Yaea820XBplJeo0' +
  'DO3hQoVtPD42j0p3aIy10cnW2g'

describe('App component', () => {
  let wrapper: any

  beforeEach(async () => {
    sessionStorage.clear()
    sessionStorage.setItem('KEYCLOAK_TOKEN', KEYCLOAK_TOKEN)
    sessionStorage.setItem('CURRENT_ACCOUNT', '{ "id": 668 }')

    // create a Local Vue and install router on it
    const localVue = createLocalVue()
    localVue.use(VueRouter)
    wrapper = shallowMount(App, { localVue, vuetify, stubs: { Affix: true } })
    await Vue.nextTick()
  })

  afterEach(() => {
    wrapper.destroy()
  })

  it('renders dialogs properly', () => {
    expect(wrapper.findComponent(AffiliationErrorDialog).exists()).toBe(true)
    expect(wrapper.findComponent(CancelDialog).exists()).toBe(true)
    expect(wrapper.findComponent(ConditionsDialog).exists()).toBe(true)
    expect(wrapper.findComponent(ConfirmNrDialog).exists()).toBe(true)
    expect(wrapper.findComponent(ErrorDialog).exists()).toBe(true)
    expect(wrapper.findComponent(ExitDialog).exists()).toBe(true)
    expect(wrapper.findComponent(ExitIncompletePaymentDialog).exists()).toBe(true)
    expect(wrapper.findComponent(HelpMeChooseDialog).exists()).toBe(true)
    expect(wrapper.findComponent(MrasSearchInfoDialog).exists()).toBe(true)
    expect(wrapper.findComponent(NrNotRequiredDialog).exists()).toBe(true)
    expect(wrapper.findComponent(PaymentCompleteDialog).exists()).toBe(true)
    expect(wrapper.findComponent(PickEntityOrConversionDialog).exists()).toBe(true)
    expect(wrapper.findComponent(RenewDialog).exists()).toBe(true)
    expect(wrapper.findComponent(ReceiptsDialog).exists()).toBe(true)
    expect(wrapper.findComponent(RefundDialog).exists()).toBe(true)
    expect(wrapper.findComponent(ResubmitDialog).exists()).toBe(true)
    expect(wrapper.findComponent(RetryDialog).exists()).toBe(true)
    expect(wrapper.findComponent(StaffPaymentErrorDialog).exists()).toBe(true)
    expect(wrapper.findComponent(UpgradeDialog).exists()).toBe(true)
  })

  it('renders the sub-components properly', () => {
    expect(wrapper.findComponent(SbcHeader).exists()).toBe(true)
    expect(wrapper.findComponent(SbcHeader).exists()).toBe(true)
    expect(wrapper.findComponent(SbcFooter).exists()).toBe(true)
  })

  it('initializes the local properties properly', () => {
    const vm: any = wrapper.vm
    expect(vm.staffPaymentErrorDialog).toBe(false)
    expect(vm.saveErrors).toEqual([])
    expect(vm.saveWarnings).toEqual([])
  })

  it('redirects to dashboard if exiting after saving changes', () => {
    // verify sessionStorage items
    expect(sessionStorage.getItem('KEYCLOAK_TOKEN')).toBe(KEYCLOAK_TOKEN)
    expect(JSON.parse(sessionStorage.getItem('CURRENT_ACCOUNT')).id).toBe(668)
  })
})
