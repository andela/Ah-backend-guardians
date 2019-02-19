import json

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


class LikeComementsJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        if 'errors' in data or 'detail' in data or 'message' in data:
            return super().render(data)

        return json.dumps({
            'likes': data,
            "likes count": len(data)
        })


class CommentJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        if type(data) != ReturnList:
            errors = data.get('errors', None)
            if errors is not None:
                return super(CommentJSONRenderer, self).render(data)
        return json.dumps({'comment': data})
