/**
 * Native Social Share Integration
 * Uses the browser's native share capability for maximum virality.
 * @module integrations/engagement/social_share/native
 */
export const native = {
    loaded: false,

    init(config) {
        if (!config.enabled || this.loaded) return;
        this.loaded = true;
        this.injectButtons();
    },

    injectButtons() {
        // Create a floating share button for mobile/desktop
        const btn = document.createElement('button');
        btn.id = 'apex-native-share';
        btn.innerHTML = `
            <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8M16 6l-4-4-4 4M12 2v13"/>
            </svg>
            <span>Share</span>
        `;

        // Styling for a premium floating button
        btn.style = `
            position: fixed;
            bottom: 30px;
            right: 30px;
            z-index: 9999;
            background: rgba(0, 122, 255, 0.9);
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 50px;
            display: flex;
            align-items: center;
            gap: 10px;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            cursor: pointer;
            backdrop-filter: blur(10px);
            box-shadow: 0 10px 30px rgba(0, 122, 255, 0.3);
            transition: transform 0.3s, background 0.3s;
        `;

        btn.onmouseover = () => btn.style.transform = 'translateY(-5px) scale(1.05)';
        btn.onmouseout = () => btn.style.transform = 'translateY(0) scale(1)';

        btn.onclick = () => {
            if (navigator.share) {
                navigator.share({
                    title: document.title,
                    text: `Check out this tool: ${document.title}`,
                    url: window.location.href
                }).then(() => {
                    console.log('[NativeShare] Success');
                }).catch((err) => {
                    console.warn('[NativeShare] Aborted', err.message);
                });
            } else {
                // Fallback: Copy to clipboard
                const dummy = document.createElement('input');
                document.body.appendChild(dummy);
                dummy.value = window.location.href;
                dummy.select();
                document.execCommand('copy');
                document.body.removeChild(dummy);

                btn.innerHTML = '<span>Link Copied!</span>';
                setTimeout(() => {
                    btn.innerHTML = `
                        <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M4 12v8a2 2 0 002 2h12a2 2 0 002-2v-8M16 6l-4-4-4 4M12 2v13"/>
                        </svg>
                        <span>Share</span>
                    `;
                }, 2000);
            }
        };

        document.body.appendChild(btn);
    }
};
