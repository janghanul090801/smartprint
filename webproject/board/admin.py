from django.contrib import admin
from .models import Posts, QuoteInquiry, Attachment, FAQ


admin.site.register(Posts)
admin.site.register(QuoteInquiry)
admin.site.register(Attachment)
admin.site.register(FAQ)