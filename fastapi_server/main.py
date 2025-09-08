from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import uvicorn
import asyncio
import logging
import json

from fastapi_server.models import ChatRequest, Planner, Reflector, NotifiWriter, EmailWriter, SendEmail, SendNotification
from fastapi_server.log import logger
from AgentManager.MarketingAgent import prompts, plnr, rflctr, ntfy, eml
from AgentManager.ActionAgent.Email import email_client
from AgentManager.ActionAgent.Telegram import telegram_client
from fastapi.middleware.cors import CORSMiddleware  # <-- Add this import

app = FastAPI()
# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can specify allowed origins here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# metrics
app.state.sentEmail = 0
app.state.sentNotification = 0
app.state.uniqueMailReceiver = 0
app.state.uniqueNotificationReceiver =0
app.state.mailFrequency = 0
app.state.notificationFrequency = 0

app.state.mailReceivers = []
app.state.notificationReceivers = []

@app.get("/")
def read_root():
    return {"message": "Code Catalyst Gen-AI Backend"}

@app.post("/api/plan")
def create_sales_plan(request: Planner):
    target_audience = request.target_audience
    logging.info(f"Received request for creating sales plan")
    
    try:
        response = plnr.get_planner_result(target_audience)
        return {
                "status": "success",
                "response": response
        }
    except Exception as e:
        logging.error(f"Error: {e}")
        return {
                "status": "fail",
                "response": None
        }

@app.post("/api/reflect")
def reflect_sales_plan(request: Reflector):
    suggestion=request.suggestions,
    previous_strategy=request.previous_strategy
    logging.info(f"Received request for reflecting sales plan")
    
    try:
        response = rflctr.get_reflector_result(suggestion, previous_strategy)
        return {
                "status": "success",
                "response": response
        }
    except Exception as e:
        logging.error(f"Error: {e}")
        return {
                "status": "fail",
                "response": None
        }

@app.post("/api/write/email")
def write_emails(request: EmailWriter):
    product_to_market = request.product_to_market
    customer_info = request.customer_info
    guidelines = request.guidelines

    logging.info(f"Received request for writing an email")
    try:
        response = eml.get_email_writer_result(product_to_market, customer_info, guidelines)
        return {
                "status": "success",
                "response": response
        }
    except Exception as e:
        logging.error(f"Error: {e}")
        return {
                "status": "fail",
                "response": None
        }

@app.post("/api/write/notification")
def write_emails(request: NotifiWriter):
    product_to_market = request.product_to_market
    customer_info = request.customer_info
    guidelines = request.guidelines

    logging.info(f"Received request for writing an email")
    try:
        response = ntfy.get_notifi_writer_result(product_to_market, customer_info, guidelines)
        return {
                "status": "success",
                "response": response
        }
    except Exception as e:
        logging.error(f"Error: {e}")
        return {
                "status": "fail",
                "response": None
        }

@app.post("/api/send/email")
def write_emails(request: SendEmail):
    receiver = request.receiver
    subject = request.subject
    email_body = request.body

    if receiver in app.state.mailReceivers:
        app.state.sentEmail += 1
    else:
        app.state.uniqueMailReceiver += 1
        app.state.mailReceivers.append(receiver)
        app.state.sentEmail += 1

    logger.info(f"Received request for sending an email")
    try:
        response = email_client.send_email_msg(receiver=receiver, subject=subject, email_body=email_body)
        logger.info(f"Processing request for sending an email")
        return {
                "status": "success",
                "response": response
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
                "status": "fail",
                "response": None
        }

@app.post("/api/send/notification")
async def send_notifications(request: SendNotification):
    receiver = request.receiver
    message = request.message
    
    if receiver in app.state.notificationReceivers:
        app.state.sentNotification += 1
    else:
        app.state.uniqueNotificationReceiver += 1
        app.state.notificationReceivers.append(receiver)
        app.state.sentNotification += 1

    logger.info(f"Received request for sending Notification")
    try:
        response = await telegram_client.send_telegram_message(receiver=receiver, message=message)
        logger.info(f"Processing request for sending Notification")
        return {
                "status": "success",
                "response": response
        }
    except Exception as e:
        logger.error(f"Error: {e}")
        return {
                "status": "fail",
                "response": None
        }

@app.get("/get_metrics")
def get_metrics():
    data = {
        "mail_sent": app.state.sentEmail,
        "unique_mail_receivers": app.state.uniqueMailReceiver,
        "mail_frequency": (
    app.state.sentEmail / app.state.uniqueMailReceiver
    if app.state.uniqueMailReceiver > 0 else 0
)
        ,
        "notification_sent": app.state.sentNotification,
        "unique_notification_receiver": app.state.uniqueNotificationReceiver,
        "notification_frequency": (
    app.state.sentNotification / app.state.uniqueNotificationReceiver
    if app.state.uniqueNotificationReceiver > 0 else 0
)
    }
    return data



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)