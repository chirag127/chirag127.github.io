/**
 * Master Integrations Loader
 *
 * Loads ALL integrations from profile.json config:
 * - Analytics (GA4, Clarity, Yandex, PostHog, etc.)
 * - Monetization (A-Ads, BMC, Ko-fi, Crypto)
 * - Chat (Tawk.to, Crisp)
 * - Bug Tracking (Sentry, LogRocket)
 * - Utilities (Instant.page, UserWay)
 *
 * Usage: <script src="https://chirag127.github.io/shared/integrations.js" defer></script>
 */

(async function() {
  'use strict';

  const CONFIG_URL = 'https://chirag127.github.io/shared/profile.json';
  const DEBUG = false;

  function log(...args) {
    if (DEBUG) console.log('[Integrations]', ...args);
  }

  try {
    const res = await fetch(CONFIG_URL);
    const profile = await res.json();
    const cfg = profile.config || {};

    log('Config loaded', cfg);

    // =========================================================================
    // 1. ANALYTICS
    // =========================================================================

    // Google Analytics 4
    if (cfg.analytics?.ga4?.enabled && cfg.analytics.ga4.measurement_id) {
      const id = cfg.analytics.ga4.measurement_id;
      const script = document.createElement('script');
      script.async = true;
      script.src = `https://www.googletagmanager.com/gtag/js?id=${id}`;
      document.head.appendChild(script);

      window.dataLayer = window.dataLayer || [];
      window.gtag = function() { dataLayer.push(arguments); };
      gtag('js', new Date());
      gtag('config', id, { send_page_view: true });
      log('GA4 loaded:', id);
    }

    // Microsoft Clarity
    if (cfg.analytics?.clarity?.enabled && cfg.analytics.clarity.project_id) {
      const id = cfg.analytics.clarity.project_id;
      (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      })(window, document, "clarity", "script", id);
      log('Clarity loaded:', id);
    }

    // Yandex Metrica
    if (cfg.analytics?.yandex?.enabled && cfg.analytics.yandex.tag_id) {
      const id = cfg.analytics.yandex.tag_id;
      (function(m,e,t,r,i,k,a){
        m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();
        k=e.createElement(t);a=e.getElementsByTagName(t)[0];
        k.async=1;k.src=r;a.parentNode.insertBefore(k,a);
      })(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
      ym(id, "init", { clickmap:true, trackLinks:true, accurateTrackBounce:true, webvisor:true });
      log('Yandex loaded:', id);
    }

    // PostHog
    if (cfg.analytics?.posthog?.enabled && cfg.analytics.posthog.api_key) {
      const key = cfg.analytics.posthog.api_key;
      const host = cfg.analytics.posthog.host || 'https://us.posthog.com';
      !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys onSessionId".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
      posthog.init(key, { api_host: host });
      log('PostHog loaded');
    }

    // Cloudflare Web Analytics
    if (cfg.analytics?.cloudflare?.enabled && cfg.analytics.cloudflare.beacon_token) {
      const token = cfg.analytics.cloudflare.beacon_token;
      const script = document.createElement('script');
      script.defer = true;
      script.src = 'https://static.cloudflareinsights.com/beacon.min.js';
      script.setAttribute('data-cf-beacon', JSON.stringify({ token }));
      document.head.appendChild(script);
      log('Cloudflare Analytics loaded');
    }

    // Umami
    if (cfg.analytics?.umami?.enabled && cfg.analytics.umami.website_id) {
      const script = document.createElement('script');
      script.async = true;
      script.src = (cfg.analytics.umami.host || 'https://cloud.umami.is') + '/script.js';
      script.setAttribute('data-website-id', cfg.analytics.umami.website_id);
      document.head.appendChild(script);
      log('Umami loaded');
    }

    // GoatCounter
    if (cfg.analytics?.goatcounter?.enabled && cfg.analytics.goatcounter.code) {
      const code = cfg.analytics.goatcounter.code;
      const script = document.createElement('script');
      script.async = true;
      script.src = `https://${code}.goatcounter.com/count.js`;
      script.setAttribute('data-goatcounter', `https://${code}.goatcounter.com/count`);
      document.head.appendChild(script);
      log('GoatCounter loaded');
    }

    // Heap
    if (cfg.analytics?.heap?.enabled && cfg.analytics.heap.app_id) {
      window.heap=window.heap||[],heap.load=function(e,t){window.heap.appid=e,window.heap.config=t=t||{};var r=document.createElement("script");r.type="text/javascript",r.async=!0,r.src="https://cdn.heapanalytics.com/js/heap-"+e+".js";var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(r,a);for(var n=function(e){return function(){heap.push([e].concat(Array.prototype.slice.call(arguments,0)))}},p=["addEventProperties","addUserProperties","clearEventProperties","identify","resetIdentity","removeEventProperty","setEventProperties","track","unsetEventProperty"],o=0;o<p.length;o++)heap[p[o]]=n(p[o])};
      heap.load(cfg.analytics.heap.app_id);
      log('Heap loaded');
    }

    // =========================================================================
    // 2. BUG TRACKING
    // =========================================================================

    // Sentry
    if (cfg.bug_tracking?.sentry?.enabled && cfg.bug_tracking.sentry.dsn) {
      const script = document.createElement('script');
      script.src = 'https://browser.sentry-cdn.com/7.100.0/bundle.tracing.min.js';
      script.crossOrigin = 'anonymous';
      script.onload = () => {
        Sentry.init({ dsn: cfg.bug_tracking.sentry.dsn, tracesSampleRate: 0.1 });
        log('Sentry loaded');
      };
      document.head.appendChild(script);
    }

    // LogRocket
    if (cfg.bug_tracking?.logrocket?.enabled && cfg.bug_tracking.logrocket.app_id) {
      const script = document.createElement('script');
      script.src = 'https://cdn.lr-ingest.com/LogRocket.min.js';
      script.crossOrigin = 'anonymous';
      script.onload = () => {
        LogRocket.init(cfg.bug_tracking.logrocket.app_id);
        log('LogRocket loaded');
      };
      document.head.appendChild(script);
    }

    // =========================================================================
    // 3. CHAT WIDGETS
    // =========================================================================

    // Tawk.to
    if (cfg.chat?.tawk?.enabled && cfg.chat.tawk.property_id && cfg.chat.tawk.widget_id) {
      var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
      const s1=document.createElement("script");
      s1.async=true;
      s1.src=`https://embed.tawk.to/${cfg.chat.tawk.property_id}/${cfg.chat.tawk.widget_id}`;
      s1.charset='UTF-8';
      s1.setAttribute('crossorigin','*');
      document.head.appendChild(s1);
      log('Tawk.to loaded');
    }

    // Crisp
    if (cfg.chat?.crisp?.enabled && cfg.chat.crisp.website_id) {
      window.$crisp=[];window.CRISP_WEBSITE_ID=cfg.chat.crisp.website_id;
      const d=document;const s=d.createElement("script");
      s.src="https://client.crisp.chat/l.js";s.async=1;
      d.getElementsByTagName("head")[0].appendChild(s);
      log('Crisp loaded');
    }

    // =========================================================================
    // 4. UTILITIES
    // =========================================================================

    // Instant.page (Preloading)
    if (cfg.utilities?.instant_page?.enabled) {
      const script = document.createElement('script');
      script.src = 'https://instant.page/5.2.0';
      script.type = 'module';
      script.integrity = 'sha384-jnZyxPjiipYXnSU0ber72X25lNzOVa3ubv/aQZqRv0VhR6yMXpHnzzLl1J8Qq3hl';
      document.body.appendChild(script);
      log('Instant.page loaded');
    }

    // UserWay (Accessibility)
    if (cfg.utilities?.userway?.enabled && cfg.utilities.userway.account_id) {
      const script = document.createElement('script');
      script.src = 'https://cdn.userway.org/widget.js';
      script.setAttribute('data-account', cfg.utilities.userway.account_id);
      document.body.appendChild(script);
      log('UserWay loaded');
    }

    // =========================================================================
    // 5. MONETIZATION
    // =========================================================================

    // A-Ads Banner
    if (cfg.monetization?.aads?.enabled && cfg.monetization.aads.unit_id) {
      injectAAdsBanner(cfg.monetization.aads.unit_id);
    }

    // Support Widget (BMC, Ko-fi, GitHub Sponsors, Crypto)
    injectSupportWidget(cfg.monetization, profile);

    log('All integrations loaded');

  } catch (err) {
    console.error('[Integrations] Failed to load:', err);
  }

  // ===========================================================================
  // MONETIZATION HELPERS
  // ===========================================================================

  function injectAAdsBanner(unitId) {
    const banner = document.createElement('div');
    banner.id = 'aads-banner';
    banner.style.cssText = `
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 9998;
      background: rgba(3, 7, 18, 0.95);
      backdrop-filter: blur(12px);
      border-top: 1px solid rgba(255,255,255,0.08);
      display: flex;
      justify-content: center;
      padding: 10px;
    `;

    const iframe = document.createElement('iframe');
    iframe.src = `//ad.a-ads.com/${unitId}?size=728x90`;
    iframe.style.cssText = 'width:728px;height:90px;border:0;';
    if (window.innerWidth < 768) {
      iframe.src = `//ad.a-ads.com/${unitId}?size=320x50`;
      iframe.style.width = '320px';
      iframe.style.height = '50px';
    }

    const close = document.createElement('button');
    close.innerHTML = '×';
    close.style.cssText = 'position:absolute;top:5px;right:15px;background:none;border:none;color:#888;font-size:20px;cursor:pointer;';
    close.onclick = () => banner.remove();

    banner.appendChild(iframe);
    banner.appendChild(close);
    document.body.appendChild(banner);
    document.body.style.paddingBottom = '110px';
  }

  function injectSupportWidget(monetization, profile) {
    const btn = document.createElement('button');
    btn.id = 'support-btn';
    btn.innerHTML = '💖 Support';
    btn.style.cssText = `
      position: fixed;
      bottom: 120px;
      left: 20px;
      z-index: 9999;
      background: linear-gradient(135deg, #ec4899, #8b5cf6);
      color: white;
      border: none;
      border-radius: 50px;
      padding: 12px 24px;
      font-weight: 600;
      font-size: 0.95rem;
      box-shadow: 0 4px 15px rgba(236, 72, 153, 0.4);
      cursor: pointer;
      transition: transform 0.2s, box-shadow 0.2s;
      font-family: var(--font-body, system-ui);
    `;
    btn.onmouseover = () => { btn.style.transform = 'scale(1.05)'; };
    btn.onmouseout = () => { btn.style.transform = 'scale(1)'; };

    const modal = document.createElement('div');
    modal.id = 'support-modal';
    modal.style.cssText = `
      display: none;
      position: fixed;
      bottom: 180px;
      left: 20px;
      z-index: 10000;
      background: rgba(15, 23, 42, 0.98);
      backdrop-filter: blur(16px);
      border: 1px solid rgba(255,255,255,0.1);
      border-radius: 16px;
      padding: 20px;
      width: 320px;
      box-shadow: 0 25px 50px rgba(0,0,0,0.5);
      color: white;
      font-family: var(--font-body, system-ui);
    `;

    let links = '<h3 style="margin:0 0 16px 0;font-size:1.1rem;">Support Development</h3>';

    if (monetization?.buymeacoffee?.enabled) {
      links += `<a href="https://buymeacoffee.com/${monetization.buymeacoffee.username}" target="_blank" style="display:flex;align-items:center;gap:10px;background:#FFDD00;color:#000;text-decoration:none;padding:12px 16px;border-radius:10px;margin-bottom:10px;font-weight:600;">☕ Buy Me a Coffee</a>`;
    }

    if (monetization?.kofi?.enabled && monetization.kofi.widget_id) {
      links += `<a href="https://ko-fi.com/${monetization.kofi.widget_id}" target="_blank" style="display:flex;align-items:center;gap:10px;background:#FF5E5B;color:white;text-decoration:none;padding:12px 16px;border-radius:10px;margin-bottom:10px;font-weight:600;">❤️ Ko-fi</a>`;
    }

    if (monetization?.github_sponsors?.enabled) {
      links += `<a href="https://github.com/sponsors/${monetization.github_sponsors.username}" target="_blank" style="display:flex;align-items:center;gap:10px;background:#24292e;color:white;text-decoration:none;padding:12px 16px;border-radius:10px;margin-bottom:10px;font-weight:600;border:1px solid #444;">💖 GitHub Sponsors</a>`;
    }

    if (monetization?.patreon?.enabled && monetization.patreon.username) {
      links += `<a href="https://patreon.com/${monetization.patreon.username}" target="_blank" style="display:flex;align-items:center;gap:10px;background:#FF424D;color:white;text-decoration:none;padding:12px 16px;border-radius:10px;margin-bottom:10px;font-weight:600;">🎨 Patreon</a>`;
    }

    if (monetization?.crypto?.enabled) {
      links += `
        <div style="margin-top:12px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.1);">
          <p style="margin:0 0 8px;font-size:0.85rem;color:#94a3b8;">Crypto Donations</p>
          <p style="margin:4px 0;font-size:0.8rem;"><strong>BTC:</strong> <code style="background:rgba(255,255,255,0.1);padding:2px 6px;border-radius:4px;font-size:0.7rem;">${monetization.crypto.btc?.substring(0,16)}...</code></p>
          <p style="margin:4px 0;font-size:0.8rem;"><strong>ETH:</strong> <code style="background:rgba(255,255,255,0.1);padding:2px 6px;border-radius:4px;font-size:0.7rem;">${monetization.crypto.eth?.substring(0,16)}...</code></p>
          <p style="margin:4px 0;font-size:0.8rem;"><strong>SOL:</strong> <code style="background:rgba(255,255,255,0.1);padding:2px 6px;border-radius:4px;font-size:0.7rem;">${monetization.crypto.sol?.substring(0,16)}...</code></p>
        </div>
      `;
    }

    modal.innerHTML = links;

    btn.onclick = () => {
      modal.style.display = modal.style.display === 'none' ? 'block' : 'none';
    };

    document.addEventListener('click', (e) => {
      if (!btn.contains(e.target) && !modal.contains(e.target)) {
        modal.style.display = 'none';
      }
    });

    document.body.appendChild(btn);
    document.body.appendChild(modal);
  }

})();
