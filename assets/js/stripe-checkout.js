/**
 * AiVRIC Stripe Checkout Integration
 *
 * This file handles Stripe Checkout session creation and Customer Portal redirection
 * for the AiVRIC subscription system.
 *
 * IMPORTANT: The Stripe publishable key is injected during GitHub Actions deployment
 * via the placeholder %%STRIPE_PUBLISHABLE_KEY%% from GitHub Secrets.
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        defenseApiUrl: 'https://defense-api.aivric.com',
        stripePublishableKey: '%%STRIPE_PUBLISHABLE_KEY%%', // Replaced by GitHub Actions
        successUrl: window.location.origin + '/success.html',
        cancelUrl: window.location.origin + '/pricing.html'
    };

    // Initialize Stripe.js
    let stripe = null;
    try {
        stripe = Stripe(CONFIG.stripePublishableKey);
    } catch (error) {
        console.error('Failed to initialize Stripe:', error);
        showError('Failed to initialize payment system. Please refresh the page.');
    }

    /**
     * Product Price IDs (must match Stripe Dashboard)
     * These will be updated after creating products in Stripe Dashboard
     */
    const PRICE_IDS = {
        defense: 'price_XXXXXXXXXX', // Replace with actual Stripe Price ID
        offense: 'price_XXXXXXXXXX', // Replace with actual Stripe Price ID
        vision: 'price_XXXXXXXXXX', // Replace with actual Stripe Price ID
        bundle_defense_offense: 'price_XXXXXXXXXX', // Replace with actual Stripe Price ID
        bundle_all: 'price_XXXXXXXXXX' // Replace with actual Stripe Price ID
    };

    /**
     * Create Stripe Checkout Session
     *
     * @param {string} priceId - The Stripe Price ID
     * @param {string} product - The product name (defense, offense, vision, etc.)
     */
    async function createCheckoutSession(priceId, product) {
        // Show loading state
        const button = event.target;
        const originalText = button.textContent;
        button.disabled = true;
        button.textContent = 'Loading...';

        try {
            // Get JWT token from localStorage (user must be logged in)
            const token = localStorage.getItem('auth_token');
            if (!token) {
                // Redirect to login if not authenticated
                window.location.href = '/login.html?redirect=' + encodeURIComponent(window.location.pathname);
                return;
            }

            // Call Defense API to create checkout session
            const response = await fetch(`${CONFIG.defenseApiUrl}/api/v1/stripe/create-checkout-session`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    price_id: priceId,
                    product: product,
                    success_url: CONFIG.successUrl,
                    cancel_url: CONFIG.cancelUrl
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to create checkout session');
            }

            const session = await response.json();

            // Redirect to Stripe Checkout
            const result = await stripe.redirectToCheckout({
                sessionId: session.id
            });

            if (result.error) {
                throw new Error(result.error.message);
            }

        } catch (error) {
            console.error('Checkout error:', error);
            showError(error.message || 'An error occurred. Please try again.');

            // Restore button state
            button.disabled = false;
            button.textContent = originalText;
        }
    }

    /**
     * Redirect to Stripe Customer Portal
     * Allows users to manage their existing subscription
     */
    async function redirectToCustomerPortal() {
        const button = event.target;
        const originalText = button.textContent;
        button.disabled = true;
        button.textContent = 'Loading...';

        try {
            // Get JWT token from localStorage
            const token = localStorage.getItem('auth_token');
            if (!token) {
                window.location.href = '/login.html?redirect=' + encodeURIComponent('/account.html');
                return;
            }

            // Call Defense API to create portal session
            const response = await fetch(`${CONFIG.defenseApiUrl}/api/v1/stripe/create-portal-session`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    return_url: window.location.origin + '/account.html'
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Failed to create portal session');
            }

            const portal = await response.json();

            // Redirect to Stripe Customer Portal
            window.location.href = portal.url;

        } catch (error) {
            console.error('Portal redirect error:', error);
            showError(error.message || 'An error occurred. Please try again.');

            // Restore button state
            button.disabled = false;
            button.textContent = originalText;
        }
    }

    /**
     * Get current user's subscription status
     *
     * @returns {Promise<Object>} Subscription status object
     */
    async function getSubscriptionStatus() {
        try {
            const token = localStorage.getItem('auth_token');
            if (!token) {
                return {
                    has_defense: false,
                    has_offense: false,
                    has_vision: false,
                    subscriptions: []
                };
            }

            const response = await fetch(`${CONFIG.defenseApiUrl}/api/v1/subscriptions/status`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                throw new Error('Failed to fetch subscription status');
            }

            return await response.json();

        } catch (error) {
            console.error('Failed to get subscription status:', error);
            return {
                has_defense: false,
                has_offense: false,
                has_vision: false,
                subscriptions: []
            };
        }
    }

    /**
     * Display error message to user
     *
     * @param {string} message - Error message to display
     */
    function showError(message) {
        // Create error notification
        const errorDiv = document.createElement('div');
        errorDiv.className = 'stripe-error-notification';
        errorDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #dc3545;
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10000;
            max-width: 300px;
            animation: slideIn 0.3s ease-in;
        `;
        errorDiv.innerHTML = `
            <strong>Error</strong><br>
            ${message}
        `;

        document.body.appendChild(errorDiv);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            errorDiv.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                document.body.removeChild(errorDiv);
            }, 300);
        }, 5000);
    }

    /**
     * Display success message to user
     *
     * @param {string} message - Success message to display
     */
    function showSuccess(message) {
        const successDiv = document.createElement('div');
        successDiv.className = 'stripe-success-notification';
        successDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #28a745;
            color: white;
            padding: 15px 20px;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10000;
            max-width: 300px;
            animation: slideIn 0.3s ease-in;
        `;
        successDiv.innerHTML = `
            <strong>Success</strong><br>
            ${message}
        `;

        document.body.appendChild(successDiv);

        setTimeout(() => {
            successDiv.style.animation = 'slideOut 0.3s ease-out';
            setTimeout(() => {
                document.body.removeChild(successDiv);
            }, 300);
        }, 5000);
    }

    /**
     * Initialize event listeners on page load
     */
    function initializeEventListeners() {
        // Subscribe buttons (data-product and data-price-id attributes)
        document.querySelectorAll('[data-stripe-subscribe]').forEach(button => {
            button.addEventListener('click', function(event) {
                event.preventDefault();
                const priceId = this.getAttribute('data-price-id');
                const product = this.getAttribute('data-product');
                createCheckoutSession(priceId, product);
            });
        });

        // Customer Portal buttons
        document.querySelectorAll('[data-stripe-portal]').forEach(button => {
            button.addEventListener('click', function(event) {
                event.preventDefault();
                redirectToCustomerPortal();
            });
        });
    }

    /**
     * Update pricing page UI based on user's subscription status
     */
    async function updatePricingPageUI() {
        // Only run on pricing page
        if (!window.location.pathname.includes('pricing')) return;

        const status = await getSubscriptionStatus();

        // Update button text for active subscriptions
        document.querySelectorAll('[data-stripe-subscribe]').forEach(button => {
            const product = button.getAttribute('data-product');

            if (product === 'defense' && status.has_defense) {
                button.textContent = 'Active Subscription';
                button.disabled = true;
                button.classList.add('subscription-active');
            } else if (product === 'offense' && status.has_offense) {
                button.textContent = 'Active Subscription';
                button.disabled = true;
                button.classList.add('subscription-active');
            } else if (product === 'vision' && status.has_vision) {
                button.textContent = 'Active Subscription';
                button.disabled = true;
                button.classList.add('subscription-active');
            }
        });
    }

    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }

        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(100%);
                opacity: 0;
            }
        }

        .subscription-active {
            background-color: #6c757d !important;
            cursor: not-allowed !important;
        }
    `;
    document.head.appendChild(style);

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', function() {
            initializeEventListeners();
            updatePricingPageUI();
        });
    } else {
        initializeEventListeners();
        updatePricingPageUI();
    }

    // Export functions for global access if needed
    window.AiVRICStripe = {
        createCheckoutSession: createCheckoutSession,
        redirectToCustomerPortal: redirectToCustomerPortal,
        getSubscriptionStatus: getSubscriptionStatus,
        PRICE_IDS: PRICE_IDS
    };

})();
