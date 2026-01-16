/**
 * Unified Analytics Module
 * Consolidates all analytics integrations into a single file.
 */

export const Analytics = {
    ga4: {
        init: (config, loadScript) => {
            if (!config.id) return;
            loadScript(`https://www.googletagmanager.com/gtag/js?id=${config.id}`)
                .then(() => {
                    window.dataLayer = window.dataLayer || [];
                    function gtag(){dataLayer.push(arguments);}
                    gtag('js', new Date());
                    gtag('config', config.id);
                });
        }
    },
    yandex: {
        init: (config, loadScript) => {
            if (!config.id) return;
            (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
            m[i].l=1*new Date();
            for (var j = 0; j < document.scripts.length; j++) {if (document.scripts[j].src === r) { return; }}
            k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
            (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

            ym(config.id, "init", {
                clickmap:true,
                trackLinks:true,
                accurateTrackBounce:true,
                webvisor:true
            });
        }
    },
    clarity: {
        init: (config, loadScript) => {
            if (!config.id) return;
            (function(c,l,a,r,i,t,y){
                c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
                t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
                y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
            })(window, document, "clarity", "script", config.id);
        }
    },
    posthog: {
        init: (config, loadScript) => {
            if (!config.key) return;
            !function(t,e){var o,n,p,r;e.__SV||(window.posthog=e,e._i=[],e.init=function(i,s,a){function g(t,e){var o=e.split(".");2==o.length&&(t=t[o[0]],e=o[1]),t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}(p=t.createElement("script")).type="text/javascript",p.async=!0,p.src=s.api_host+"/static/array.js",(r=t.getElementsByTagName("script")[0]).parentNode.insertBefore(p,r);var u=e;for(void 0!==a?u=e[a]=[]:a="posthog",u.people=u.people||[],u.toString=function(t){var e="posthog";return"posthog"!==a&&(e+="."+a),t||(e+=" (stub)"),e},u.people.toString=function(){return u.toString(1)+".people (stub)"},o="capture identify alias people.set people.set_once set_config register register_once unregister opt_out_capturing has_opted_out_capturing opt_in_capturing reset isFeatureEnabled onFeatureFlags getFeatureFlag getFeatureFlagPayload reloadFeatureFlags group updateEarlyAccessFeatureEnrollment getEarlyAccessFeatures getActiveMatchingSurveys getSurveys".split(" "),n=0;n<o.length;n++)g(u,o[n]);e._i.push([i,s,a])},e.__SV=1)}(document,window.posthog||[]);
            posthog.init(config.key, {api_host: config.host || 'https://app.posthog.com'});
        }
    },
    umami: {
        init: (config, loadScript) => {
            if (!config.id || !config.host) return;
            const s = document.createElement('script');
            s.async = true;
            s.defer = true;
            s.dataset.websiteId = config.id;
            s.src = config.host; // e.g., https://analytics.umami.is/script.js
            document.head.appendChild(s);
        }
    },
    cloudflare: {
        init: (config, loadScript) => {
             if (!config.token) return;
            const s = document.createElement('script');
            s.defer = true;
            s.src = 'https://static.cloudflareinsights.com/beacon.min.js';
            s.dataset.cfBeacon = `{"token": "${config.token}"}`;
            document.body.appendChild(s);
        }
    },
    mixpanel: {
        init: (config, loadScript) => {
            if (!config.token) return;
            (function(f,b){if(!b.__SV){var e,g,i,h;window.mixpanel=b;b._i=[];b.init=function(e,f,c){function g(a,d){var b=d.split(".");2==b.length&&(a=a[b[0]],d=b[1]);a[d]=function(){a.push([d].concat(Array.prototype.slice.call(arguments,0)))}}var a=b; "undefined"!==typeof c?a=b[c]=[]:c="mixpanel";a.people=a.people||[];a.toString=function(a){var d="mixpanel";"mixpanel"!==c&&(d+="."+c);a||(d+=" (stub)");return d};a.people.toString=function(){return a.toString(1)+".people (stub)"};i="disable time_event track track_pageview track_links track_forms register register_once alias unregister identify name_tag set_config reset people.set people.set_once people.unset people.increment people.append people.union people.track_charge people.clear_charges people.delete_user".split(" ");
            for(h=0;h<i.length;h++)g(a,i[h]);b._i.push([e,f,c])};b.__SV=1.2;e=f.createElement("script");e.type="text/javascript";e.async=!0;e.src="undefined"!==typeof MIXPANEL_CUSTOM_LIB_URL?MIXPANEL_CUSTOM_LIB_URL:"file:"===f.location.protocol&&"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js".match(/^\/\//)?"https://cdn.mxpnl.com/libs/mixpanel-2-latest.min.js":"//cdn.mxpnl.com/libs/mixpanel-2-latest.min.js";g=f.getElementsByTagName("script")[0];g.parentNode.insertBefore(e,g)}})(document,window.mixpanel||[]);
            mixpanel.init(config.token);
        }
    },
    goatcounter: {
        init: (config, loadScript) => {
            if (!config.endpoint) return;
            const s = document.createElement('script');
            s.async = true;
            s.src = '//gc.zgo.at/count.js';
            s.dataset.goatcounter = config.endpoint;
            document.body.appendChild(s);
        }
    },
    heap: {
        init: (config, loadScript) => {
            if (!config.id) return;
            window.heap=window.heap||[],heap.load=function(e,t){window.heap.appid=e,window.heap.config=t=t||{};var r=document.createElement("script");r.type="text/javascript",r.async=!0,r.src="https://cdn.heapanalytics.com/js/heap-"+e+".js";var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(r,a);for(var n=function(e){return function(){heap.push([e].concat(Array.prototype.slice.call(arguments,0)))}},p=["addEventProperties","addUserProperties","clearEventProperties","identify","resetIdentity","removeEventProperty","setEventProperties","track","unsetEventProperty"],o=0;o<p.length;o++)heap[p[o]]=n(p[o])};
            heap.load(config.id);
        }
    },
    logrocket: {
        init: (config, loadScript) => {
            if (!config.id) return;
            loadScript('https://cdn.lr-in.com/LogRocket.min.js')
                .then(() => { if(window.LogRocket) window.LogRocket.init(config.id); });
        }
    },
    amplitude: {
        init: (config, loadScript) => {
             if (!config.key) return;
             loadScript('https://cdn.amplitude.com/libs/amplitude-8.17.0-min.gz.js')
                .then(() => {
                    if(window.amplitude) window.amplitude.getInstance().init(config.key);
                });
        }
    },
    beam: {
        init: (config, loadScript) => {
            if (!config.token) return;
            const s = document.createElement('script');
            s.src = "https://beamanalytics.b-cdn.net/beam.min.js";
            s.dataset.token = config.token;
            s.async = true;
            document.head.appendChild(s);
        }
    },
    counterdev: {
        init: (config, loadScript) => {
             if (!config.id) return;
             const s = document.createElement('script');
             s.src = "https://cdn.counter.dev/script.js";
             s.dataset.id = config.id;
             s.dataset.utcoffset = config.offset || "0";
             document.body.appendChild(s);
        }
    },
    cronitor: {
        init: (config, loadScript) => {
             if (!config.id) return;
             window.cronitor = window.cronitor || function() { (window.cronitor.q = window.cronitor.q || []).push(arguments); };
             cronitor('config', { clientKey: config.id });
             const s = document.createElement('script');
             s.src = "https://rum.cronitor.io/script.js";
             s.async = true;
             document.body.appendChild(s);
        }
    }
};
