import json

from rest_framework.renderers import JSONRenderer


class LikeComementsJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, media_type=None, renderer_context=None):

        if 'errors' in data or 'detail' in data or 'message' in data:
            return super().render(data)

        return json.dumps({
            'likes': data,
            "likes count": len(data)
        })
