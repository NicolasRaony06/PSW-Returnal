from ninja import Router
from .schemas import LinkSchema, UpdateLinkSchema
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

@shortener_router.put('/{link_id}/', response={200: UpdateLinkSchema, 409: dict})
def update_link(request, link_id: int, link_schema: UpdateLinkSchema):
    link = get_object_or_404(Links, id=link_id)

    data = link_schema.dict()

    token = data['token']
    if token and Links.objects.filter(token=token).exclude(id=link_id).exists():
        return 409, {'error':'Token already exists'}
    
    for field, value in data.items():
        if value:
            setattr(link, field, value)

    link.save()

    return 200, link

@shortener_router.get('statistics/{link_id}/', response={200: dict})
def statistics(request, link_id: int):
    link = get_object_or_404(Links, id=link_id)

    uniques_clicks = Clicks.objects.filter(link=link).values('ip').distinct().count()
    total_clicks = Clicks.objects.filter(link=link).values('ip').count()

    return 200, {'uniques_clicks': uniques_clicks, 'total_clicks': total_clicks}
