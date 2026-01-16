/**
 * Monetization Manager
 * Renders support widgets and banners based on shared/profile.json config.
 */

(async function() {
    console.log("💰 Initializing Monetization...");

    const CONFIG_URL = 'https://chirag127.github.io/shared/profile.json';

    try {
        const response = await fetch(CONFIG_URL);
        const profile = await response.json();
        const monetization = profile.config?.monetization || {};

        if (monetization.aads?.enabled) injectAAdsBanner(monetization.aads);
        injectSupportWidget(monetization);

    } catch (e) {
        console.error("Monetization Error:", e);
    }

    // ===========================================
    // 1. A-Ads Banner
    // ===========================================
    function injectAAdsBanner(config) {
        if (!config.unit_id) return;

        const banner = document.createElement('div');
        banner.id = 'aads-banner-container';
        banner.style.cssText = `
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            z-index: 9998;
            background: rgba(3, 7, 18, 0.9);
            backdrop-filter: blur(12px);
            border-top: 1px solid rgba(255,255,255,0.08);
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 10px;
            min-height: 60px;
        `;

        const iframe = document.createElement('iframe');
        iframe.src = `//ad.a-ads.com/${config.unit_id}?size=728x90`;
        iframe.style.cssText = "width:728px; height:90px; border:0; overflow:hidden;";
        // Mobile check
        if (window.innerWidth < 768) {
             iframe.src = `//ad.a-ads.com/${config.unit_id}?size=320x50`;
             iframe.style.width = "320px";
             iframe.style.height = "50px";
        }

        const closeBtn = document.createElement('button');
        closeBtn.innerHTML = '×';
        closeBtn.style.cssText = `
            position: absolute;
            top: 5px;
            right: 10px;
            background: none;
            border: none;
            color: #ccc;
            font-size: 24px;
            cursor: pointer;
        `;
        closeBtn.onclick = () => banner.remove();

        banner.appendChild(iframe);
        banner.appendChild(closeBtn);
        document.body.appendChild(banner);
    }

    // ===========================================
    // 2. Support Widget (Floating)
    // ===========================================
    function injectSupportWidget(config) {
        // Create Floating Button
        const btn = document.createElement('button');
        btn.innerHTML = '💖 Support';
        btn.id = 'support-floating-btn';
        btn.style.cssText = `
            position: fixed;
            bottom: 100px; /* Above ads */
            left: 20px;
            z-index: 9999;
            background: linear-gradient(135deg, #ec4899, #8b5cf6);
            color: white;
            border: none;
            border-radius: 50px;
            padding: 12px 24px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
            cursor: pointer;
            transition: transform 0.2s;
            font-family: var(--font-body, system-ui);
        `;
        btn.onmouseover = () => btn.style.transform = 'scale(1.05)';
        btn.onmouseout = () => btn.style.transform = 'scale(1)';

        // Create Modal
        const modal = document.createElement('div');
        modal.id = 'support-modal';
        modal.style.cssText = `
            display: none;
            position: fixed;
            bottom: 160px;
            left: 20px;
            z-index: 9999;
            background: rgba(30, 41, 59, 0.95);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 20px;
            width: 300px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.5);
            color: white;
            font-family: var(--font-body, system-ui);
        `;

        let linksHtml = '';

        if (config.buymeacoffee?.enabled) {
            linksHtml += `
                <a href="https://buymeacoffee.com/${config.buymeacoffee.username}" target="_blank" style="display:flex;align-items:center;gap:10px;background:#FFDD00;color:black;text-decoration:none;padding:10px;border-radius:8px;margin-bottom:10px;font-weight:600;">
                    ☕ Buy me a Coffee
                </a>`;
        }
        if (config.github_sponsors?.enabled) {
             linksHtml += `
                <a href="https://github.com/sponsors/${config.github_sponsors.username}" target="_blank" style="display:flex;align-items:center;gap:10px;background:#24292e;color:white;text-decoration:none;padding:10px;border-radius:8px;margin-bottom:10px;font-weight:600;border:1px solid #444;">
                    💖 GitHub Sponsors
                </a>`;
        }
        if (config.crypto?.enabled) {
            linksHtml += `<div style="margin-top:10px;font-size:0.85rem;color:#ccc;">
                <p style="margin-bottom:4px"><strong>BTC:</strong> <span style="font-family:monospace;font-size:0.8rem;opacity:0.8">${config.crypto.btc.substring(0,12)}...</span></p>
                <p><strong>SOL:</strong> <span style="font-family:monospace;font-size:0.8rem;opacity:0.8">${config.crypto.sol.substring(0,12)}...</span></p>
            </div>`;
        }

        modal.innerHTML = `
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;">
                <h3 style="margin:0;font-size:1.1rem;">Support Development</h3>
                <span id="close-support" style="cursor:pointer;opacity:0.7;">×</span>
            </div>
            ${linksHtml}
        `;

        // Toggle
        btn.onclick = () => {
             modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
        };

        document.body.appendChild(btn);
        document.body.appendChild(modal);

        modal.querySelector('#close-support').onclick = () => {
            modal.style.display = 'none';
        };
    }

})();
