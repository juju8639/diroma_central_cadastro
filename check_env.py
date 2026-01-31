import os
print('EMAIL_SENDER=', os.getenv('EMAIL_SENDER'))
print('EMAIL_PASSWORD set=', bool(os.getenv('EMAIL_PASSWORD')))
print('EMAIL_SMTP=', os.getenv('EMAIL_SMTP', 'smtp.gmail.com'))
print('EMAIL_PORT=', os.getenv('EMAIL_PORT', '587'))
