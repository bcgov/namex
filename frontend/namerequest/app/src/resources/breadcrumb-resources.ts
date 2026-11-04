import { BreadcrumbIF } from '@/interfaces'

/** Returns URL param string with Account ID if present, else empty string. */
function getParams (): string {
  const accountId = JSON.parse(sessionStorage.getItem('CURRENT_ACCOUNT'))?.id
  return accountId ? `?accountid=${accountId}` : ''
}

export function getRegistryDashboardBreadcrumb (): BreadcrumbIF {
  const registryHomeUrl = sessionStorage.getItem('REGISTRY_HOME_URL')
  return {
    text: 'BC Registries and Online Services',
    href: `${registryHomeUrl}`
  }
}

export function getRegistryHomeBreadcrumb (): BreadcrumbIF {
  const registryHomeUrl = sessionStorage.getItem('REGISTRY_HOME_URL')
  return {
    text: 'BC Registries Dashboard',
    href: `${registryHomeUrl}dashboard/${getParams()}`
  }
}

export function getStaffDashboardBreadcrumb (): BreadcrumbIF {
  const businessUrl = sessionStorage.getItem('AUTH_WEB_URL')
  return {
    text: 'Staff Dashboard',
    href: `${businessUrl}staff/dashboard/active${getParams()}`
  }
}
