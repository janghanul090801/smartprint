from django.utils.deprecation import MiddlewareMixin
from order.models import Goods
import json

class HeaderMiddleware(MiddlewareMixin):
    def getJsonList(self, category) :
        return json.dumps(list(Goods.objects.filter(category=category).values()))

    def process_response(self, request, response):
        response['namecardList'] = self.getJsonList('namecard')
        response['promotionList'] = self.getJsonList('promotion')
        response['stickerList'] = self.getJsonList('sticker')
        response['envelopeList'] = self.getJsonList('envelope')
        response['bookList'] = self.getJsonList('book')
        response['otherList'] = self.getJsonList('other')
        return response
    