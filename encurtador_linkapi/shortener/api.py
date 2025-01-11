from ninja import Router
from .schemas import LinkSchema
from .models import Links, Clicks
from django.shortcuts import get_object_or_404, redirect

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

@shortener_router.get('/{token}', response={404: dict})
def redirect_link(request, token):
    link = get_object_or_404(Links, token=token, active=True)

    if link.expired():
        return 404, {'error':'link expired'}
    
    unique_clicks = Clicks.objects.filter(link=link).values('ip').distinct().count()

    if link.max_uniques_clicks and unique_clicks >= link.max_uniques_clicks:
        return 404, {'error':'link expired'}

    click = Clicks(
        link=link,
        ip=request.META.get('REMOTE_ADDR')
    )
    click.save()
    
    return redirect(link.redirect_link)
