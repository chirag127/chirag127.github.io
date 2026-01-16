/**
 * Monetization Module
 * Handles ads and affiliate integrations
 */
(function() {
  // Placeholder for ad integrations
  // Add your ad network scripts here

  // Example: Google AdSense
  // const ADS_CLIENT = 'ca-pub-XXXXXXXXXX';

  console.log('[Ads] Monetization module loaded');

  // Buy Me A Coffee floating widget
  window.bmcWidget = {
    coffeeUrl: 'https://buymeacoffee.com/chirag127',
    loaded: false
  };

  // Create floating donate button
  function createDonateButton() {
    const btn = document.createElement('a');
    btn.href = 'https://buymeacoffee.com/chirag127';
    btn.target = '_blank';
    btn.innerHTML = '☕';
    btn.style.cssText = `
      position: fixed;
      bottom: 80px;
      right: 20px;
      width: 50px;
      height: 50px;
      background: linear-gradient(135deg, #6366f1, #a855f7);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      text-decoration: none;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
      z-index: 9999;
      transition: transform 0.3s, box-shadow 0.3s;
    `;
    btn.onmouseenter = () => btn.style.transform = 'scale(1.1)';
    btn.onmouseleave = () => btn.style.transform = 'scale(1)';
    document.body.appendChild(btn);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createDonateButton);
  } else {
    createDonateButton();
  }
})();
