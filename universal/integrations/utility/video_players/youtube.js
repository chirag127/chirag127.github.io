export const youtube = {
    init: (config) => {
        if (!config.enabled) return;
        // YouTube API often loaded on demand, but this could load the IFrame API
        const tag = document.createElement('script');
        tag.src = "https://www.youtube.com/iframe_api";
        const firstScriptTag = document.getElementsByTagName('script')[0];
        firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    }
};
