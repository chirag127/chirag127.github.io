/**
 * Mailchimp Email Capture Integration
 */
export const mailchimp = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.formAction || this.loaded) return;

        this.formAction = config.formAction;
        this.loaded = true;
        console.log('[Mailchimp] Ready');
    },

    render(containerId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <form action="${this.formAction}" method="post" target="_blank" class="mailchimp-form">
                <input type="email" name="EMAIL" placeholder="${options.placeholder || 'Enter your email'}" required
                       style="padding:12px 16px;border:1px solid #ddd;border-radius:4px;font-size:16px;width:100%;max-width:300px;">
                <button type="submit"
                        style="padding:12px 24px;background:${options.buttonColor || '#007bff'};color:#fff;border:none;border-radius:4px;cursor:pointer;margin-top:8px;">
                    ${options.buttonText || 'Subscribe'}
                </button>
            </form>
        `;
    },

    createPopup(options = {}) {
        const popup = document.createElement('div');
        popup.id = 'mailchimp-popup';
        popup.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;';
        popup.innerHTML = `
            <div style="background:#fff;padding:32px;border-radius:8px;max-width:400px;text-align:center;">
                <h3 style="margin-bottom:16px;">${options.title || 'Subscribe to our newsletter'}</h3>
                <div id="mailchimp-popup-form"></div>
                <button onclick="this.closest('#mailchimp-popup').remove()" style="margin-top:16px;background:none;border:none;cursor:pointer;color:#666;">No thanks</button>
            </div>
        `;
        document.body.appendChild(popup);
        this.render('mailchimp-popup-form', options);
    }
};
