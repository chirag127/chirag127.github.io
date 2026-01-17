/**
 * Facebook Comments Integration
 */
export const facebookComments = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.appId || this.loaded) return;

        window.fbAsyncInit = function() {
            window.FB.init({
                appId: config.appId,
                xfbml: true,
                version: 'v18.0'
            });
        };

        const script = document.createElement('script');
        script.src = 'https://connect.facebook.net/en_US/sdk.js';
        script.async = true;
        script.defer = true;
        script.crossOrigin = 'anonymous';
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[FacebookComments] Loaded:', config.appId);
    },

    render(containerId, url) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="fb-comments"
                 data-href="${url || window.location.href}"
                 data-width="100%"
                 data-numposts="10">
            </div>
        `;

        if (window.FB) {
            window.FB.XFBML.parse(container);
        }
    }
};
