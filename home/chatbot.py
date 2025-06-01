import random
from django.core.mail import send_mail

responses = {
    # Greetings & General
    "hello": ["Hi! How can I assist you today?", "Hello! How may I help you?"],
    "hi": ["Hey there! How can I help?", "Hi! What do you need assistance with?"],
    "how are you": ["I'm just a bot, but I'm here to help!", "I'm good! How can I assist you?"],
    
    # Pricing & Payment
    "pricing": ["Our pricing details are available at /pricing.", "Check out our pricing plans at /plans."],
    "payment methods": ["We accept credit/debit cards, PayPal, and bank transfers."],
    "refund policy": ["Refunds are processed within 5-7 business days. More details at /refund-policy."],
    "discounts": ["We offer seasonal discounts! Check our website for ongoing offers."],

    # Account Issues
    "create account": ["You can sign up at /signup. Let me know if you need help!"],
    "forgot password": ["Reset your password here: /reset-password"],
    "delete account": ["To delete your account, visit /delete-account or contact support."],
    "change email": ["You can update your email in your profile settings at /settings."],

    # Product & Services
    "features": ["Our platform offers chatbots, analytics, support automation, and more!"],
    "subscription": ["You can subscribe to our services at /subscription."],
    "trial": ["We offer a free 7-day trial! Sign up at /free-trial."],
    "upgrade": ["Upgrade your plan at /upgrade."],

    # Technical Support
    "not working": ["I'm sorry to hear that. Can you describe the issue in detail?"],
    "bug report": ["You can report bugs at /bug-report."],
    "slow performance": ["Try clearing cache and cookies. If the issue persists, contact support."],
    
    # Contact & Support
    "contact": ["You can reach us at support@yourwebsite.com.", "Call our support team at +1234567890."],
    "support": ["Our support team is available 24/7 at /support."],
    "live chat": ["You can chat with an agent at /livechat."],

    # Order & Delivery
    "track order": ["Track your order here: /track-order."],
    "delivery status": ["You can check your delivery details at /delivery-status."],
    "cancel order": ["To cancel your order, visit /cancel-order within 24 hours of purchase."],

    # Miscellaneous
    "faq": ["Find answers to common questions at /faq."],
    "terms and conditions": ["Our terms of service are available at /terms."],
    "privacy policy": ["You can read our privacy policy at /privacy-policy."],
    
    # Default Response
    "default": ["I'm not sure about that. Let me connect you to an admin."]
                
}






def get_response(user_input):
    user_input = user_input.lower()
    for key in responses.keys():
        if key in user_input:
            return random.choice(responses[key])
   
    # If no response is found, escalate to admin
    send_email_to_admin(user_input)
    return random.choice(responses["default"]) 

def send_email_to_admin(query):
    

    send_mail(
        "User Query Escalation",
        f"A user needs help with the following query:\n\n{query}",
        "support@yourwebsite.com",
        ["admin@yourwebsite.com"]
    )
