# ========================================
# JUSTIN E-COMMERCE - Checkout Routes
# ========================================

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from models import db, Product, Cart, Order, OrderItem
import stripe
import os
from config import Config
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

checkout_bp = Blueprint('checkout', __name__)

# Initialize Stripe
stripe.api_key = Config.STRIPE_SECRET_KEY

def get_session_id():
    """Get session ID"""
    return session.get('session_id', '')

@checkout_bp.route('/checkout')
def checkout():
    """Checkout page"""
    session_id = get_session_id()
    
    # Get cart items
    cart_items = Cart.query.filter_by(session_id=session_id).all()
    
    if not cart_items:
        return redirect(url_for('cart.view_cart'))
    
    # Calculate totals
    subtotal = sum(item.get_subtotal() for item in cart_items)
    tax_rate = Config.TAX_RATE
    tax = int(subtotal * tax_rate)
    shipping = Config.SHIPPING_COST
    total = subtotal + tax + shipping
    
    return render_template(
        'checkout.html',
        cart_items=cart_items,
        subtotal=subtotal,
        tax=tax,
        shipping=shipping,
        total=total,
        stripe_publishable_key=Config.STRIPE_PUBLISHABLE_KEY
    )

@checkout_bp.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    """Create Stripe payment intent"""
    try:
        data = request.get_json()
        session_id = get_session_id()
        
        # Get cart items
        cart_items = Cart.query.filter_by(session_id=session_id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate total
        subtotal = sum(item.get_subtotal() for item in cart_items)
        tax = int(subtotal * Config.TAX_RATE)
        shipping = Config.SHIPPING_COST
        total = subtotal + tax + shipping
        
        # Create payment intent
        intent = stripe.PaymentIntent.create(
            amount=total,
            currency=Config.STRIPE_CURRENCY,
            metadata={
                'session_id': session_id,
                'customer_email': data.get('email', '')
            }
        )
        
        return jsonify({
            'clientSecret': intent.client_secret,
            'amount': total
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@checkout_bp.route('/process-order', methods=['POST'])
def process_order():
    """Process order after successful payment"""
    try:
        data = request.get_json()
        session_id = get_session_id()
        
        # Get cart items
        cart_items = Cart.query.filter_by(session_id=session_id).all()
        
        if not cart_items:
            return jsonify({'error': 'Cart is empty'}), 400
        
        # Calculate totals
        subtotal = sum(item.get_subtotal() for item in cart_items)
        tax = int(subtotal * Config.TAX_RATE)
        shipping = Config.SHIPPING_COST
        total = subtotal + tax + shipping
        
        # Create order
        order = Order(
            order_number=Order.generate_order_number(),
            customer_name=data.get('name'),
            customer_email=data.get('email'),
            customer_phone=data.get('phone', ''),
            shipping_address=data.get('address'),
            shipping_city=data.get('city'),
            shipping_state=data.get('state'),
            shipping_zip=data.get('zip'),
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            total=total,
            stripe_payment_id=data.get('payment_intent_id'),
            stripe_payment_status='succeeded',
            status='processing'
        )
        
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items and reduce stock
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                product_name=cart_item.product.name,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                subtotal=cart_item.get_subtotal()
            )
            db.session.add(order_item)
            
            # Reduce product stock
            cart_item.product.reduce_stock(cart_item.quantity)
        
        # Clear cart
        Cart.query.filter_by(session_id=session_id).delete()
        
        db.session.commit()
        
        # Send confirmation email
        send_order_confirmation(order)
        
        return jsonify({
            'success': True,
            'order_number': order.order_number,
            'order_id': order.id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@checkout_bp.route('/confirmation/<order_number>')
def confirmation(order_number):
    """Order confirmation page"""
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    
    return render_template('confirmation.html', order=order)

def send_order_confirmation(order):
    """Send order confirmation email via SendGrid"""
    try:
        if not Config.SENDGRID_API_KEY:
            print("SendGrid API key not configured - skipping email")
            return
        
        # Create email content
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: linear-gradient(135deg, #1e3a5f, #4a90e2); padding: 30px; text-align: center;">
                <h1 style="color: white; margin: 0;">JUSTIN E-COMMERCE</h1>
                <p style="color: #c0c5ce; margin: 10px 0 0 0;">Order Confirmation</p>
            </div>
            
            <div style="padding: 30px; background: #f5f5f5;">
                <h2>Thank you for your order!</h2>
                <p>Hi {order.customer_name},</p>
                <p>Your order has been confirmed and is being processed.</p>
                
                <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3>Order Details</h3>
                    <p><strong>Order Number:</strong> {order.order_number}</p>
                    <p><strong>Order Date:</strong> {order.created_at.strftime('%B %d, %Y')}</p>
                    <p><strong>Total:</strong> ${order.total / 100:.2f}</p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3>Shipping Address</h3>
                    <p>{order.get_full_address()}</p>
                </div>
                
                <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h3>Order Items</h3>
                    {''.join([f'<p>{item.product_name} x {item.quantity} - ${item.subtotal / 100:.2f}</p>' for item in order.items])}
                </div>
                
                <p style="margin-top: 30px;">We'll send you another email when your order ships.</p>
                
                <p style="color: #666; font-size: 12px; margin-top: 40px;">
                    Questions? Contact us at {Config.FROM_EMAIL}
                </p>
            </div>
        </body>
        </html>
        """
        
        message = Mail(
            from_email=Config.FROM_EMAIL,
            to_emails=order.customer_email,
            subject=f'Order Confirmation - {order.order_number}',
            html_content=html_content
        )
        
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)
        
        print(f"Confirmation email sent to {order.customer_email}")
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")

# ========================================
# END OF CHECKOUT ROUTES
# ========================================