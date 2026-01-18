/**
 * Part 3: Communication - Live Chat
 * Real-time customer support and engagement widgets
 * ENABLED for user support (reputation building)
 * @module config/communication/live_chat
 */

export const live_chat = {
    // ============================================================================
    // TAWK.TO - 100% Free Forever Live Chat
    // ============================================================================
    // What it does:
    // - Completely free live chat widget (no paid plans!)
    // - UNLIMITED agents (team members)
    // - Real-time visitor monitoring
    // - Chat history and transcripts
    // - File sharing in chats
    // - Pre-chat forms and offline messages
    // - Mobile apps (iOS/Android) for agents
    // - Customizable widget appearance
    // - Visitor tracking and analytics
    // - Triggers and automated messages
    //
    // What it doesn't do:
    // - No video/voice calls
    // - Basic analytics compared to enterprise tools
    // - Limited integrations compared to paid tools
    //
    // Free Tier Limits:
    // - 100% FREE FOREVER (no paid plans exist!)
    // - UNLIMITED agents
    // - UNLIMITED chats
    // - UNLIMITED chat history
    // - All features included
    //
    // Best for: Any website needing customer support, small businesses, startups
    // Website: https://www.tawk.to
    // Note: Best free live chat - truly unlimited with no catches
    tawkto: {
        source: 'https://embed.tawk.to/6968e3ea8783b31983eb190b/1jf0rkjhp',
        enabled: true
    },

    // ============================================================================
    // CRISP - Modern Live Chat Platform
    // ============================================================================
    // What it does:
    // - Beautiful, modern chat widget
    // - Shared inbox for team collaboration
    // - Chatbot builder (basic automation)
    // - Knowledge base integration
    // - Email and social media integration
    // - Mobile apps for agents
    // - Visitor tracking
    // - Chat triggers and targeting
    //
    // What it doesn't do:
    // - Limited to 2 team members on free tier
    // - No advanced chatbot features
    // - No video calls
    // - Limited integrations on free tier
    //
    // Free Tier Limits (Basic Plan):
    // - 2 seats (team members)
    // - Unlimited chat history
    // - Unlimited conversations
    // - Basic chatbot
    // - Mobile apps
    // - Crisp branding
    //
    // Best for: Small teams, modern UI preference, basic automation needs
    // Website: https://crisp.chat
    // Note: Good free tier but limited to 2 agents
    crisp: { websiteId: '', enabled: false },

    // ============================================================================
    // TIDIO - Chat + Chatbots Combo
    // ============================================================================
    // What it does:
    // - Live chat with built-in chatbot builder
    // - Email integration (manage emails in same inbox)
    // - Pre-made chatbot templates
    // - Visitor tracking and analytics
    // - Mobile apps for agents
    // - Customizable widget
    // - Automated responses
    //
    // What it doesn't do:
    // - Limited conversations on free tier (50/month)
    // - Limited chatbot triggers
    // - No advanced automation
    // - Limited integrations
    //
    // Free Tier Limits (Free Plan):
    // - 50 conversations per month (limited!)
    // - 3 chatbot triggers
    // - Unlimited chat history (7 days visible)
    // - 1 operator seat
    // - Email integration
    // - Tidio branding
    //
    // Best for: Small sites with light traffic, chatbot experimentation
    // Website: https://www.tidio.com
    // Note: Limited conversations - Tawk.to is better for unlimited needs
    tidio: { publicKey: '', enabled: false },

    // ============================================================================
    // DRIFT - B2B Conversational Marketing (LIMITED FREE)
    // ============================================================================
    // What it does:
    // - Conversational marketing platform
    // - Lead qualification and routing
    // - Meeting scheduling integration
    // - Playbooks for sales automation
    // - Email capture and lead generation
    // - CRM integrations
    //
    // What it doesn't do:
    // - Very limited free tier (mostly paid)
    // - No live chat in free tier (only chatbots)
    // - Requires paid plan for most features
    // - Enterprise pricing
    //
    // Free Tier Limits (Free Plan):
    // - Very limited (mostly trial)
    // - Basic chatbot only
    // - No live chat support
    // - Limited to 100 contacts
    //
    // Best for: B2B companies with budget for paid plans
    // Website: https://www.drift.com
    // Note: Not recommended for free tier - very limited
    drift: { embedId: '', enabled: false },

    // ============================================================================
    // INTERCOM - Enterprise Customer Platform (NO FREE TIER)
    // ============================================================================
    // What it does:
    // - Full customer engagement platform
    // - Live chat, email, and in-app messaging
    // - Advanced automation and workflows
    // - Product tours and onboarding
    // - Help center and knowledge base
    // - Advanced analytics and reporting
    // - CRM and sales features
    //
    // What it doesn't do:
    // - NO FREE TIER (trial only)
    // - Expensive (starts at $39/month minimum)
    // - Overkill for small businesses
    //
    // Free Tier Limits:
    // - NO FREE TIER
    // - 14-day trial only
    // - Paid plans start at $39/seat/month
    //
    // Best for: Enterprise companies with large budgets
    // Website: https://www.intercom.com
    // Note: NOT RECOMMENDED - no free tier, use Tawk.to instead
    intercom: { appId: '', enabled: false }
};

export const live_chat_priority = ['tawk', 'crisp', 'tidio', 'drift'];

// Made with Bob
