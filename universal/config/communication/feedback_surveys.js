/**
 * Part 4: Communication - Feedback / Surveys
 * Collect user feedback and conduct surveys
 * @module config/communication/feedback_surveys
 */

export const feedback_surveys = {
    // ============================================================================
    // TYPEFORM - Conversational Forms & Surveys
    // ============================================================================
    // What it does:
    // - Beautiful, conversational form experience (one question at a time)
    // - Logic jumps and conditional questions
    // - Multiple question types (multiple choice, rating, file upload)
    // - Custom branding and themes
    // - Integration with 500+ apps (Zapier, Slack, etc.)
    // - Real-time response notifications
    // - Basic analytics and reporting
    //
    // What it doesn't do:
    // - Very limited free tier (only 10 responses/month)
    // - No advanced analytics in free tier
    // - No custom domains
    // - No remove Typeform branding
    //
    // Free Tier Limits (Basic Plan):
    // - 10 responses per month (very limited!)
    // - Unlimited forms
    // - 10 questions per form
    // - Basic logic jumps
    // - Typeform branding
    //
    // Best for: High-engagement surveys, lead generation, customer feedback
    // Website: https://www.typeform.com
    // Note: Beautiful UX but very restrictive free tier - consider Google Forms for more responses
    typeform: { formId: '', enabled: false },

    // ============================================================================
    // GOOGLE FORMS - Unlimited Free Surveys
    // ============================================================================
    // What it does:
    // - Create unlimited surveys with unlimited questions
    // - UNLIMITED responses (no cap!)
    // - Automatic data collection in Google Sheets
    // - Real-time response charts and summaries
    // - Email notifications for new responses
    // - File upload support
    // - Quiz mode with auto-grading
    // - Form logic and section branching
    //
    // What it doesn't do:
    // - Basic design (Google branding)
    // - No advanced customization
    // - Limited question types compared to paid tools
    // - No advanced analytics
    //
    // Free Tier Limits:
    // - UNLIMITED responses (truly unlimited!)
    // - UNLIMITED forms
    // - UNLIMITED questions per form
    // - Storage limited by Google Drive (15GB free)
    // - All features free forever
    //
    // Best for: Any survey needs, data collection, event registration, quizzes
    // Website: https://forms.google.com
    // Note: Best free option - no response limits, perfect for most use cases
    googleForms: { formUrl: '', enabled: false },

    // ============================================================================
    // SURVEYMONKEY - Professional Survey Platform
    // ============================================================================
    // What it does:
    // - Professional survey creation with templates
    // - Advanced question types and logic
    // - Survey analytics and reporting
    // - Data export capabilities
    // - Mobile-optimized surveys
    // - Email invitations
    //
    // What it doesn't do:
    // - Limited responses on free tier
    // - No advanced features (logic, exports) in free tier
    // - No custom branding
    // - No data export in free tier
    //
    // SurveyMonkey
    // Feature: Deep analytics and professional templates
    // Free Limit: 25 viewable responses per survey
    surveymonkey: { surveyUrl: '', enabled: false }
};

export const feedback_surveys_priority = ['googleForms', 'typeform', 'surveymonkey'];

// Made with Bob
