from ninja import Router
from .schemas import LinkSchema
from .models import Links

shortener_router = Router()

@shortener_router.post('create/', response={200:LinkSchema, 409:dict})
def create(request, link_schema: LinkSchema):
    data = link_schema.to_model_data()
    redirect_link = data['redirect_link']
    token = data['token']
    expiration_time = data['expiration_time']
    max_uniques_clicks = data['max_uniques_clicks']

    if token and Links.objects.filter(token=token).exists():
        return 409, {'error':'Token already exists'}
    
    links = Links(**data)
    links.save()

    return 200, LinkSchema.from_model(links)