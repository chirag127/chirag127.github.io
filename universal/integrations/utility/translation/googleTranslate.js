/**
 * Google Translate Widget Integration
 */
export const googleTranslate = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;

        window.googleTranslateElementInit = () => {
            new window.google.translate.TranslateElement({
                pageLanguage: config.pageLanguage || 'en',
                includedLanguages: config.languages || '',
                layout: window.google.translate.TranslateElement.InlineLayout.SIMPLE,
                autoDisplay: false
            }, config.containerId || 'google_translate_element');

            this.ready = true;
            console.log('[GoogleTranslate] Ready');
        };

        const script = document.createElement('script');
        script.src = '//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
        document.head.appendChild(script);

        this.loaded = true;
    },

    render(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.id = 'google_translate_element';
    }
};
