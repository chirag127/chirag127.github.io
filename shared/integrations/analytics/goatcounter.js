/**
 * GoatCounter Analytics
 * Code: chirag127
 */
(function() {
  const GOAT_CODE = 'chirag127';

  window.goatcounter = {
    path: function(p) { return location.host + p }
  };

  const script = document.createElement('script');
  script.async = true;
  script.src = `https://${GOAT_CODE}.goatcounter.com/count.js`;
  script.setAttribute('data-goatcounter', `https://${GOAT_CODE}.goatcounter.com/count`);
  document.head.appendChild(script);

  console.log('[Analytics] GoatCounter loaded');
})();
