/**
 * SuprSend Notification Integration
 */
export const suprsend = {
    loaded: false,

    init(config) {
        if (!config.enabled || !config.workspaceKey || this.loaded) return;

        this.workspaceKey = config.workspaceKey;
        this.loaded = true;
        console.log('[SuprSend] Ready');
    }
};
