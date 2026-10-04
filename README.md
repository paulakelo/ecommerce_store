# ecommerce_store

## M-Pesa setup

Install the project dependencies with `python -m pip install -r requirements.txt`.

The checkout uses Daraja STK Push in sandbox mode by default. Django loads the project-root `.env` file; set `MPESA_CONSUMER_KEY`, `MPESA_CONSUMER_SECRET`, `MPESA_PASSKEY`, and `BUSINESS_SHORTCODE` there. `MPESA_SHORTCODE` is also accepted as an alias. An optional `MPESA_CALLBACK_URL` overrides the callback URL, which otherwise is built from the checkout host at `/payments/mpesa/callback/`. Daraja must be able to reach that URL over HTTPS, so local development needs an HTTPS tunnel and production needs a publicly reachable HTTPS domain.

Run `python manage.py migrate` after updating the order model. The callback marks an order paid only when its checkout request ID, amount, phone number, and receipt match the stored order. Never expose Daraja credentials in source control.

## Languages

The English and Kiswahili selector uses Django's language cookie and the translation catalog in `locale/sw/LC_MESSAGES/django.po`. After changing translations, run `python manage.py compilemessages` (GNU gettext is required).

## Checks

Run the focused application tests with `python manage.py test`.