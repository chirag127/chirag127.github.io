/**
 * Tawk.to Live Chat
 * Source: https://embed.tawk.to/6968e3ea8783b31983eb190b/1jf0rkjhp
 */
(function() {
  const TAWKTO_SRC = 'https://embed.tawk.to/6968e3ea8783b31983eb190b/1jf0rkjhp';

  var Tawk_API = Tawk_API || {};
  var Tawk_LoadStart = new Date();

  var s1 = document.createElement("script");
  s1.async = true;
  s1.src = TAWKTO_SRC;
  s1.charset = 'UTF-8';
  s1.setAttribute('crossorigin', '*');

  var s0 = document.getElementsByTagName("script")[0];
  s0.parentNode.insertBefore(s1, s0);

  console.log('[Chat] Tawk.to loaded');
})();
