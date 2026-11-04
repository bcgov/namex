export default defineNuxtRouteMiddleware(async (to) => {

  // Check metadata to skip middleware
  if (to.meta.layout === 'empty') {
    console.log('Skipping middleware for routes with blank layout.');
    return;
  }
  
  // remove query params in url added by keycloak
  // from https://github.com/bcgov/business-transparency-registry/blob/3a8a8364c3279859e130f2c7aae4feee6b65c5a2/btr-web/btr-common-components/middleware/setupAuth.global.ts#L13
  if (to.query) {
    const params = new URLSearchParams(to.fullPath.split('?')[1])
    params.delete('state')
    params.delete('session_state')
    params.delete('code')
    params.delete('error')
    to.fullPath = to.path + (params.size > 0 ? `?${params}` : '') + to.hash
  }

  // Access the Keycloak instance
  const { $auth } = useNuxtApp(); 
  console.log('Auth object:', JSON.stringify($auth, null, 2));

  // Check if authentication data is available
  if (!$auth?.tokenParsed ) {
    console.error('Authentication object is not available. Redirecting to error page.');
    return navigateTo('/error');
  }
 
  // Check if the user is a staff member
  const userRoles = $auth.tokenParsed?.realm_access?.roles ??[];
  if (!['staff', 'names_viewer'].some(role => userRoles.includes(role))) {
    console.error('Access denied: You are not authorized to use this application.');
    return navigateTo('/error'); // Redirect to an error page or login page
  }
})
