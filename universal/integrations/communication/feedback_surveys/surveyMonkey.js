/**
 * SurveyMonkey Integration
 */
export const surveyMonkey = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        this.surveyId = config.surveyId;
        this.loaded = true;
        console.log('[SurveyMonkey] Ready');
    },

    embed(containerId, surveyId, options = {}) {
        const container = document.getElementById(containerId);
        if (!container) return;

        const id = surveyId || this.surveyId;
        if (!id) return;

        container.innerHTML = `
            <script>(function(t,e,s,n){var o,a,c;t.SMCX=t.SMCX||[],e.getElementById(n)||(o=e.getElementsByTagName(s),a=o[o.length-1],c=e.createElement(s),c.type="text/javascript",c.async=!0,c.id=n,c.src="https://widget.surveymonkey.com/collect/website/js/tRaiETqnLgj758hTBazgd${id}.js",a.parentNode.insertBefore(c,a))})(window,document,"script","smcx-sdk");</script>
            <a style="font: 12px Helvetica, sans-serif; color: #999; text-decoration: none;" href=https://www.surveymonkey.com> Create your own user feedback survey </a>
        `;
    },

    popup(surveyId) {
        const id = surveyId || this.surveyId;
        if (!id) return;

        window.open(`https://www.surveymonkey.com/r/${id}`, 'survey', 'width=600,height=700');
    }
};
