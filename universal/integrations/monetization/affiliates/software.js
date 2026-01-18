/**
 * Software & Tools Affiliate Integration
 * Specifically for direct utility tool upsells (e.g. Adobe, Nitro)
 * @module integrations/monetization/affiliates/software
 */
export const software = {
    loaded: false,
    config: {},

    init(config) {
        if (!config || !config.enabled || this.loaded) return;
        this.config = config;
        this.loaded = true;

        // Auto-inject upsells when DOM is ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.injectUpsell());
        } else {
            this.injectUpsell();
        }
    },

    /**
     * Injects relevant upsells based on the current page context
     */
    injectUpsell() {
        const title = (document.title || '').toLowerCase();
        const main = document.querySelector('main');
        if (!main) return;

        // Determine tool category
        let toolType = '';
        if (title.includes('pdf')) toolType = 'pdf';
        else if (title.includes('video') || title.includes('movie')) toolType = 'video';
        else if (title.includes('image') || title.includes('photo') || title.includes('compress')) toolType = 'image';
        else if (title.includes('ip') || title.includes('dns') || title.includes('whois')) toolType = 'privacy';

        const upsells = {
            pdf: [
                { id: 'adobe', text: 'Need to edit PDF text? Try Adobe Acrobat' },
                { id: 'nitro', text: 'Professional PDF Editor for Desktop' }
            ],
            video: [
                { id: 'adobe', text: 'Edit videos like a pro with Premiere' }
            ],
            image: [
                { id: 'adobe', text: 'Free Trial: Adobe Photoshop & Creative Cloud' }
            ],
            privacy: [
                { id: 'nordvpn', text: 'Secure your IP with NordVPN (Special Offer)' }
            ]
        };

        const relevant = upsells[toolType];
        if (!relevant) return;

        // Check if container already exists
        if (document.getElementById('apex-upsell-banner')) return;

        const container = document.createElement('div');
        container.id = 'apex-upsell-banner';
        container.className = 'apex-card'; // Use existing design system class
        container.style = 'margin: 30px auto; max-width: 800px; padding: 20px; border-radius: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); text-align: center; backdrop-filter: blur(10px);';

        const header = document.createElement('p');
        header.innerText = '💡 Recommended for Power Users';
        header.style = 'font-size: 12px; color: rgba(255,255,255,0.5); margin-bottom: 12px; text-transform: uppercase; letter-spacing: 1px;';
        container.appendChild(header);

        let addedCount = 0;
        relevant.forEach(item => {
            const program = this.config[item.id];
            if (program && program.enabled) {
                const btn = document.createElement('a');
                // Use a proper tracking link if ID exists, else fallback to baseUrl
                const link = program.trackingId ? `${program.baseUrl}?affid=${program.trackingId}` : program.baseUrl;

                btn.href = link;
                btn.target = '_blank';
                btn.rel = 'nofollow noopener';
                btn.innerText = item.text;
                btn.className = 'apex-btn'; // Use existing design system class if available or style directly
                btn.style = 'display: inline-block; margin: 8px; padding: 12px 24px; border-radius: 8px; background: linear-gradient(135deg, #007bff 0%, #0056b3 100%); color: white; text-decoration: none; font-weight: 600; font-size: 14px; transition: transform 0.2s;';

                btn.onmouseover = () => btn.style.transform = 'scale(1.02)';
                btn.onmouseout = () => btn.style.transform = 'scale(1)';

                container.appendChild(btn);
                addedCount++;
            }
        });

        if (addedCount > 0) {
            // Append at the end of the main content
            main.appendChild(container);
            console.log(`[SoftwareUpsell] Injected ${addedCount} offers for category: ${toolType}`);
        }
    }
};
