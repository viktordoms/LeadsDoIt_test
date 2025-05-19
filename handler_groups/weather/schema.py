from datetime import datetime

from marshmallow import fields as f, post_load

from libs.schemas import BasicSchema, BasicSuccessSchema

class WeatherSearchSchema(BasicSchema):
    day = f.Date(
        required=True,
        allow_none=False,
        format="%Y-%m-%d",
        example='2025-05-19'
    )

    @post_load
    def _prepare_timestamps(self, data, **kwargs):
        day = data['day']
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day, datetime.max.time())
        return {
            "time_from": start,
            "time_to": end,
        }

class WeatherSchema(BasicSchema):
    id = f.Integer()
    city = f.String()
    created_at = f.DateTime(format="%Y-%m-%d %H:%M:%S")
    temperature = f.Float()


class WeatherSearchResultSchema(BasicSuccessSchema):
    results = f.Nested(WeatherSchema, many=True)
