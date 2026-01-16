export function init(config, loadScript) {
  if (!config.id || !config.enabled) return;

  (function(m,e,t,r,i,k,a){m[i]=m[i]||function(){(m[i].a=m[i].a||[]).push(arguments)};
  m[i].l=1*new Date();k=e.createElement(t),a=e.getElementsByTagName(t)[0],k.async=1,k.src=r,a.parentNode.insertBefore(k,a)})
  (window, document, "script", "https://mc.yandex.ru/metrika/tag.js", "ym");

  ym(config.id, "init", {
      clickmap: config.clickmap,
      trackLinks: config.trackLinks,
      accurateTrackBounce: config.accurateTrackBounce,
      webvisor: config.webvisor
  });
}
