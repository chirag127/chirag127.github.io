/**
 * Centralized Monetization - Ads, Donations, Affiliate
 *
 * Include in ALL projects:
 * <script src="https://chirag127.github.io/shared/monetization.js" defer></script>
 *
 * UPDATE THIS FILE ONCE → CHANGES APPLY EVERYWHERE
 */

(function() {
  'use strict';

  // =========================================================================
  // CONFIGURATION - UPDATE ONLY HERE
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
      color: '#5F7FFF',
      message: 'Thank you for using this tool!',
      enabled: true
    },

    // GitHub Sponsors
    githubSponsors: {
      username: 'chirag127',
      enabled: true
    },

    // Amazon Affiliate
    amazon: {
      storeId: 'chirag127-21',
      enabled: false // Enable when needed
    }
  };

  // =========================================================================
  // INJECT A-ADS BANNER (Footer)
  // =========================================================================

  function injectAAdsBanner() {
    if (!CONFIG.aads.enabled) return;

    // Check if already exists
    if (document.getElementById('centralized-aads-banner')) return;

    const banner = document.createElement('div');
    banner.id = 'centralized-aads-banner';
    banner.style.cssText = `
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 9998;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(8px);
      padding: 8px;
      text-align: center;
      border-top: 1px solid rgba(255,255,255,0.1);
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
    `;

    banner.appendChild(iframe);
    document.body.appendChild(banner);

    // Add padding to body to prevent content overlap
    document.body.style.paddingBottom = '110px';
  }

  // =========================================================================
  // INJECT BUY ME A COFFEE WIDGET
  // =========================================================================

  function injectBuyMeACoffee() {
    if (!CONFIG.buymeacoffee.enabled) return;

    // Check if already exists
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
    script.setAttribute('data-y_margin', '108');

    document.body.appendChild(script);
  }

  // =========================================================================
  // INJECT SUPPORT LINKS
  // =========================================================================

  function createSupportSection() {
    const supportDiv = document.createElement('div');
    supportDiv.id = 'centralized-support';
    supportDiv.innerHTML = `
      <style>
        #centralized-support-btn {
          position: fixed;
          bottom: 120px;
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
          background: #1e293b;
          border-radius: 16px;
          padding: 20px;
          min-width: 280px;
          box-shadow: 0 20px 50px rgba(0,0,0,0.5);
          border: 1px solid rgba(255,255,255,0.1);
        }
        #support-modal.show { display: block; }
        #support-modal h3 {
          margin: 0 0 15px 0;
          color: white;
          font-size: 18px;
        }
        .support-link {
          display: flex;
          align-items: center;
          gap: 10px;
          padding: 10px 15px;
          margin: 8px 0;
          background: rgba(255,255,255,0.05);
          border-radius: 10px;
          color: white;
          text-decoration: none;
          transition: background 0.2s;
        }
        .support-link:hover { background: rgba(255,255,255,0.1); }
        .support-link span { font-size: 20px; }
      </style>

      <button id="centralized-support-btn">❤️ Support</button>

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
    btn.addEventListener('click', () => modal.classList.toggle('show'));

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!supportDiv.contains(e.target)) {
        modal.classList.remove('show');
      }
    });
  }

  // =========================================================================
  // INITIALIZATION
  // =========================================================================

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
    console.log('[Monetization] Injected from central hub');
  }

  init();
})();
