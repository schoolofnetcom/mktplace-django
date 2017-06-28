import math
from django.conf import settings
from iugu import Transfer

from billing.models import Order
from portal.models import UserProfile
from iugu.customer import Customer
from iugu.token import Token


class BillingService(object):
    def create_remote_customer(self, user):

        try:
            profile = user.userprofile
        except:
            profile = UserProfile()
            profile.user = user
            profile.save()

        if not profile.remote_customer_id:
            data = {
                'email': user.email
            }

            customer = Customer()
            res = customer.create(data)

            if res['id']:
                user.userprofile.remote_customer_id = res['id']
                user.userprofile.save()

        if user.userprofile.remote_customer_id:
            return user

        return False

    def transfer(self, order):
        percent_commission = settings.IUGU_COMMISSION_MARKET_PLACE

        total = math.ceil(float(order.total) * float(percent_commission)) * 100

        data_commission = {
            'receiver_id': order.user.remote_receiver_id,
            'amount_cents': total
        }

        transfer = Transfer().create(data_commission)
        return transfer

    def charge(self, user, product, payment_data):

        remote_customer = self.create_remote_customer(user)

        data_token = {
            'account_id': settings.IUGU_ACCOUNT_ID,
            'method': 'credit_card',
            'data': payment_data['data']
        }

        token = Token().create(data_token)

        if 'errors' in token:
            return False

        data = {
            'items': {
                'description': product.name,
                'quantity': 1,
                'price_cents': str(product.price).replace(".", "")
            },
            'token': token['id'],
            'email': user.email,
            'customer_id': user.userprofile.remote_customer_id
        }

        charge = Token().charge(data)

        if 'success' in charge:
            order = Order()
            order.user = user
            order.merchant = product.user
            order.product = product
            order.status = "Approved"
            order.total = product.price
            order.save()

            if not settings.DEBUG:
                transfer_commission = self.transfer(order)
                order.commission = transfer_commission['amount_localized']
                order.save()

            return order

        return False
