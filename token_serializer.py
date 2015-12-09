from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from SharedModels import token_secretKey

class TokenSerializer:
    @staticmethod
    def generate_auth_token(user_id, expiration = 600):
        tokenSerializer = Serializer(token_secretKey, expires_in = expiration)

        return tokenSerializer.dumps({ 'id': user_id })

    @staticmethod
    def verify_auth_token(token, user_id):
        tokenSerializer = Serializer(token_secretKey)
        try:
            data = tokenSerializer.loads(token)
        except SignatureExpired:
            return False # valid token, but expired
        except BadSignature:
            return False # invalid token

        token_user_id = data['id']
        return token_user_id == user_id
