from django.contrib import admin

from swe0.ledger import models


admin.site.register(models.Transaction)
