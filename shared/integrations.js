/**
 * Master Integrations Loader
 * Dynamically loads 3rd-party services based on shared/profile.json config.
 */

(async function () {
  console.log('🚀 Initializing Master Integrations...');

  const PROFILE_URL = 'https://chirag127.github.io/shared/profile.json';

  try {
    const response = await fetch(PROFILE_URL);
    if (!response.ok) throw new Error('Failed to load profile.json');
    const profile = await response.json();
    const config = profile.config || {};

    if (config.analytics) loadAnalytics(config.analytics);
    if (config.chat) loadChat(config.chat);
    if (config.bug_tracking) loadBugTracking(config.bug_tracking);
    if (config.monetization) loadMonetizationScripts(config.monetization);
    if (config.utilities) loadUtilities(config.utilities);

  } catch (error) {
    console.error('❌ Integration Error:', error);
  }

  // =========================================================================
  // ANALYTICS
  // =========================================================================
  function loadAnalytics(cfg) {
    // 1. Google Analytics 4
    if (cfg.google_analytics_4?.enabled && cfg.google_analytics_4.measurement_id) {
      loadScript(`https://www.googletagmanager.com/gtag/js?id=${cfg.google_analytics_4.measurement_id}`);
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());
      gtag('config', cfg.google_analytics_4.measurement_id);
      console.log('✅ GA4 Loaded');
    }

    // 2. Microsoft Clarity
    if (cfg.microsoft_clarity?.enabled && cfg.microsoft_clarity.project_id) {
      (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      })(window, document, "clarity", "script", cfg.microsoft_clarity.project_id);
      console.log('✅ Clarity Loaded');
    }

    // 3. Yandex Metrica
    if (cfg.yandex_metrica?.enabled && cfg.yandex_metrica.tag_id) {
       (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
       m[i].l=1*new Date();
       for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
       k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
       (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
       ym(cfg.yandex_metrica.tag_id, "init", { clickmap:true, trackLinks:true, accurateTrackBounce:true });
       console.log('✅ Yandex Metrica Loaded');
    }

    // 4. Umami
    if (cfg.umami?.enabled && cfg.umami.website_id) {
      const script = document.createElement('script');
      script.src = cfg.umami.src || "https://cloud.umami.is/script.js";
      script.defer = true;
      script.setAttribute('data-website-id', cfg.umami.website_id);
      document.head.appendChild(script);
      console.log('✅ Umami Loaded');
    }

    // 5. Cloudflare Web Analytics
    if (cfg.cloudflare_web_analytics?.enabled && cfg.cloudflare_web_analytics.beacon_token) {
        const script = document.createElement('script');
        script.defer = true;
        script.src = 'https://static.cloudflareinsights.com/beacon.min.js';
        script.setAttribute('data-cf-beacon', `{"token": "${cfg.cloudflare_web_analytics.beacon_token}"}`);
        document.body.appendChild(script);
        console.log('✅ Cloudflare Analytics Loaded');
    }
  }

  // =========================================================================
  // CHAT
  // =========================================================================
  function loadChat(cfg) {
    // 1. Tawk.to
    if (cfg.tawk_to?.enabled && cfg.tawk_to.property_id) {
      var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
      (function(){
      var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
      s1.async=true;
      s1.src=`https://embed.tawk.to/${cfg.tawk_to.property_id}/${cfg.tawk_to.widget_id || 'default'}`;
      s1.charset='UTF-8';
      s1.setAttribute('crossorigin','*');
      s0.parentNode.insertBefore(s1,s0);
      })();
      console.log('✅ Tawk.to Loaded');
    }

    // 2. Crisp
    if (cfg.crisp?.enabled && cfg.crisp.website_id) {
      window.$crisp=[];window.CRISP_WEBSITE_ID=cfg.crisp.website_id;
      (function(){
        d=document;s=d.createElement("script");s.src="https://client.crisp.chat/l.js";
        s.async=1;d.getElementsByTagName("head")[0].appendChild(s);
      })();
      console.log('✅ Crisp Loaded');
    }
  }

  // =========================================================================
  // BUG TRACKING
  // =========================================================================
  function loadBugTracking(cfg) {
    // 1. Sentry
    if (cfg.sentry?.enabled && cfg.sentry.dsn) {
      loadScript('https://browser.sentry-cdn.com/7.54.0/bundle.min.js', () => {
        if (window.Sentry) {
          Sentry.init({ dsn: cfg.sentry.dsn });
          console.log('✅ Sentry Loaded');
        }
      });
    }
  }

  // =========================================================================
  // MONETIZATION SCRIPTS
  // =========================================================================
  function loadMonetizationScripts(cfg) {
    // 1. Google AdSense
    if (cfg.google_adsense?.enabled && cfg.google_adsense.publisher_id) {
       const script = document.createElement('script');
       script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${cfg.google_adsense.publisher_id}`;
       script.async = true;
       script.crossOrigin = "anonymous";
       document.head.appendChild(script);
       console.log('✅ AdSense Loaded');
    }
  }

  // =========================================================================
  // UTILITIES
  // =========================================================================
  function loadUtilities(cfg) {
      // 1. UserWay
      if (cfg.userway?.enabled && cfg.userway.account_id) {
          (function(d){var s = d.createElement("script");s.setAttribute("data-account", cfg.userway.account_id);
          s.setAttribute("src", "https://cdn.userway.org/widget.js");(d.body || d.head).appendChild(s);})(document);
          console.log('✅ UserWay Loaded');
      }
  }

  // Helper
  function loadScript(src, callback) {
    const script = document.createElement('script');
    script.src = src;
    script.async = true;
    if (callback) script.onload = callback;
    document.head.appendChild(script);
  }

})();
