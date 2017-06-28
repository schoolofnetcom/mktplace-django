from django import forms

from billing.models import Order


class PaymentForm(forms.Form):
    MONTH_CHOICES = (
        ('1', '1',),
        ('2', '2',),
        ('3', '3',),
        ('4', '4',),
        ('5', '5',),
        ('6', '6',),
        ('7', '7',),
        ('8', '8',),
        ('9', '9',),
        ('10', '10',),
        ('11', '11',),
        ('12', '12',),
    )

    YEAR_CHOICES = (
        ('2017', '2017',),
        ('2018', '2018',),
        ('2019', '2019',),
        ('2020', '2020',),
        ('2021', '2021',),
        ('2023', '2023',),
        ('2023', '2023',),
    )

    first_name = forms.CharField(label='Nome do titular',
                                 max_length=255,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'})
                                 )

    number = forms.CharField(label='Número do cartão',
                             max_length=255,
                             required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'})
                             )

    month = forms.ChoiceField(label='Vencimento',
                              required=True,
                              widget=forms.Select(attrs={'class': 'form-control'}),
                              choices=MONTH_CHOICES
                              )

    year = forms.ChoiceField(label='Ano',
                             required=True,
                             widget=forms.Select(attrs={'class': 'form-control'}),
                             choices=YEAR_CHOICES
                             )

    verification_value = forms.CharField(label='Cód.Segurança',
                                         max_length=3,
                                         required=True,
                                         widget=forms.TextInput(attrs={'class': 'form-control'})
                                         )


class EditOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ('user', 'merchant', 'commission', 'product', 'total', 'status', 'created_at')

        widgets = {
            'shipment_status': forms.Select(attrs={'class': 'form-control', 'onchange': 'this.form.submit();'}),
        }

        labels = {
            'order_status': "Status do produto",
        }
