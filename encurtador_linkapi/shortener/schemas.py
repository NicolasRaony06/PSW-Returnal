from ninja import Schema, ModelSchema
from .models import Links
from datetime import timedelta

class LinkSchema(ModelSchema):
    expiration_time: int

    class Meta:
        model = Links
        fields = ['redirect_link','token','expiration_time','max_uniques_clicks']

    def to_model_data(self):
        return {
            'redirect_link': self.redirect_link,
            'token': self.token,
            'expiration_time': timedelta(minutes=self.expiration_time),
            'max_uniques_clicks': self.max_uniques_clicks
        }
    
    @classmethod
    def from_model(cls, instance: Links):
        return cls(
            redirect_link=instance.redirect_link,
            token=instance.token,
            expiration_time=int(instance.expiration_time.total_seconds() // 60),
            max_uniques_clicks=instance.max_uniques_clicks
        )