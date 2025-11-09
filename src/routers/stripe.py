from fastapi import APIRouter, Depends, Request, Header

from ..database_service import DatabaseService
from ..stripe_service import StripeService
from ..dependencies import CurrentActiveUser, get_database_service, get_stripe_service

import logging

logger = logging.getLogger('uvicorn.error')

"""Create user management router with dependency injection"""
router = APIRouter()

@router.post("/stripe-webhook", tags=["stripe"])
async def stripe_webhook_received(
    request: Request,
    stripe_signature=Header(None),
    db_service: DatabaseService = Depends(get_database_service),
    stripe_service: StripeService = Depends(get_stripe_service),
):
    return await stripe_service.handle_webhook_event(
        request=request,
        db_service=db_service,
        stripe_signature=stripe_signature,
        )


@router.post("/create-customer-portal-session", tags=["stripe"])
async def create_customer_portal_session(
    request: Request,
    current_user: CurrentActiveUser,
    stripe_service: StripeService = Depends(get_stripe_service),
):
    locale = request.headers.get('Accept-Language', 'auto')
    return await stripe_service.create_customer_portal_session(
        customer_id=current_user.stripe_customer_id,
        locale=locale
    )