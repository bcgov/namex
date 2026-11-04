def setup_test_token(jwt, claims, token_header):
    # Create JWT & setup header with a Bearer Token using the JWT
    token = jwt.create_jwt(claims, token_header)
    return token, {'Authorization': 'Bearer ' + token, 'content-type': 'application/json'}
