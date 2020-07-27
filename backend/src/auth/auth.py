import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
# Used to test json
import pprint
pp = pprint.PrettyPrinter(indent=4)

from secure import AUTH0_DOMAIN, ALGORITHM, API_AUDIENCE


ALGORITHMS = [ALGORITHM]

## AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    # extra TODO return json
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


## Auth Header

'''
it should attempt to get the header from the request
    it should raise an AuthError if no header is present
it should attempt to split bearer and the token
    it should raise an AuthError if the header is malformed
return the token part of the header
'''
def get_token_auth_header():
    # if no header is sent, raise a 401
    if 'Authorization' not in request.headers:
        raise AuthError(
            error='Unauthorized',
            status_code='401'
        )
    # Get auth header
    auth_header = request.headers.get('Authorization')
    if len(auth_header.split(' ')) != 2:
        raise AuthError(
            error='Unauthorized',
            status_code='401'
        )
    # If the first part of the token is not bearer, raise a 401
    if auth_header.split(' ')[0] != 'Bearer':
        raise AuthError(
            error='Unauthorized',
            status_code='401'
        )
    token = auth_header.split(" ")[1]
    return token

'''
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is not in the payload permissions array
    return true otherwise
'''
def check_permissions(permission, payload):
    #if no permissions are included in our payload, abort as a 400
    if 'permissions' not in payload:
        raise AuthError(
            error='Bad Request',
            status_code='401'
        )

    # if the permission that we require is not in the payload, we'll abort with a 403
    if permission not in payload['permissions']:
        raise AuthError(
            error='Forbidden',
            status_code='403'
        )
    return True
'''
@INPUTS
    token: a json web token (string)

it should be an Auth0 token with key id (kid)
it should verify the token using Auth0 /.well-known/jwks.json
it should decode the payload from the token
it should validate the claims
return the decoded payload

!!NOTE urlopen has a common certificate error described here: https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''
def verify_decode_jwt(token):
    print(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    
    jwks = json.loads(jsonurl.read())
    # pp.pprint(jwks)
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

'''
@INPUTS
    permission: string permission (i.e. 'post:drink')

it should use the get_token_auth_header method to get the token
it should use the verify_decode_jwt method to decode the jwt
it should use the check_permissions method validate claims and check the requested permission
return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator