/**
 * Gleam.io Rewards/Giveaways Integration
 */
export const gleam = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;
        this.loaded = true;
        console.log('[Gleam] Ready');
    },

    embed(containerId, campaignUrl) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <a class="e-widget no-hierarchie"
               href="${campaignUrl}"
               rel="nofollow">
                Competition
            </a>
            <script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0];if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.async=true;js.src="https://js.gleam.io/e.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","gleam-js");</script>
        `;
    }
};
