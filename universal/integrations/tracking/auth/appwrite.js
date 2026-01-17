/**
 * Appwrite Integration
 */
export const appwrite = {
    loaded: false,
    client: null,
    account: null,

    init(config) {
        if (!config.enabled || !config.endpoint || !config.projectId || this.loaded) return;

        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/appwrite@13.0.0';
        script.onload = () => {
            const { Client, Account } = window.Appwrite;
            this.client = new Client()
                .setEndpoint(config.endpoint)
                .setProject(config.projectId);
            this.account = new Account(this.client);
            this.ready = true;
            console.log('[Appwrite] Ready');
        };
        document.head.appendChild(script);

        this.loaded = true;
    },

    async createAccount(email, password, name) {
        if (!this.account) return null;
        return this.account.create('unique()', email, password, name);
    },

    async login(email, password) {
        if (!this.account) return null;
        return this.account.createEmailSession(email, password);
    },

    async logout() {
        if (!this.account) return;
        return this.account.deleteSession('current');
    },

    async getAccount() {
        if (!this.account) return null;
        return this.account.get();
    }
};
