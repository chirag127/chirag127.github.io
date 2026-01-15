/**
 * Centralized Monetization - Ads, Donations, Affiliate
 * UPDATE THIS FILE ONCE → CHANGES APPLY EVERYWHERE
 */

(function() {
  'use strict';

  // =========================================================================
  // CONFIGURATION
  // =========================================================================

  const CONFIG = {
    // A-Ads (Crypto Ad Network)
    aads: {
      unitId: '2424216',
      enabled: true
    },

    // Buy Me a Coffee
    buymeacoffee: {
      username: 'chirag127',
      color: '#6366f1', // Indigo to match theme
      message: 'Thank you for using this tool!',
      enabled: true
    },

    // GitHub Sponsors
    githubSponsors: {
      username: 'chirag127',
      enabled: true
    }
  };

  // =========================================================================
  // INJECT A-ADS BANNER (Footer)
  // =========================================================================

  function injectAAdsBanner() {
    if (!CONFIG.aads.enabled) return;
    if (document.getElementById('centralized-aads-banner')) return;

    const banner = document.createElement('div');
    banner.id = 'centralized-aads-banner';
    // Glassmorphism, blurred, dark theme
    banner.style.cssText = `
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 9998;
      background: rgba(3, 7, 18, 0.85); /* Matches new dark theme */
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      padding: 10px;
      text-align: center;
      border-top: 1px solid rgba(255,255,255,0.08);
      box-shadow: 0 -4px 20px rgba(0,0,0,0.4);
      transition: transform 0.3s ease;
    `;

    const iframe = document.createElement('iframe');
    iframe.setAttribute('data-aa', CONFIG.aads.unitId);
    iframe.src = `//acceptable.a-ads.com/${CONFIG.aads.unitId}/?size=728x90`;
    iframe.style.cssText = `
      border: 0;
      padding: 0;
      width: 100%;
      max-width: 728px;
      height: 90px;
      display: block;
      margin: 0 auto;
      border-radius: 8px; /* Slight roundness */
      background: rgba(255,255,255,0.02);
    `;

    banner.appendChild(iframe);
    document.body.appendChild(banner);

    // Padding for content
    document.body.style.paddingBottom = '110px';
  }

  // =========================================================================
  // INJECT BUY ME A COFFEE WIDGET
  // =========================================================================

  function injectBuyMeACoffee() {
    if (!CONFIG.buymeacoffee.enabled) return;
    if (document.querySelector('script[data-name="BMC-Widget"]')) return;

    const script = document.createElement('script');
    script.setAttribute('data-name', 'BMC-Widget');
    script.setAttribute('data-cfasync', 'false');
    script.src = 'https://cdnjs.buymeacoffee.com/1.0.0/widget.prod.min.js';
    script.setAttribute('data-id', CONFIG.buymeacoffee.username);
    script.setAttribute('data-description', 'Support me!');
    script.setAttribute('data-message', CONFIG.buymeacoffee.message);
    script.setAttribute('data-color', CONFIG.buymeacoffee.color);
    script.setAttribute('data-position', 'Right');
    script.setAttribute('data-x_margin', '18');
    script.setAttribute('data-y_margin', '125'); // Moved up to avoid banner

    document.body.appendChild(script);
  }

  // =========================================================================
  // INJECT SUPPORT LINKS (Mobile/Custom)
  // =========================================================================

  function createSupportSection() {
    const supportDiv = document.createElement('div');
    supportDiv.id = 'centralized-support';
    supportDiv.innerHTML = `
      <style>
        #centralized-support-btn {
          position: fixed;
          bottom: 125px; /* Above banner */
          left: 20px;
          z-index: 9997;
          background: linear-gradient(135deg, #FF6B6B, #FF8E53);
          color: white;
          border: none;
          border-radius: 50px;
          padding: 12px 20px;
          font-weight: 600;
          cursor: pointer;
          box-shadow: 0 4px 15px rgba(255,107,107,0.3);
          transition: all 0.3s ease;
          font-family: system-ui, sans-serif;
          display: flex; align-items: center; gap: 8px;
        }
        #centralized-support-btn:hover {
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(255,107,107,0.4);
        }
        #support-modal {
          display: none;
          position: fixed;
          bottom: 180px;
          left: 20px;
          z-index: 9999;
          background: rgba(30, 41, 59, 0.95);
          backdrop-filter: blur(12px);
          border-radius: 16px;
          padding: 20px;
          min-width: 280px;
          box-shadow: 0 20px 50px rgba(0,0,0,0.5);
          border: 1px solid rgba(255,255,255,0.1);
          animation: slideIn 0.2s ease-out;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        #support-modal.show { display: block; }
        #support-modal h3 {
          margin: 0 0 15px 0;
          color: white;
          font-size: 1.1rem;
          font-family: system-ui, sans-serif;
        }
        .support-link {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px 15px;
          margin: 8px 0;
          background: rgba(255,255,255,0.05);
          border-radius: 10px;
          color: #e2e8f0;
          text-decoration: none;
          transition: all 0.2s;
          font-family: system-ui, sans-serif;
          font-size: 0.95rem;
        }
        .support-link:hover { background: rgba(255,255,255,0.1); color: white; transform: translateX(5px); }
      </style>

      <button id="centralized-support-btn"><span>❤️</span> Support</button>

      <div id="support-modal">
        <h3>Support This Project</h3>
        <a class="support-link" href="https://buymeacoffee.com/${CONFIG.buymeacoffee.username}" target="_blank">
          <span>☕</span> Buy Me a Coffee
        </a>
        <a class="support-link" href="https://github.com/sponsors/${CONFIG.githubSponsors.username}" target="_blank">
          <span>💖</span> GitHub Sponsors
        </a>
        <a class="support-link" href="https://github.com/${CONFIG.githubSponsors.username}" target="_blank">
          <span>⭐</span> Star on GitHub
        </a>
      </div>
    `;

    document.body.appendChild(supportDiv);

    // Toggle modal
    const btn = document.getElementById('centralized-support-btn');
    const modal = document.getElementById('support-modal');
    btn.addEventListener('click', (e) => {
        e.stopPropagation();
        modal.classList.toggle('show');
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!supportDiv.contains(e.target)) {
        modal.classList.remove('show');
      }
    });
  }

  function init() {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', inject);
    } else {
      inject();
    }
  }

  function inject() {
    injectAAdsBanner();
    injectBuyMeACoffee();
    createSupportSection();
  }

  init();
})();
