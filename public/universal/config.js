/* UNIVERSAL CONFIGURATION & NON-MODULE LOADERS
   Hosted at: /universal/config.js
*/

window.SITE_CONFIG = {
    // --- ANALYTICS STACK ---
    ga4: { id: 'G-PQ26TN1XJ4', enabled: true },
    yandex: { id: 106273806, enabled: true, webvisor: true, clickmap: true, trackLinks: true, accurateTrackBounce: true },
    clarity: { id: 'v1u8hhnpw2', enabled: true },
    cloudflare: { token: '333c0705152b4949b3eb0538cd4c2296', enabled: true },
    mixpanel: { token: '8d06e28c86c9b01865d866d0ac4982af', enabled: true },
    amplitude: { apiKey: 'd1733215e7a8236a73912adf86ac450b', enabled: true },
    posthog: { key: 'phc_P9VZ5bjyFoWrIUbecuFTUN2oKavGQYqT3rVSxX8Kqn8', host: 'https://us.i.posthog.com', enabled: true },
    umami: { id: '18b3773e-e365-458c-be78-d1d8238b4f15', host: 'https://cloud.umami.is', enabled: true },
    goatcounter: { code: 'chirag127', enabled: true },
    heap: { id: '3491046690', enabled: true },
    logrocket: { id: 'nshsif/github-hub', enabled: true },
    beam: { token: '1148dc4c-933b-4fd2-ba28-a0bb56f78978', enabled: true },
    counter_dev: { id: '5c0f4066-d78f-4cd8-a31d-40448c2f2749', enabled: true },
    cronitor: { key: '205a4c0b70da8fb459aac415c1407b4d', enabled: true },

    // --- MONETIZATION (Ads) ---
    propeller: { zone: '202358', enabled: true },
    adsense: { id: '', enabled: false }, // Placeholder for future use

    // --- CHAT ---
    tawk: { src: 'https://embed.tawk.to/6968e3ea8783b31983eb190b/1jf0rkjhp', enabled: true },

    // --- ERROR TRACKING ---
    sentry: { dsn: 'https://45890ca96ce164182a3c74cca6018e3e@o4509333332164608.ingest.de.sentry.io/4509333334458448', enabled: true },
    honeybadger: { apiKey: 'hbp_x8dJHBTim5uTkF7pIZVqj55X4wedmR11iovM', enabled: true },
    rollbar: { accessToken: '88062048efd74f7c8e11659187da782b', enabled: true },
    bugsnag: { apiKey: '84afb61cb3bf458037f4f15eeab394c4', enabled: true },
    glitchtip: { dsn: 'https://fe8b6978187b4ef09020464050d17b06@app.glitchtip.com/19542', enabled: true },

    // --- AUTHENTICATION (Firebase handled in firebase-modules.js) ---
    auth0: { domain: '', clientId: '' },
    clerk: { publishableKey: '' },

    // --- DATABASE ---
    supabase: { url: '', anonKey: '' }
};

(function() {
    console.log("🚀 Initializing Universal Engines...");

    function loadScript(src, attrs = {}) {
        const s = document.createElement('script');
        s.src = src;
        Object.keys(attrs).forEach(k => s.setAttribute(k, attrs[k]));
        s.async = true;
        document.head.appendChild(s);
    }

    const c = window.SITE_CONFIG;

    // 1. Google Analytics 4
    if(c.ga4.id && c.ga4.enabled) {
        loadScript(`https://www.googletagmanager.com/gtag/js?id=${c.ga4.id}`);
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', c.ga4.id);
    }

    // 2. Yandex Metrica
    if(c.yandex.id && c.yandex.enabled) {
        (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
        m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
        (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");
        ym(c.yandex.id, "init", {
            clickmap: c.yandex.clickmap,
            trackLinks: c.yandex.trackLinks,
            accurateTrackBounce: c.yandex.accurateTrackBounce,
            webvisor: c.yandex.webvisor
        });
    }

    // 3. Microsoft Clarity
    if(c.clarity.id && c.clarity.enabled) {
        (function(c,l,a,r,i,t,y){c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);})
        (window, document, "clarity", "script", c.clarity.id);
    }

    // 4. PostHog
    if(c.posthog.key && c.posthog.enabled) {
        !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
        posthog.init(c.posthog.key,{api_host:c.posthog.host});
    }

    // 5. Cloudflare Analytics
    if(c.cloudflare.token && c.cloudflare.enabled) loadScript('https://static.cloudflareinsights.com/beacon.min.js', {'data-cf-beacon': `{"token": "${c.cloudflare.token}"}`});

    // 6. Tawk.to
    if(c.tawk.src && c.tawk.enabled) loadScript(c.tawk.src, {'crossorigin': '*'});

    // 7. Umami
    if(c.umami.id && c.umami.enabled) loadScript(`${c.umami.host}/script.js`, {'data-website-id': c.umami.id});

    // 8. GoatCounter
    if(c.goatcounter.code && c.goatcounter.enabled) loadScript('//gc.zgo.at/count.js', {'data-goatcounter': `https://${c.goatcounter.code}.goatcounter.com/count`});

    // 9. Heap
    if(c.heap.id && c.heap.enabled) {
        window.heap=window.heap||[],heap.load=function(e,t){window.heap.envId=e,window.heap.clientConfig=t=t||{},window.heap.clientConfig.shouldFetchServerConfig=!1;var a=document.createElement("script");a.type="text/javascript",a.async=!0,a.src="https://cdn.us.heap-api.com/config/"+e+"/heap_config.js";var r=document.getElementsByTagName("script")[0];r.parentNode.insertBefore(a,r);var n=["init","startTracking","stopTracking","track","resetIdentity","identify","getSessionId","getUserId","getIdentity","addUserProperties","addEventProperties","removeEventProperty","clearEventProperties","addAccountProperties","addAdapter","addTransformer","addTransformerFn","onReady","addPageviewProperties","removePageviewProperty","clearPageviewProperties","trackPageview"],i=function(e){return function(){var t=Array.prototype.slice.call(arguments,0);window.heapReadyCb.push({name:e,fn:function(){heap[e]&&heap[e].apply(heap,t)}})}};for(var p=0;p<n.length;p++)heap[n[p]]=i(n[p])};
        heap.load(c.heap.id);
    }

    // 10. LogRocket
    if(c.logrocket.id && c.logrocket.enabled) {
        loadScript('https://cdn.logr-in.com/LogRocket.min.js');
        window.setTimeout(() => { if(window.LogRocket) window.LogRocket.init(c.logrocket.id); }, 2000);
    }

    // 11. Beam Analytics
    if(c.beam.token && c.beam.enabled) loadScript('https://beamanalytics.b-cdn.net/beam.min.js', {'data-token': c.beam.token});

    // 12. Counter.dev
    if(c.counter_dev.id && c.counter_dev.enabled) loadScript('https://cdn.counter.dev/script.js', {'data-id': c.counter_dev.id, 'data-utcoffset': '6'});

    // 13. Cronitor RUM
    if(c.cronitor.key && c.cronitor.enabled) {
        loadScript('https://rum.cronitor.io/script.js');
        window.cronitor = window.cronitor || function() { (window.cronitor.q = window.cronitor.q || []).push(arguments); };
        cronitor('config', { clientKey: c.cronitor.key });
    }

    // 14. PropellerAds (Multitag)
    if(c.propeller.zone && c.propeller.enabled) {
        loadScript('https://quge5.com/88/tag.min.js', {'data-zone': c.propeller.zone, 'data-cfasync': 'false'});
    }

    // 15. Sentry
    if(c.sentry.dsn && c.sentry.enabled) {
          loadScript('https://browser.sentry-cdn.com/7.60.0/bundle.min.js', {'crossorigin': 'anonymous'});
          window.Sentry = window.Sentry || {};
          window.setTimeout(() => {
              if(window.Sentry && window.Sentry.init) {
                  window.Sentry.init({
                      dsn: c.sentry.dsn,
                      sendDefaultPii: true
                  });
              }
          }, 2000);
    }

    // 16. Honeybadger
    if(c.honeybadger.apiKey && c.honeybadger.enabled) {
        loadScript('//js.honeybadger.io/v6.12/honeybadger.min.js');
        window.setTimeout(() => {
            if(window.Honeybadger) {
                window.Honeybadger.configure({
                    apiKey: c.honeybadger.apiKey,
                    environment: "production"
                });
            }
        }, 2000);
    }

    // 17. Bugsnag
    if(c.bugsnag.apiKey && c.bugsnag.enabled) {
        loadScript('//d2wy8f7a9ursnm.cloudfront.net/v8/bugsnag.min.js');
        window.setTimeout(() => {
            if(window.Bugsnag) {
                window.Bugsnag.start({ apiKey: c.bugsnag.apiKey });
            }
        }, 2000);
    }

     // 18. GlitchTip
     if(c.glitchtip.dsn && c.glitchtip.enabled) {
        // GlitchTip uses Sentry SDK, ensure Sentry is loaded or handle appropriately
        // If Sentry is already loaded by step 15, we might need to handle instance conflict or just use one.
        // For simplicity, we assume one primary error tracker, but if both are present, last one might win or they might conflict.
        // If Sentry is NOT enabled but GlitchTip is, we need to load Sentry SDK.
        if (!c.sentry.enabled) {
             loadScript('https://browser.sentry-cdn.com/7.60.0/bundle.min.js', {'crossorigin': 'anonymous'});
        }
        window.setTimeout(() => {
              if(window.Sentry && window.Sentry.init) {
                  window.Sentry.init({
                      dsn: c.glitchtip.dsn,
                      tracesSampleRate: 0.01
                  });
              }
        }, 2500); // Wait a bit longer than Sentry init
    }


})();
