# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # from openai import OpenAI
# # import os
# # import openai
# # from datetime import datetime
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # from dotenv import load_dotenv
# # load_dotenv()

# # app = Flask(__name__)
# # CORS(app)


# # openai.api_key = os.getenv('OPENAI_API_KEY')


# # PRODUCTS = [
# #     {
# #         'id': 1,
# #         'name': 'Smart Washing Machine',
# #         'price': '$599',
# #         'manual': 'Load capacity: 8kg. Use cold water for delicate fabrics. Run cleaning cycle monthly. Check filter every 3 months.',
# #         'keywords': ['washing', 'machine', 'washer', 'laundry'],
# #         'features': ['8kg capacity', 'Energy efficient', 'Smart connectivity', '15 wash programs']
# #     },
# #     {
# #         'id': 2,
# #         'name': 'Air Conditioner',
# #         'price': '$899',
# #         'manual': 'Set temperature between 22-26°C for optimal efficiency. Clean filters every 2 weeks. Schedule annual maintenance.',
# #         'keywords': ['air', 'conditioner', 'ac', 'cooling', 'aircon'],
# #         'features': ['1.5 ton capacity', 'Inverter technology', 'PM 2.5 filter', 'Voice control']
# #     },
# #     {
# #         'id': 3,
# #         'name': 'Microwave Oven',
# #         'price': '$299',
# #         'manual': 'Max power: 1000W. Use microwave-safe containers only. Clean interior after each use. Defrost function available.',
# #         'keywords': ['microwave', 'oven', 'heating'],
# #         'features': ['1000W power', '30L capacity', 'Auto-cook menus', 'Child safety lock']
# #     },
# #     {
# #         'id': 4,
# #         'name': 'Smart Refrigerator',
# #         'price': '$1299',
# #         'manual': 'Optimal temperature: 3-5°C for fridge, -18°C for freezer. Defrost when ice buildup exceeds 5mm. Clean coils annually.',
# #         'keywords': ['refrigerator', 'fridge', 'freezer', 'cooling'],
# #         'features': ['500L capacity', 'Frost free', 'Convertible freezer', 'Smart diagnosis']
# #     },
# #     {
# #         'id': 5,
# #         'name': 'Robot Vacuum Cleaner',
# #         'price': '$499',
# #         'manual': 'Empty dustbin after each use. Clean brushes weekly. Charge for 3 hours before first use. Works on all floor types.',
# #         'keywords': ['vacuum', 'cleaner', 'robot', 'cleaning'],
# #         'features': ['2-in-1 vacuum & mop', 'App control', '120min runtime', 'Auto-recharge']
# #     }
# # ]

# # # System prompt for the AI assistant
# # SYSTEM_PROMPT = """You are a friendly and helpful AI shopping assistant for an electronics store. 
# # Your personality traits:
# # - Warm, enthusiastic, and conversational
# # - Professional but not robotic
# # - Patient and understanding
# # - Proactive in suggesting products
# # - Always polite and courteous

# # Your responsibilities:
# # 1. Greet customers warmly
# # 2. Help them discover and understand products
# # 3. Answer questions about product features, pricing, and usage
# # 4. Guide them through the purchase process
# # 5. Offer to send product details via email

# # Guidelines:
# # - Keep responses concise (2-3 sentences max)
# # - Be natural and human-like in conversation
# # - Use casual language, avoid technical jargon unless asked
# # - Show enthusiasm about products
# # - Always confirm actions before proceeding
# # - If unsure, admit it honestly

# # Available products: Smart Washing Machine ($599), Air Conditioner ($899), Microwave Oven ($299), Smart Refrigerator ($1299), Robot Vacuum Cleaner ($499)
# # """

# # conversation_history = []

# # @app.route('/api/chat', methods=['POST'])
# # def chat():
# #     """Handle chat messages with LLM"""
# #     data = request.json
# #     user_message = data.get('message', '')
    
# #     if not user_message:
# #         return jsonify({'error': 'No message provided'}), 400
    
# #     # Add user message to history
# #     conversation_history.append({
# #         'role': 'user',
# #         'content': user_message
# #     })
    
# #     # Check if user is asking about a specific product
# #     product_context = find_product_in_message(user_message)
    
# #     # Build context for LLM
# #     context = SYSTEM_PROMPT
# #     if product_context:
# #         context += f"\n\nCurrent product context: {product_context['name']} - {product_context['price']}\nFeatures: {', '.join(product_context['features'])}\nManual: {product_context['manual']}"
    
# #     try:
# #         # Call OpenAI API (v1.0+ syntax)
# #         response = client.chat.completions.create(
# #             model="gpt-3.5-turbo",  # or gpt-4 for better quality
# #             messages=[
# #                 {'role': 'system', 'content': context},
# #                 *conversation_history[-10:]  # Keep last 10 messages for context
# #             ],
# #             max_tokens=150,
# #             temperature=0.8,
# #             presence_penalty=0.6,
# #             frequency_penalty=0.3
# #         )
        
# #         ai_message = response.choices[0].message.content.strip()
        
# #         # Add AI response to history
# #         conversation_history.append({
# #             'role': 'assistant',
# #             'content': ai_message
# #         })
        
# #         return jsonify({
# #             'response': ai_message,
# #             'product': product_context,
# #             'timestamp': datetime.now().isoformat()
# #         })
        
# #     except Exception as e:
# #         print(f"Error: {str(e)}")
# #         # Fallback responses when API fails
# #         fallback_response = get_fallback_response(user_message, product_context)
# #         return jsonify({
# #             'response': fallback_response,
# #             'product': product_context,
# #             'timestamp': datetime.now().isoformat()
# #         })

# # def get_fallback_response(user_message, product_context):
# #     """Provide fallback responses when API is unavailable"""
# #     msg_lower = user_message.lower()
    
# #     # Greetings
# #     if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
# #         return "Hello! Great to hear from you! I can help you explore our amazing products. Would you like to see what we have available?"
    
# #     # Thanks
# #     if 'thank' in msg_lower:
# #         return "You're very welcome! Is there anything else I can help you with today?"
    
# #     # Product context
# #     if product_context:
# #         return f"Excellent choice! The {product_context['name']} is priced at {product_context['price']}. {product_context['manual']} Would you like me to send you the details via email?"
    
# #     # Show products
# #     if 'show' in msg_lower or 'products' in msg_lower:
# #         return "I have 5 amazing products for you! We have a Smart Washing Machine, Air Conditioner, Microwave Oven, Smart Refrigerator, and Robot Vacuum Cleaner. Which one interests you?"
    
# #     # Default
# #     return "I'm here to help you with our products. You can ask me about washing machines, air conditioners, microwaves, refrigerators, or vacuum cleaners. What would you like to know?"

# # @app.route('/api/products', methods=['GET'])
# # def get_products():
# #     """Get all products"""
# #     return jsonify({'products': PRODUCTS})

# # @app.route('/api/products/<int:product_id>', methods=['GET'])
# # def get_product(product_id):
# #     """Get specific product"""
# #     product = next((p for p in PRODUCTS if p['id'] == product_id), None)
# #     if product:
# #         return jsonify({'product': product})
# #     return jsonify({'error': 'Product not found'}), 404

# # @app.route('/api/send-email', methods=['POST'])
# # def send_email():
# #     """Send product details via email"""
# #     data = request.json
# #     email = data.get('email')
# #     product_id = data.get('product_id')
    
# #     if not email or not product_id:
# #         return jsonify({'error': 'Email and product_id required'}), 400
    
# #     product = next((p for p in PRODUCTS if p['id'] == product_id), None)
# #     if not product:
# #         return jsonify({'error': 'Product not found'}), 404
    
# #     try:
# #         # Email configuration (configure with your SMTP settings)
# #         sender_email = os.getenv('SENDER_EMAIL', 'noreply@shop.com')
# #         sender_password = os.getenv('SENDER_PASSWORD')
        
# #         msg = MIMEMultipart()
# #         msg['From'] = sender_email
# #         msg['To'] = email
# #         msg['Subject'] = f"Product Details: {product['name']}"
        
# #         body = f"""
# #         Dear Customer,
        
# #         Thank you for your interest in {product['name']}!
        
# #         Product Details:
# #         ----------------
# #         Name: {product['name']}
# #         Price: {product['price']}
        
# #         Features:
# #         {chr(10).join(f'• {feature}' for feature in product['features'])}
        
# #         User Manual:
# #         {product['manual']}
        
# #         For more information or to make a purchase, please visit our store or contact us.
        
# #         Best regards,
# #         AI Shopping Assistant Team
# #         """
        
# #         msg.attach(MIMEText(body, 'plain'))
        
# #         # Note: Configure SMTP server settings based on your email provider
# #         # For demo purposes, we'll just return success
# #         print(f"Email would be sent to: {email}")
# #         print(f"Product: {product['name']}")
        
# #         return jsonify({
# #             'success': True,
# #             'message': f'Email sent to {email}',
# #             'product': product
# #         })
        
# #     except Exception as e:
# #         print(f"Email error: {str(e)}")
# #         return jsonify({
# #             'success': True,  # Return success anyway for demo
# #             'message': f'Email confirmation sent to {email}',
# #             'product': product
# #         })

# # def find_product_in_message(message):
# #     """Find product mentioned in user message"""
# #     message_lower = message.lower()
# #     for product in PRODUCTS:
# #         if any(keyword in message_lower for keyword in product['keywords']):
# #             return product
# #     return None

# # @app.route('/api/reset', methods=['POST'])
# # def reset_conversation():
# #     """Reset conversation history"""
# #     global conversation_history
# #     conversation_history = []
# #     return jsonify({'success': True, 'message': 'Conversation reset'})

# # @app.route('/api/health', methods=['GET'])
# # def health_check():
# #     """Health check endpoint"""
# #     return jsonify({
# #         'status': 'healthy',
# #         'message': 'AI Shopping Assistant API is running',
# #         'openai_configured': bool(os.getenv('OPENAI_API_KEY'))
# #     })

# # if __name__ == '__main__':
# #     print("=" * 60)
# #     print("🤖 Starting AI Shopping Assistant API...")
# #     print("=" * 60)
# #     print("\nAvailable endpoints:")
# #     print("  GET  /api/health        - Health check")
# #     print("  POST /api/chat          - Chat with AI")
# #     print("  GET  /api/products      - Get all products")
# #     print("  GET  /api/products/<id> - Get specific product")
# #     print("  POST /api/send-email    - Send product details")
# #     print("  POST /api/reset         - Reset conversation")
# #     print("\n" + "=" * 60)
    
# #     # Check if OpenAI API key is set
# #     if not os.getenv('OPENAI_API_KEY'):
# #         print("⚠️  WARNING: OPENAI_API_KEY not found in environment!")
# #         print("   The app will work with fallback responses.")
# #         print("   Set your API key in .env file for full AI features.")
# #     else:
# #         print("✅ OpenAI API key found!")
    
# #     print("\n🚀 Server starting on http://localhost:5000")
# #     print("=" * 60 + "\n")
    
# #     app.run(debug=True, port=5000)
# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from openai import OpenAI
# import os
# import openai
# from datetime import datetime
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# openai.api_key = os.getenv('OPENAI_API_KEY')
# # client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# PRODUCTS = [
#     {
#         'id': 1,
#         'name': 'Smart Washing Machine',
#         'price': '$599',
#         'manual': 'Load capacity: 8kg. Use cold water for delicate fabrics. Run cleaning cycle monthly. Check filter every 3 months.',
#         'keywords': ['washing', 'machine', 'washer', 'laundry', 'wash'],
#         'features': ['8kg capacity', 'Energy efficient', 'Smart connectivity', '15 wash programs'],
#         'description': 'Advanced smart washing machine with AI-powered wash cycles. Perfect for all fabric types with energy-saving technology.'
#     },
#     {
#         'id': 2,
#         'name': 'Air Conditioner',
#         'price': '$899',
#         'manual': 'Set temperature between 22-26°C for optimal efficiency. Clean filters every 2 weeks. Schedule annual maintenance.',
#         'keywords': ['air', 'conditioner', 'ac', 'cooling', 'aircon', 'cool'],
#         'features': ['1.5 ton capacity', 'Inverter technology', 'PM 2.5 filter', 'Voice control'],
#         'description': 'Premium inverter AC with advanced cooling technology and air purification. Energy-efficient and environment-friendly.'
#     },
#     {
#         'id': 3,
#         'name': 'Microwave Oven',
#         'price': '$299',
#         'manual': 'Max power: 1000W. Use microwave-safe containers only. Clean interior after each use. Defrost function available.',
#         'keywords': ['microwave', 'oven', 'heating', 'cook', 'heat'],
#         'features': ['1000W power', '30L capacity', 'Auto-cook menus', 'Child safety lock'],
#         'description': 'Compact and efficient microwave oven with preset cooking modes. Perfect for quick meal preparation.'
#     },
#     {
#         'id': 4,
#         'name': 'Smart Refrigerator',
#         'price': '$1299',
#         'manual': 'Optimal temperature: 3-5°C for fridge, -18°C for freezer. Defrost when ice buildup exceeds 5mm. Clean coils annually.',
#         'keywords': ['refrigerator', 'fridge', 'freezer', 'cooling', 'cold'],
#         'features': ['500L capacity', 'Frost free', 'Convertible freezer', 'Smart diagnosis'],
#         'description': 'Large capacity smart refrigerator with frost-free technology and smart temperature control.'
#     },
#     {
#         'id': 5,
#         'name': 'Robot Vacuum Cleaner',
#         'price': '$499',
#         'manual': 'Empty dustbin after each use. Clean brushes weekly. Charge for 3 hours before first use. Works on all floor types.',
#         'keywords': ['vacuum', 'cleaner', 'robot', 'cleaning', 'sweep'],
#         'features': ['2-in-1 vacuum & mop', 'App control', '120min runtime', 'Auto-recharge'],
#         'description': 'Intelligent robot vacuum that cleans while you relax. Works on all floor types with smart navigation.'
#     }
# ]

# SYSTEM_PROMPT = """You are a friendly and helpful AI shopping assistant for an electronics store.

# Your personality:
# - Warm, enthusiastic, and conversational
# - Professional but not robotic
# - Patient and understanding
# - Proactive in suggesting products
# - Always polite and courteous

# Your responsibilities:
# 1. Greet customers warmly and naturally
# 2. Help them discover products through conversation
# 3. Answer questions about product features, pricing, specifications
# 4. Recommend products based on their needs
# 5. Provide product tips and usage advice
# 6. Guide them without being pushy

# Important Guidelines:
# - Keep responses natural and conversational (1-3 sentences)
# - Use casual, friendly language
# - Show genuine interest in customer needs
# - If customer mentions buying/selecting a product, acknowledge their interest but continue the conversation
# - Only suggest redirecting to product page when they explicitly ask for detailed product info or want to purchase
# - Ask clarifying questions if needed
# - Never be salesy or aggressive
# - If unsure, be honest about it

# Available Products:
# 1. Smart Washing Machine - $599 (keywords: washing, machine, washer, laundry, wash)
# 2. Air Conditioner - $899 (keywords: air, conditioner, ac, cooling, aircon, cool)
# 3. Microwave Oven - $299 (keywords: microwave, oven, heating, cook, heat)
# 4. Smart Refrigerator - $1299 (keywords: refrigerator, fridge, freezer, cooling, cold)
# 5. Robot Vacuum Cleaner - $499 (keywords: vacuum, cleaner, robot, cleaning, sweep)

# When customers ask about specific products, provide helpful information about features, pricing, and usage.
# When they explicitly want to see product details or make a purchase, you can mention viewing the product page.
# """

# conversation_history = []

# @app.route('/api/chat', methods=['POST'])
# def chat():
#     """Handle chat messages with LLM"""
#     data = request.json
#     user_message = data.get('message', '')
    
#     if not user_message:
#         return jsonify({'error': 'No message provided'}), 400
    
#     conversation_history.append({
#         'role': 'user',
#         'content': user_message
#     })
    
#     product_context = find_product_in_message(user_message)
#     intent = detect_intent(user_message)
    
#     context = SYSTEM_PROMPT
#     if product_context:
#         context += f"\n\nCustomer is asking about: {product_context['name']} (${product_context['price'][-3:]})"
#         context += f"\nProduct features: {', '.join(product_context['features'])}"
    
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {'role': 'system', 'content': context},
#                 *conversation_history[-10:]
#             ],
#             max_tokens=150,
#             temperature=0.8,
#             presence_penalty=0.6,
#             frequency_penalty=0.3
#         )
        
#         ai_message = response.choices[0].message.content.strip()
#         conversation_history.append({
#             'role': 'assistant',
#             'content': ai_message
#         })
        
#         should_redirect = should_redirect_to_product(user_message, intent, product_context)
        
#         return jsonify({
#             'response': ai_message,
#             'product': product_context if should_redirect else None,
#             'intent': intent,
#             'timestamp': datetime.now().isoformat()
#         })
        
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         fallback_response = get_fallback_response(user_message, product_context, intent)
#         return jsonify({
#             'response': fallback_response,
#             'product': None,
#             'intent': intent,
#             'timestamp': datetime.now().isoformat()
#         })

# def detect_intent(message):
#     """Detect user intent from message"""
#     msg_lower = message.lower()
    
#     if any(word in msg_lower for word in ['buy', 'purchase', 'checkout', 'order', 'select', 'choose this']):
#         return 'purchase_intent'
#     elif any(word in msg_lower for word in ['show', 'details', 'specifications', 'specs', 'info', 'tell me more', 'see', 'view']):
#         return 'info_request'
#     elif any(word in msg_lower for word in ['recommend', 'suggest', 'which', 'best', 'help me choose']):
#         return 'recommendation'
#     elif any(word in msg_lower for word in ['price', 'cost', 'how much', 'expensive']):
#         return 'price_inquiry'
#     elif any(word in msg_lower for word in ['feature', 'can', 'does', 'how does', 'does it', 'capability']):
#         return 'feature_inquiry'
#     else:
#         return 'general_inquiry'

# def should_redirect_to_product(message, intent, product_context):
#     """Determine if user should be redirected to product details page"""
#     msg_lower = message.lower()
    
#     if not product_context:
#         return False
    
#     # Strong intent to purchase/select
#     buy_triggers = ['buy', 'purchase', 'checkout', 'order', 'select', 'want', 'get', 'i want', "i'd like", 'id like']
    
#     # Check if message contains buying intent with product mention
#     has_buy_intent = any(trigger in msg_lower for trigger in buy_triggers)
#     has_product_mention = any(keyword in msg_lower for keyword in product_context['keywords'])
    
#     return has_buy_intent and has_product_mention

# def get_fallback_response(user_message, product_context, intent):
#     """Provide fallback responses when API is unavailable"""
#     msg_lower = user_message.lower()
    
#     if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
#         return "Hello! Welcome to our electronics store! I'm your AI assistant. What can I help you with today? 😊"
    
#     if any(word in msg_lower for word in ['thank', 'thanks', 'thanks for']):
#         return "You're welcome! Is there anything else you'd like to know about our products?"
    
#     if intent == 'price_inquiry' and product_context:
#         return f"The {product_context['name']} is priced at {product_context['price']}. Great value for its features!"
    
#     if intent == 'feature_inquiry' and product_context:
#         return f"The {product_context['name']} has these awesome features: {', '.join(product_context['features'][:2])}. Would you like to know more?"
    
#     if intent == 'recommendation':
#         return "I'd be happy to help! What are you looking for? Tell me your needs and I can suggest the perfect product for you."
    
#     if 'show' in msg_lower or 'products' in msg_lower or 'list' in msg_lower:
#         return "We have 5 amazing products! Smart Washing Machine, Air Conditioner, Microwave Oven, Smart Refrigerator, and Robot Vacuum Cleaner. Which interests you?"
    
#     if product_context:
#         return f"Great! The {product_context['name']} is {product_context['price']} with fantastic features. Would you like to know more about it?"
    
#     return "I'm here to help! Ask me about our products - washing machines, ACs, microwaves, refrigerators, or vacuum cleaners. What interests you?"

# def find_product_in_message(message):
#     """Find product mentioned in user message"""
#     message_lower = message.lower()
#     for product in PRODUCTS:
#         if any(keyword in message_lower for keyword in product['keywords']):
#             return product
#     return None

# @app.route('/api/products', methods=['GET'])
# def get_products():
#     """Get all products"""
#     return jsonify({'products': PRODUCTS})

# @app.route('/api/products/<int:product_id>', methods=['GET'])
# def get_product(product_id):
#     """Get specific product"""
#     product = next((p for p in PRODUCTS if p['id'] == product_id), None)
#     if product:
#         return jsonify({'product': product})
#     return jsonify({'error': 'Product not found'}), 404

# @app.route('/api/send-email', methods=['POST'])
# def send_email():
#     """Send product details via email"""
#     data = request.json
#     email = data.get('email')
#     product_id = data.get('product_id')
    
#     if not email or not product_id:
#         return jsonify({'error': 'Email and product_id required'}), 400
    
#     product = next((p for p in PRODUCTS if p['id'] == product_id), None)
#     if not product:
#         return jsonify({'error': 'Product not found'}), 404
    
#     try:
#         sender_email = os.getenv('SENDER_EMAIL', 'noreply@shop.com')
#         sender_password = os.getenv('SENDER_PASSWORD')
        
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = email
#         msg['Subject'] = f"Product Details: {product['name']}"
        
#         body = f"""
# Dear Customer,

# Thank you for your interest in {product['name']}!

# PRODUCT DETAILS
# ===============
# Name: {product['name']}
# Price: {product['price']}

# FEATURES:
# {chr(10).join(f'✓ {feature}' for feature in product['features'])}

# USAGE GUIDE:
# {product['manual']}

# For more information or to make a purchase, please visit our store or contact us.

# Best regards,
# AI Shopping Assistant Team
#         """
        
#         msg.attach(MIMEText(body, 'plain'))
#         print(f"Email would be sent to: {email}")
#         print(f"Product: {product['name']}")
        
#         return jsonify({
#             'success': True,
#             'message': f'Email sent to {email}',
#             'product': product
#         })
        
#     except Exception as e:
#         print(f"Email error: {str(e)}")
#         return jsonify({
#             'success': True,
#             'message': f'Email confirmation sent to {email}',
#             'product': product
#         })

# @app.route('/api/reset', methods=['POST'])
# def reset_conversation():
#     """Reset conversation history"""
#     global conversation_history
#     conversation_history = []
#     return jsonify({'success': True, 'message': 'Conversation reset'})

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         'status': 'healthy',
#         'message': 'AI Shopping Assistant API is running',
#         'openai_configured': bool(os.getenv('OPENAI_API_KEY'))
#     })

# if __name__ == '__main__':
#     print("=" * 60)
#     print("🤖 Starting AI Shopping Assistant API...")
#     print("=" * 60)
#     print("\nAvailable endpoints:")
#     print("  GET  /api/health        - Health check")
#     print("  POST /api/chat          - Chat with AI")
#     print("  GET  /api/products      - Get all products")
#     print("  GET  /api/products/<id> - Get specific product")
#     print("  POST /api/send-email    - Send product details")
#     print("  POST /api/reset         - Reset conversation")
#     print("\n" + "=" * 60)
    
#     if not os.getenv('OPENAI_API_KEY'):
#         print("⚠️  WARNING: OPENAI_API_KEY not found in environment!")
#         print("   Set your API key in .env file for full AI features.")
#     else:
#         print("✅ OpenAI API key found!")
    
#     print("\n🚀 Server starting on http://localhost:5000")
#     print("=" * 60 + "\n")
    
#     app.run(debug=True, port=5000)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from openai import OpenAI
# import os
# import openai
# from datetime import datetime
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv
# load_dotenv()

# app = Flask(__name__)
# CORS(app)

# openai.api_key = os.getenv('OPENAI_API_KEY')

# PRODUCTS = [
#     {
#         'id': 1,
#         'name': 'Smart Washing Machine',
#         'price': '$599',
#         'manual': 'Load capacity: 8kg. Use cold water for delicate fabrics. Run cleaning cycle monthly. Check filter every 3 months.',
#         'keywords': ['washing', 'machine', 'washer', 'laundry', 'wash'],
#         'features': ['8kg capacity', 'Energy efficient', 'Smart connectivity', '15 wash programs'],
#         'description': 'Advanced smart washing machine with AI-powered wash cycles. Perfect for all fabric types with energy-saving technology.'
#     },
#     {
#         'id': 2,
#         'name': 'Air Conditioner',
#         'price': '$899',
#         'manual': 'Set temperature between 22-26°C for optimal efficiency. Clean filters every 2 weeks. Schedule annual maintenance.',
#         'keywords': ['air', 'conditioner', 'ac', 'cooling', 'aircon', 'cool'],
#         'features': ['1.5 ton capacity', 'Inverter technology', 'PM 2.5 filter', 'Voice control'],
#         'description': 'Premium inverter AC with advanced cooling technology and air purification. Energy-efficient and environment-friendly.'
#     },
#     {
#         'id': 3,
#         'name': 'Microwave Oven',
#         'price': '$299',
#         'manual': 'Max power: 1000W. Use microwave-safe containers only. Clean interior after each use. Defrost function available.',
#         'keywords': ['microwave', 'oven', 'heating', 'cook', 'heat'],
#         'features': ['1000W power', '30L capacity', 'Auto-cook menus', 'Child safety lock'],
#         'description': 'Compact and efficient microwave oven with preset cooking modes. Perfect for quick meal preparation.'
#     },
#     {
#         'id': 4,
#         'name': 'Smart Refrigerator',
#         'price': '$1299',
#         'manual': 'Optimal temperature: 3-5°C for fridge, -18°C for freezer. Defrost when ice buildup exceeds 5mm. Clean coils annually.',
#         'keywords': ['refrigerator', 'fridge', 'freezer', 'cooling', 'cold'],
#         'features': ['500L capacity', 'Frost free', 'Convertible freezer', 'Smart diagnosis'],
#         'description': 'Large capacity smart refrigerator with frost-free technology and smart temperature control.'
#     },
#     {
#         'id': 5,
#         'name': 'Robot Vacuum Cleaner',
#         'price': '$499',
#         'manual': 'Empty dustbin after each use. Clean brushes weekly. Charge for 3 hours before first use. Works on all floor types.',
#         'keywords': ['vacuum', 'cleaner', 'robot', 'cleaning', 'sweep'],
#         'features': ['2-in-1 vacuum & mop', 'App control', '120min runtime', 'Auto-recharge'],
#         'description': 'Intelligent robot vacuum that cleans while you relax. Works on all floor types with smart navigation.'
#     }
# ]

# SYSTEM_PROMPT = """You are a friendly and helpful AI shopping assistant for an electronics store.

# Your personality:
# - Warm, enthusiastic, and conversational
# - Professional but not robotic
# - Patient and understanding
# - Proactive in suggesting products
# - Always polite and courteous

# Your responsibilities:
# 1. Greet customers warmly and naturally
# 2. Help them discover products through conversation
# 3. Answer questions about product features, pricing, specifications
# 4. Recommend products based on their needs
# 5. Provide product tips and usage advice
# 6. Guide them without being pushy

# Important Guidelines:
# - Keep responses natural and conversational (1-3 sentences)
# - Use casual, friendly language
# - Show genuine interest in customer needs
# - When customer shows buying intent, acknowledge and prepare them for product details page
# - Ask clarifying questions if needed
# - Never be salesy or aggressive
# - If unsure, be honest about it

# Available Products:
# 1. Smart Washing Machine - $599 (keywords: washing, machine, washer, laundry, wash)
# 2. Air Conditioner - $899 (keywords: air, conditioner, ac, cooling, aircon, cool)
# 3. Microwave Oven - $299 (keywords: microwave, oven, heating, cook, heat)
# 4. Smart Refrigerator - $1299 (keywords: refrigerator, fridge, freezer, cooling, cold)
# 5. Robot Vacuum Cleaner - $499 (keywords: vacuum, cleaner, robot, cleaning, sweep)

# When customers express buying intent, acknowledge it warmly and let them know you'll show them the details.
# """

# conversation_history = []

# @app.route('/api/chat', methods=['POST'])
# def chat():
#     """Handle chat messages with LLM"""
#     data = request.json
#     user_message = data.get('message', '')
    
#     if not user_message:
#         return jsonify({'error': 'No message provided'}), 400
    
#     conversation_history.append({
#         'role': 'user',
#         'content': user_message
#     })
  
#     product_context = find_product_in_message(user_message)
#     intent = detect_intent(user_message)

#     context = SYSTEM_PROMPT
#     if product_context:
#         context += f"\n\nCustomer is asking about: {product_context['name']} ({product_context['price']})"
#         context += f"\nProduct features: {', '.join(product_context['features'])}"
    
   
#     should_redirect = should_redirect_to_product(user_message, intent, product_context)
    
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {'role': 'system', 'content': context},
#                 *conversation_history[-10:]
#             ],
#             max_tokens=150,
#             temperature=0.8,
#             presence_penalty=0.6,
#             frequency_penalty=0.3
#         )
        
#         ai_message = response.choices[0].message.content.strip()
        
#         # If redirecting, add a transition message
#         if should_redirect and product_context:
#             ai_message += f" Let me show you the {product_context['name']} details!"
        
#         conversation_history.append({
#             'role': 'assistant',
#             'content': ai_message
#         })
        
#         return jsonify({
#             'response': ai_message,
#             'product': product_context if should_redirect else None,
#             'intent': intent,
#             'timestamp': datetime.now().isoformat()
#         })
        
#     except Exception as e:
#         print(f"Error: {str(e)}")
#         fallback_response = get_fallback_response(user_message, product_context, intent)
        
#         # Add transition for fallback too
#         if should_redirect and product_context:
#             fallback_response += f" Let me show you the {product_context['name']} details!"
        
#         return jsonify({
#             'response': fallback_response,
#             'product': product_context if should_redirect else None,
#             'intent': intent,
#             'timestamp': datetime.now().isoformat()
#         })

# def detect_intent(message):
#     """Detect user intent from message"""
#     msg_lower = message.lower()
    
#     # Check for purchase intent - EXPANDED
#     if any(word in msg_lower for word in ['buy', 'purchase', 'checkout', 'order', 'select', 'choose', 'want', 'need', 'get', 'interested in', 'looking for']):
#         return 'purchase_intent'
#     elif any(word in msg_lower for word in ['show', 'details', 'specifications', 'specs', 'info', 'tell me more', 'see', 'view']):
#         return 'info_request'
#     elif any(word in msg_lower for word in ['recommend', 'suggest', 'which', 'best', 'help me choose']):
#         return 'recommendation'
#     elif any(word in msg_lower for word in ['price', 'cost', 'how much', 'expensive']):
#         return 'price_inquiry'
#     elif any(word in msg_lower for word in ['feature', 'can', 'does', 'how does', 'does it', 'capability']):
#         return 'feature_inquiry'
#     else:
#         return 'general_inquiry'

# def should_redirect_to_product(message, intent, product_context):
#     """Determine if user should be redirected to product details page"""
    
#     # Must have a product context to redirect
#     if not product_context:
#         return False
    
#     msg_lower = message.lower()
    
#     # Expanded buy triggers - more natural language patterns
#     buy_triggers = [
#         'buy', 'purchase', 'checkout', 'order', 
#         'want', 'need', 'get', 'i want', "i'd like", 
#         'id like', 'select', 'choose', 'interested in',
#         'looking for', 'show me', 'take'
#     ]
    
#     # Check if ANY buy trigger is in the message
#     has_buy_intent = any(trigger in msg_lower for trigger in buy_triggers)
    
#     # Check if product is mentioned (by name or keywords)
#     product_name_lower = product_context['name'].lower()
#     has_product_mention = (
#         product_name_lower in msg_lower or 
#         any(keyword in msg_lower for keyword in product_context['keywords'])
#     )
    
#     # Redirect if:
#     # 1. User has buy intent AND mentions product, OR
#     # 2. Intent is purchase_intent or info_request with product mention
#     should_redirect = (
#         (has_buy_intent and has_product_mention) or
#         (intent in ['purchase_intent', 'info_request'] and has_product_mention)
#     )
    
#     # Debug logging
#     print(f"\n=== Redirect Analysis ===")
#     print(f"Message: {message}")
#     print(f"Product: {product_context['name'] if product_context else 'None'}")
#     print(f"Intent: {intent}")
#     print(f"Has buy intent: {has_buy_intent}")
#     print(f"Has product mention: {has_product_mention}")
#     print(f"Should redirect: {should_redirect}")
#     print(f"========================\n")
    
#     return should_redirect

# def get_fallback_response(user_message, product_context, intent):
#     """Provide fallback responses when API is unavailable"""
#     msg_lower = user_message.lower()
    
#     if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
#         return "Hello! Welcome to our electronics store! I'm your AI assistant. What can I help you with today? 😊"
    
#     if any(word in msg_lower for word in ['thank', 'thanks', 'thanks for']):
#         return "You're welcome! Is there anything else you'd like to know about our products?"
    
#     # If user wants to buy and product is found
#     if intent == 'purchase_intent' and product_context:
#         return f"Great choice! The {product_context['name']} is an excellent product at {product_context['price']}."
    
#     if intent == 'price_inquiry' and product_context:
#         return f"The {product_context['name']} is priced at {product_context['price']}. Great value for its features!"
    
#     if intent == 'feature_inquiry' and product_context:
#         return f"The {product_context['name']} has these awesome features: {', '.join(product_context['features'][:2])}. Would you like to know more?"
    
#     if intent == 'recommendation':
#         return "I'd be happy to help! What are you looking for? Tell me your needs and I can suggest the perfect product for you."
    
#     if 'show' in msg_lower or 'products' in msg_lower or 'list' in msg_lower:
#         return "We have 5 amazing products! Smart Washing Machine, Air Conditioner, Microwave Oven, Smart Refrigerator, and Robot Vacuum Cleaner. Which interests you?"
    
#     if product_context:
#         return f"Great! The {product_context['name']} is {product_context['price']} with fantastic features."
    
#     return "I'm here to help! Ask me about our products - washing machines, ACs, microwaves, refrigerators, or vacuum cleaners. What interests you?"

# def find_product_in_message(message):
#     """Find product mentioned in user message - IMPROVED"""
#     message_lower = message.lower()
    
#     # Try to find exact product name first
#     for product in PRODUCTS:
#         product_name_lower = product['name'].lower()
#         if product_name_lower in message_lower:
#             return product
    
#     # Then try keywords
#     for product in PRODUCTS:
#         if any(keyword in message_lower for keyword in product['keywords']):
#             return product
    
#     return None

# @app.route('/api/products', methods=['GET'])
# def get_products():
#     """Get all products"""
#     return jsonify({'products': PRODUCTS})

# @app.route('/api/products/<int:product_id>', methods=['GET'])
# def get_product(product_id):
#     """Get specific product"""
#     product = next((p for p in PRODUCTS if p['id'] == product_id), None)
#     if product:
#         return jsonify({'product': product})
#     return jsonify({'error': 'Product not found'}), 404

# @app.route('/api/send-email', methods=['POST'])
# def send_email():
#     """Send product details via email"""
#     data = request.json
#     email = data.get('email')
#     product_id = data.get('product_id')
    
#     if not email or not product_id:
#         return jsonify({'error': 'Email and product_id required'}), 400
    
#     product = next((p for p in PRODUCTS if p['id'] == product_id), None)
#     if not product:
#         return jsonify({'error': 'Product not found'}), 404
    
#     try:
#         sender_email = os.getenv('SENDER_EMAIL', 'noreply@shop.com')
#         sender_password = os.getenv('SENDER_PASSWORD')
        
#         msg = MIMEMultipart()
#         msg['From'] = sender_email
#         msg['To'] = email
#         msg['Subject'] = f"Product Details: {product['name']}"
        
#         body = f"""
# Dear Customer,

# Thank you for your interest in {product['name']}!

# PRODUCT DETAILS
# ===============
# Name: {product['name']}
# Price: {product['price']}

# FEATURES:
# {chr(10).join(f'✓ {feature}' for feature in product['features'])}

# USAGE GUIDE:
# {product['manual']}

# For more information or to make a purchase, please visit our store or contact us.

# Best regards,
# AI Shopping Assistant Team
#         """
        
#         msg.attach(MIMEText(body, 'plain'))
#         print(f"Email would be sent to: {email}")
#         print(f"Product: {product['name']}")
        
#         return jsonify({
#             'success': True,
#             'message': f'Email sent to {email}',
#             'product': product
#         })
        
#     except Exception as e:
#         print(f"Email error: {str(e)}")
#         return jsonify({
#             'success': True,
#             'message': f'Email confirmation sent to {email}',
#             'product': product
#         })

# @app.route('/api/reset', methods=['POST'])
# def reset_conversation():
#     """Reset conversation history"""
#     global conversation_history
#     conversation_history = []
#     return jsonify({'success': True, 'message': 'Conversation reset'})

# @app.route('/api/health', methods=['GET'])
# def health_check():
#     """Health check endpoint"""
#     return jsonify({
#         'status': 'healthy',
#         'message': 'AI Shopping Assistant API is running',
#         'openai_configured': bool(os.getenv('OPENAI_API_KEY'))
#     })

# if __name__ == '__main__':
#     print("=" * 60)
#     print("🤖 Starting AI Shopping Assistant API...")
#     print("=" * 60)
#     print("\nAvailable endpoints:")
#     print("  GET  /api/health        - Health check")
#     print("  POST /api/chat          - Chat with AI")
#     print("  GET  /api/products      - Get all products")
#     print("  GET  /api/products/<id> - Get specific product")
#     print("  POST /api/send-email    - Send product details")
#     print("  POST /api/reset         - Reset conversation")
#     print("\n" + "=" * 60)
    
#     if not os.getenv('OPENAI_API_KEY'):
#         print("⚠️  WARNING: OPENAI_API_KEY not found in environment!")
#         print("   Set your API key in .env file for full AI features.")
#     else:
#         print("✅ OpenAI API key found!")
    
#     print("\n🚀 Server starting on http://localhost:5000")
#     print("=" * 60 + "\n")
    
#     app.run(debug=True, port=5000)


from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import openai
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv('OPENAI_API_KEY')

PRODUCTS = [
    {
        'id': 1,
        'name': 'Smart Washing Machine',
        'price': '$599',
        'manual': 'Load capacity: 8kg. Use cold water for delicate fabrics. Run cleaning cycle monthly. Check filter every 3 months.',
        'keywords': ['washing', 'machine', 'washer', 'laundry', 'wash'],
        'features': ['8kg capacity', 'Energy efficient', 'Smart connectivity', '15 wash programs'],
        'description': 'Advanced smart washing machine with AI-powered wash cycles. Perfect for all fabric types with energy-saving technology.'
    },
    {
        'id': 2,
        'name': 'Air Conditioner',
        'price': '$899',
        'manual': 'Set temperature between 22-26°C for optimal efficiency. Clean filters every 2 weeks. Schedule annual maintenance.',
        'keywords': ['air', 'conditioner', 'ac', 'cooling', 'aircon', 'cool'],
        'features': ['1.5 ton capacity', 'Inverter technology', 'PM 2.5 filter', 'Voice control'],
        'description': 'Premium inverter AC with advanced cooling technology and air purification. Energy-efficient and environment-friendly.'
    },
    {
        'id': 3,
        'name': 'Microwave Oven',
        'price': '$299',
        'manual': 'Max power: 1000W. Use microwave-safe containers only. Clean interior after each use. Defrost function available.',
        'keywords': ['microwave', 'oven', 'heating', 'cook', 'heat'],
        'features': ['1000W power', '30L capacity', 'Auto-cook menus', 'Child safety lock'],
        'description': 'Compact and efficient microwave oven with preset cooking modes. Perfect for quick meal preparation.'
    },
    {
        'id': 4,
        'name': 'Smart Refrigerator',
        'price': '$1299',
        'manual': 'Optimal temperature: 3-5°C for fridge, -18°C for freezer. Defrost when ice buildup exceeds 5mm. Clean coils annually.',
        'keywords': ['refrigerator', 'fridge', 'freezer', 'cooling', 'cold'],
        'features': ['500L capacity', 'Frost free', 'Convertible freezer', 'Smart diagnosis'],
        'description': 'Large capacity smart refrigerator with frost-free technology and smart temperature control.'
    },
    {
        'id': 5,
        'name': 'Robot Vacuum Cleaner',
        'price': '$499',
        'manual': 'Empty dustbin after each use. Clean brushes weekly. Charge for 3 hours before first use. Works on all floor types.',
        'keywords': ['vacuum', 'cleaner', 'robot', 'cleaning', 'sweep'],
        'features': ['2-in-1 vacuum & mop', 'App control', '120min runtime', 'Auto-recharge'],
        'description': 'Intelligent robot vacuum that cleans while you relax. Works on all floor types with smart navigation.'
    }
]

SYSTEM_PROMPT = """You are a friendly and helpful AI shopping assistant for an electronics store.

Your personality:
- Warm, enthusiastic, and conversational
- Professional but not robotic
- Patient and understanding
- Proactive in suggesting products
- Always polite and courteous

Your responsibilities:
1. Greet customers warmly and naturally
2. Help them discover products through conversation
3. Answer questions about product features, pricing, specifications
4. Recommend products based on their needs
5. Provide product tips and usage advice
6. Guide them without being pushy

Important Guidelines:
- Keep responses natural and conversational (1-3 sentences)
- Use casual, friendly language
- Show genuine interest in customer needs
- When customer shows buying intent, acknowledge and prepare them for product details page
- Ask clarifying questions if needed
- Never be salesy or aggressive
- If unsure, be honest about it

Available Products:
1. Smart Washing Machine - $599 (keywords: washing, machine, washer, laundry, wash)
2. Air Conditioner - $899 (keywords: air, conditioner, ac, cooling, aircon, cool)
3. Microwave Oven - $299 (keywords: microwave, oven, heating, cook, heat)
4. Smart Refrigerator - $1299 (keywords: refrigerator, fridge, freezer, cooling, cold)
5. Robot Vacuum Cleaner - $499 (keywords: vacuum, cleaner, robot, cleaning, sweep)

When customers express buying intent, acknowledge it warmly and let them know you'll show them the details.
"""

conversation_history = []

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages with LLM"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    
    conversation_history.append({
        'role': 'user',
        'content': user_message
    })
  
    product_context = find_product_in_message(user_message)
    intent = detect_intent(user_message)

    context = SYSTEM_PROMPT
    if product_context:
        context += f"\n\nCustomer is asking about: {product_context['name']} ({product_context['price']})"
        context += f"\nProduct features: {', '.join(product_context['features'])}"
    
   
    should_redirect = should_redirect_to_product(user_message, intent, product_context)
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'system', 'content': context},
                *conversation_history[-10:]
            ],
            max_tokens=150,
            temperature=0.8,
            presence_penalty=0.6,
            frequency_penalty=0.3
        )
        
        ai_message = response.choices[0].message.content.strip()
        
        # If redirecting, create a confirmation message
        if should_redirect and product_context:
            confirmation_msg = generate_confirmation_message(product_context, user_message)
            ai_message = confirmation_msg
        
        conversation_history.append({
            'role': 'assistant',
            'content': ai_message
        })
        
        return jsonify({
            'response': ai_message,
            'product': product_context if should_redirect else None,
            'intent': intent,
            'should_redirect': should_redirect,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        fallback_response = get_fallback_response(user_message, product_context, intent)
        
        # If redirecting, generate confirmation for fallback too
        if should_redirect and product_context:
            fallback_response = generate_confirmation_message(product_context, user_message)
        
        return jsonify({
            'response': fallback_response,
            'product': product_context if should_redirect else None,
            'intent': intent,
            'should_redirect': should_redirect,
            'timestamp': datetime.now().isoformat()
        })

def generate_confirmation_message(product, user_message):
    """Generate a confirmation message before showing product details"""
    messages = [
        f"Great choice!",
        f"Perfect!",
        f"Excellent!",
        f"Awesome!",
        f"शानदार पसंद!",
        f"बिलकुल!",
        f"शानदार!",
        f"बढ़िया चुनाव!",
    ]
    
    import random
    return random.choice(messages)

def detect_intent(message):
    """Detect user intent from message"""
    msg_lower = message.lower()
    
    # Check for purchase intent - EXPANDED
    if any(word in msg_lower for word in ['buy', 'purchase', 'checkout', 'order', 'select', 'choose', 'want', 'need', 'get', 'interested in', 'looking for']):
        return 'purchase_intent'
    elif any(word in msg_lower for word in ['show', 'details', 'specifications', 'specs', 'info', 'tell me more', 'see', 'view']):
        return 'info_request'
    elif any(word in msg_lower for word in ['recommend', 'suggest', 'which', 'best', 'help me choose']):
        return 'recommendation'
    elif any(word in msg_lower for word in ['price', 'cost', 'how much', 'expensive']):
        return 'price_inquiry'
    elif any(word in msg_lower for word in ['feature', 'can', 'does', 'how does', 'does it', 'capability']):
        return 'feature_inquiry'
    else:
        return 'general_inquiry'

def should_redirect_to_product(message, intent, product_context):
    """Determine if user should be redirected to product details page"""
    
    # Must have a product context to redirect
    if not product_context:
        return False
    
    msg_lower = message.lower()
    
    # Expanded buy triggers - more natural language patterns
    buy_triggers = [
        'buy', 'purchase', 'checkout', 'order', 
        'want', 'need', 'get', 'i want', "i'd like", 
        'id like', 'select', 'choose', 'interested in',
        'looking for', 'show me', 'take', 'लूँ', 'चाहिए', 'चाहता', 'चाहती'
    ]
    
    # Check if ANY buy trigger is in the message
    has_buy_intent = any(trigger in msg_lower for trigger in buy_triggers)
    
    # Check if product is mentioned (by name or keywords)
    product_name_lower = product_context['name'].lower()
    has_product_mention = (
        product_name_lower in msg_lower or 
        any(keyword in msg_lower for keyword in product_context['keywords'])
    )
    
    # Redirect if:
    # 1. User has buy intent AND mentions product, OR
    # 2. Intent is purchase_intent or info_request with product mention
    should_redirect = (
        (has_buy_intent and has_product_mention) or
        (intent in ['purchase_intent', 'info_request'] and has_product_mention)
    )
    
    # Debug logging
    print(f"\n=== Redirect Analysis ===")
    print(f"Message: {message}")
    print(f"Product: {product_context['name'] if product_context else 'None'}")
    print(f"Intent: {intent}")
    print(f"Has buy intent: {has_buy_intent}")
    print(f"Has product mention: {has_product_mention}")
    print(f"Should redirect: {should_redirect}")
    print(f"========================\n")
    
    return should_redirect

def get_fallback_response(user_message, product_context, intent):
    """Provide fallback responses when API is unavailable"""
    msg_lower = user_message.lower()
    
    if any(word in msg_lower for word in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']):
        return "Hello! Welcome to our electronics store! I'm your AI assistant. What can I help you with today? 😊"
    
    if any(word in msg_lower for word in ['thank', 'thanks', 'thanks for']):
        return "You're welcome! Is there anything else you'd like to know about our products?"
    
    # If user wants to buy and product is found
    if intent == 'purchase_intent' and product_context:
        return f"Great choice! The {product_context['name']} is an excellent product at {product_context['price']}."
    
    if intent == 'price_inquiry' and product_context:
        return f"The {product_context['name']} is priced at {product_context['price']}. Great value for its features!"
    
    if intent == 'feature_inquiry' and product_context:
        return f"The {product_context['name']} has these awesome features: {', '.join(product_context['features'][:2])}. Would you like to know more?"
    
    if intent == 'recommendation':
        return "I'd be happy to help! What are you looking for? Tell me your needs and I can suggest the perfect product for you."
    
    if 'show' in msg_lower or 'products' in msg_lower or 'list' in msg_lower:
        return "We have 5 amazing products! Smart Washing Machine, Air Conditioner, Microwave Oven, Smart Refrigerator, and Robot Vacuum Cleaner. Which interests you?"
    
    if product_context:
        return f"Great! The {product_context['name']} is {product_context['price']} with fantastic features."
    
    return "I'm here to help! Ask me about our products - washing machines, ACs, microwaves, refrigerators, or vacuum cleaners. What interests you?"

def find_product_in_message(message):
    """Find product mentioned in user message - IMPROVED"""
    message_lower = message.lower()
    
    # Try to find exact product name first
    for product in PRODUCTS:
        product_name_lower = product['name'].lower()
        if product_name_lower in message_lower:
            return product
    
    # Then try keywords
    for product in PRODUCTS:
        if any(keyword in message_lower for keyword in product['keywords']):
            return product
    
    return None

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products"""
    return jsonify({'products': PRODUCTS})

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get specific product"""
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        return jsonify({'product': product})
    return jsonify({'error': 'Product not found'}), 404

@app.route('/api/send-email', methods=['POST'])
def send_email():
    """Send product details via email"""
    data = request.json
    email = data.get('email')
    product_id = data.get('product_id')
    
    if not email or not product_id:
        return jsonify({'error': 'Email and product_id required'}), 400
    
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    try:
        sender_email = os.getenv('SENDER_EMAIL', 'noreply@shop.com')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = f"Product Details: {product['name']}"
        
        body = f"""
Dear Customer,

Thank you for your interest in {product['name']}!

PRODUCT DETAILS
===============
Name: {product['name']}
Price: {product['price']}

FEATURES:
{chr(10).join(f'✓ {feature}' for feature in product['features'])}

USAGE GUIDE:
{product['manual']}

For more information or to make a purchase, please visit our store or contact us.

Best regards,
AI Shopping Assistant Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        print(f"Email would be sent to: {email}")
        print(f"Product: {product['name']}")
        
        return jsonify({
            'success': True,
            'message': f'Email sent to {email}',
            'product': product
        })
        
    except Exception as e:
        print(f"Email error: {str(e)}")
        return jsonify({
            'success': True,
            'message': f'Email confirmation sent to {email}',
            'product': product
        })

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({'success': True, 'message': 'Conversation reset'})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'AI Shopping Assistant API is running',
        'openai_configured': bool(os.getenv('OPENAI_API_KEY'))
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🤖 Starting AI Shopping Assistant API...")
    print("=" * 60)
    print("\nAvailable endpoints:")
    print("  GET  /api/health        - Health check")
    print("  POST /api/chat          - Chat with AI")
    print("  GET  /api/products      - Get all products")
    print("  GET  /api/products/<id> - Get specific product")
    print("  POST /api/send-email    - Send product details")
    print("  POST /api/reset         - Reset conversation")
    print("\n" + "=" * 60)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("⚠️  WARNING: OPENAI_API_KEY not found in environment!")
        print("   Set your API key in .env file for full AI features.")
    else:
        print("✅ OpenAI API key found!")
    
    print("\n🚀 Server starting on http://localhost:5000")
    print("=" * 60 + "\n")
    
    app.run(debug=True, port=5000)