/**
 * CrazyEgg Integration
 */
export const crazyegg = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.accountNumber || this.loaded) return;

        const script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = `//script.crazyegg.com/pages/scripts/${config.accountNumber}.js`;
        script.async = true;
        document.head.appendChild(script);

        this.loaded = true;
        console.log('[CrazyEgg] Loaded:', config.accountNumber);
    }
};
