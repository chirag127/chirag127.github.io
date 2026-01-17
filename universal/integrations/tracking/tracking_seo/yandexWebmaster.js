/**
 * Yandex Webmaster Verification Integration
 */
export const yandexWebmaster = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.verificationTag || this.loaded) return;

        const meta = document.createElement('meta');
        meta.name = 'yandex-verification';
        meta.content = config.verificationTag;
        document.head.appendChild(meta);

        this.loaded = true;
        console.log('[YandexWebmaster] Verification tag added');
    }
};
