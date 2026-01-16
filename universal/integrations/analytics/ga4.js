export function init(config, loadScript) {
  if (!config.id || !config.enabled) return;

  loadScript(`https://www.googletagmanager.com/gtag/js?id=${config.id}`);

  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', config.id);
}
