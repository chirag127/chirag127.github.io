/**
 * Part 4: Communication - Feedback / Surveys
 * @module config/communication/feedback_surveys
 */
export const feedback_surveys = {
    // Typeform
    // Feature: Highly engaging conversational forms
    // Free Limit: 10 responses/month
    typeform: { formId: '', enabled: false },

    // Google Forms
    // Feature: Simple, reliable, unlimited
    // Free Limit: Unlimited responses
    googleForms: { formUrl: '', enabled: false },

    // SurveyMonkey
    // Feature: Professional survey tools
    // Free Limit: 40 responses/survey (Basic Plan)
    surveyMonkey: { surveyId: '', enabled: false }
};
