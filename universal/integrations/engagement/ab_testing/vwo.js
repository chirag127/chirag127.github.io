/**
 * VWO (Visual Website Optimizer) Integration
 */
export const vwo = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.accountId || this.loaded) return;

        window._vwo_code = window._vwo_code || (function() {
            var account_id = config.accountId,
                settings_tolerance = 2000,
                library_tolerance = 2500,
                use_existing_jquery = false,
                is_spa = 1,
                hide_element = 'body';

            var f = false, d = document;
            return {
                use_existing_jquery: function() { return use_existing_jquery; },
                library_tolerance: function() { return library_tolerance; },
                finish: function() { if (!f) { f = true; var a = d.getElementById('_vis_opt_path_hides'); if (a) a.parentNode.removeChild(a); } },
                finished: function() { return f; },
                load: function(a) { var b = d.createElement('script'); b.src = a; b.type = 'text/javascript'; b.innerText; b.onerror = function() { window._vwo_code.finish(); }; d.getElementsByTagName('head')[0].appendChild(b); },
                init: function() { this.settings_timer = setTimeout('window._vwo_code.finish()', settings_tolerance); var a = d.createElement('style'), b = hide_element ? hide_element + '{opacity:0 !important;filter:alpha(opacity=0) !important;background:none !important;}' : '', h = d.getElementsByTagName('head')[0]; a.setAttribute('id', '_vis_opt_path_hides'); a.setAttribute('type', 'text/css'); if (a.styleSheet) a.styleSheet.cssText = b; else a.appendChild(d.createTextNode(b)); h.appendChild(a); this.load('https://dev.visualwebsiteoptimizer.com/j.php?a=' + account_id + '&u=' + encodeURIComponent(d.URL) + '&r=' + Math.random()); return settings_tolerance; }
            };
        }());

        window._vwo_settings_timer = window._vwo_code.init();

        this.loaded = true;
        console.log('[VWO] Loaded:', config.accountId);
    }
};
