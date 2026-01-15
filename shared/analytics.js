/**
 * Centralized Analytics - All 10 Trackers
 *
 * Include this single file in ALL projects:
 * <script src="https://chirag127.github.io/shared/analytics.js" defer></script>
 *
 * UPDATE THIS FILE ONCE → CHANGES APPLY EVERYWHERE
 */

(function() {
  'use strict';

  // =========================================================================
  // CONFIGURATION - UPDATE ONLY HERE
  // =========================================================================

  const CONFIG = {
    // Google Analytics 4
    ga4: {
      id: 'G-PQ26TN1XJ4',
      enabled: true
    },

    // Yandex Metrica (Webvisor, Clickmap, Scrollmap enabled)
    yandex: {
      id: 106273806,
      enabled: true,
      webvisor: true,
      clickmap: true,
      trackLinks: true,
      accurateTrackBounce: true
    },

    // Microsoft Clarity
    clarity: {
      id: 'v1u8hhnpw2',
      enabled: true
    },

    // Cloudflare Web Analytics
    cloudflare: {
      token: '333c0705152b4949b3eb0538cd4c2296',
      enabled: true
    },

    // Tawk.to Live Chat
    tawkto: {
      src: 'https://embed.tawk.to/6968e3ea8783b31983eb190b/1jf0rkjhp',
      enabled: true
    },

    // Mixpanel
    mixpanel: {
      token: '8d06e28c86c9b01865d866d0ac4982af',
      enabled: true
    },

    // Amplitude
    amplitude: {
      apiKey: 'd1733215e7a8236a73912adf86ac450b',
      enabled: true
    },

    // PostHog
    posthog: {
      key: 'phc_P9VZ5bjyFoWrIUbecuFTUN2oKavGQYqT3rVSxX8Kqn8',
      host: 'https://us.i.posthog.com',
      enabled: true
    },

    // Umami
    umami: {
      id: '18b3773e-e365-458c-be78-d1d8238b4f15',
      host: 'https://cloud.umami.is',
      enabled: true
    },

    // GoatCounter
    goatcounter: {
      code: 'chirag127',
      enabled: true
    }
  };

  // =========================================================================
  // LOADER FUNCTIONS
  // =========================================================================

  function loadScript(src, attrs = {}) {
    const script = document.createElement('script');
    script.src = src;
    script.async = true;
    Object.entries(attrs).forEach(([key, value]) => {
      script.setAttribute(key, value);
    });
    document.head.appendChild(script);
    return script;
  }

  // =========================================================================
  // 1. GOOGLE ANALYTICS 4
  // =========================================================================

  if (CONFIG.ga4.enabled) {
    loadScript(`https://www.googletagmanager.com/gtag/js?id=${CONFIG.ga4.id}`);
    window.dataLayer = window.dataLayer || [];
    function gtag() { dataLayer.push(arguments); }
    gtag('js', new Date());
    gtag('config', CONFIG.ga4.id);
    window.gtag = gtag;
  }

  // =========================================================================
  // 2. YANDEX METRICA
  // =========================================================================

  if (CONFIG.yandex.enabled) {
    (function(m,e,t,r,i,k,a){
      m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
      m[i].l=1*new Date();
      for (var j = 0; j < document.scripts.length; j++) {
        if (document.scripts[j].src === r) { return; }
      }
      k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a);
    })(window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

    ym(CONFIG.yandex.id, "init", {
      clickmap: CONFIG.yandex.clickmap,
      trackLinks: CONFIG.yandex.trackLinks,
      accurateTrackBounce: CONFIG.yandex.accurateTrackBounce,
      webvisor: CONFIG.yandex.webvisor
    });
  }

  // =========================================================================
  // 3. MICROSOFT CLARITY
  // =========================================================================

  if (CONFIG.clarity.enabled) {
    (function(c,l,a,r,i,t,y){
      c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
      t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
      y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
    })(window, document, "clarity", "script", CONFIG.clarity.id);
  }

  // =========================================================================
  // 4. CLOUDFLARE WEB ANALYTICS
  // =========================================================================

  if (CONFIG.cloudflare.enabled) {
    loadScript('https://static.cloudflareinsights.com/beacon.min.js', {
      'data-cf-beacon': JSON.stringify({ token: CONFIG.cloudflare.token })
    });
  }

  // =========================================================================
  // 5. TAWK.TO LIVE CHAT
  // =========================================================================

  if (CONFIG.tawkto.enabled) {
    var Tawk_API = Tawk_API || {}, Tawk_LoadStart = new Date();
    loadScript(CONFIG.tawkto.src, { charset: 'UTF-8', crossorigin: '*' });
  }

  // =========================================================================
  // 6. MIXPANEL
  // =========================================================================

  if (CONFIG.mixpanel.enabled) {
    (function(f,b){if(!b.__SV){var e,g,i,h;window.mixpanel=b;b._i=[];b.init=function(e,f,c){
    function g(a,d){var b=d.split(".");2==b.length&&(a=a[b[0]],d=b[1]);a[d]=function(){a.push([d].concat(
    Array.prototype.slice.call(arguments,0)))}}var a=b;"undefined"!==typeof c?a=b[c]=[]:c="mixpanel";
    a.people=a.people||[];a.toString=function(a){var d="mixpanel";"mixpanel"!==c&&(d+="."+c);a||(d+=" (stub)");
    return d};a.people.toString=function(){return a.toString(1)+".people (stub)"};
    i="disable time_event track track_pageview track_links track_forms track_with_groups add_group set_group remove_group register register_once alias unregister identify name_tag set_config reset opt_in_tracking opt_out_tracking has_opted_in_tracking has_opted_out_tracking clear_opt_in_out_tracking start_batch_senders people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user people.remove".split(" ");
    for(h=0;h<i.length;h++)g(a,i[h]);var j="set set_once union unset remove delete".split(" ");
    a.get_group=function(){function b(c){d[c]=function(){call2_args=arguments;call2=[c].concat(Array.prototype.slice.call(call2_args,0));a.push([e,call2])}}
    for(var d={},e=["get_group"].concat(Array.prototype.slice.call(arguments,0)),c=0;c<j.length;c++)b(j[c]);return d};
    b._i.push([e,f,c])};b.__SV=1.2;e=f.createElement("script");e.type="text/javascript";e.async=!0;
    e.src="https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";
    g=f.getElementsByTagName("script")[0];g.parentNode.insertBefore(e,g)}})(document,window.mixpanel||[]);

    mixpanel.init(CONFIG.mixpanel.token, { track_pageview: "url-with-path" });
  }

  // =========================================================================
  // 7. AMPLITUDE
  // =========================================================================

  if (CONFIG.amplitude.enabled) {
    !function(){"use strict";!function(e,t){var r=e.amplitude||{_q:[],_iq:{}};if(r.invoked);else{r.invoked=!0;
    var n=t.createElement("script");n.type="text/javascript",n.integrity="sha384-PPfHw98myKtJkA9OdPBMQ6n8yvUaYk0EBkKreHyfc+A/LNwqX4Xbqr/n+1Hw9G7I",
    n.crossOrigin="anonymous",n.async=!0,n.src="https://cdn.amplitude.com/libs/analytics-browser-2.11.1-min.js.gz",
    n.onload=function(){e.amplitude.runQueuedFunctions||console.log("[Amplitude] Error: could not load SDK")};
    var s=t.getElementsByTagName("script")[0];s.parentNode.insertBefore(n,s);for(var a=function(){return this._q.push(Array.prototype.slice.call(arguments,0)),this},o=["add","append","clearAll","prepend","set","setOnce","unset","preInsert","postInsert","remove","getUserProperties"],u=0;u<o.length;u++)r.Identify.prototype[o[u]]=a;for(var c=function(){return this._q.push(Array.prototype.slice.call(arguments,0)),this},l=["getEventProperties","setProductId","setQuantity","setPrice","setRevenue","setRevenueType","setEventProperties"],d=0;d<l.length;d++)r.Revenue.prototype[l[d]]=c;r.Identify=function(){this._q=[]},r.Revenue=function(){this._q=[]};for(var i=["init","logEvent","logRevenue","setUserId","setUserProperties","setOptOut","setVersionName","setDomain","setDeviceId","enableTracking","setGlobalUserProperties","identify","clearUserProperties","setGroup","logRevenueV2","regenerateDeviceId","groupIdentify","onInit","onNewSessionStart","logEventWithTimestamp","logEventWithGroups","setSessionId","resetSessionId","getDeviceId","getUserId","setMinTimeBetweenSessionsMillis","setEventUploadThreshold","setEventUploadPeriodMillis","setServerZone","setServerUrl","sendEvents","setLibrary","setTransport","getSessionId","setContentType","setBatchEvents"],p=function(e){r[e]=function(){return this._q.push({name:e,args:Array.prototype.slice.call(arguments,0)}),this}},v=0;v<i.length;v++)p(i[v]);e.amplitude=r}}(window,document)}();

    amplitude.init(CONFIG.amplitude.apiKey);
  }

  // =========================================================================
  // 8. POSTHOG
  // =========================================================================

  if (CONFIG.posthog.enabled) {
    !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.crossOrigin="anonymous",p.async=!0,p.src=s.api_host.replace(".i.posthog.com","-assets.i.posthog.com")+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="init capture register register_once register_for_session unregister unregister_for_session getFeatureFlag getFeatureFlagPayload isFeatureEnabled reloadFeatureFlags updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures on onFeatureFlags onSessionId getSurveys getActiveMatchingSurveys renderSurvey canRenderSurvey getNextSurveyStep identify setPersonProperties group resetGroups setPersonPropertiesForFlags resetPersonPropertiesForFlags setGroupPropertiesForFlags resetGroupPropertiesForFlags reset get_distinct_id getGroups get_session_id get_session_replay_url alias set_config startSessionRecording stopSessionRecording sessionRecordingStarted captureException loadToolbar get_property getSessionProperty createPersonProfile opt_in_capturing opt_out_capturing has_opted_in_capturing has_opted_out_capturing clear_opt_in_out_capturing debug".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);

    posthog.init(CONFIG.posthog.key, { api_host: CONFIG.posthog.host });
  }

  // =========================================================================
  // 9. UMAMI
  // =========================================================================

  if (CONFIG.umami.enabled) {
    loadScript(`${CONFIG.umami.host}/script.js`, {
      'data-website-id': CONFIG.umami.id
    });
  }

  // =========================================================================
  // 10. GOATCOUNTER
  // =========================================================================

  if (CONFIG.goatcounter.enabled) {
    loadScript(`https://${CONFIG.goatcounter.code}.goatcounter.com/count.js`, {
      'data-goatcounter': `https://${CONFIG.goatcounter.code}.goatcounter.com/count`
    });
  }

  // =========================================================================
  // HELPER: Track Custom Events (Unified API)
  // =========================================================================

  window.trackEvent = function(eventName, properties = {}) {
    // GA4
    if (window.gtag) {
      gtag('event', eventName, properties);
    }

    // Yandex
    if (window.ym) {
      ym(CONFIG.yandex.id, 'reachGoal', eventName, properties);
    }

    // Mixpanel
    if (window.mixpanel) {
      mixpanel.track(eventName, properties);
    }

    // Amplitude
    if (window.amplitude) {
      amplitude.track(eventName, properties);
    }

    // PostHog
    if (window.posthog) {
      posthog.capture(eventName, properties);
    }

    console.log('[Analytics] Event:', eventName, properties);
  };

  console.log('[Analytics] All 10 trackers loaded from central hub');
})();
