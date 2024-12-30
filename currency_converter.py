import currencyapicom


class CurrencyConverter:
    def __init__(self, api_key):
        self.client = currencyapicom.Client(api_key)

    def convert(self, amount, base_currency):
        try:
            result = self.client.latest(base_currency=base_currency)
            if 'data' in result:
                if base_currency in result['data']:
                    target_currencies = {
                        'UAH': '🇺🇦',
                        'EUR': '🇪🇺',
                        'CZK': '🇨🇿',
                        'USD': '🇺🇸'
                    }
                    conversion_result = []

                    for currency, emoji in target_currencies.items():
                        if currency != base_currency and currency in result['data']:
                            rate = result['data'][currency]['value']
                            converted_amount = rate * float(amount)
                            conversion_result.append(f'{emoji}{round(converted_amount, 2)} {currency}')

                    if conversion_result:
                        return '\n'.join(conversion_result)
                    else:
                        return "No valid target currencies found."
                else:
                    return f"Invalid currency code: {base_currency}"
            return "Conversion failed. Please check the currency code."
        except Exception as e:
            return f"An Error occured: {e}"
