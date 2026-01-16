/**
 * Amplitude Analytics
 * API Key: d1733215e7a8236a73912adf86ac450b
 */
(function() {
  const AMPLITUDE_KEY = 'd1733215e7a8236a73912adf86ac450b';

  !function(){"use strict";!function(e,t){var r=e.amplitude||{_q:[],_iq:{}};if(r.invoked)e.console&&console.error&&console.error("Amplitude snippet has been loaded.");else{var n=function(e,t){e.prototype[t]=function(){return this._q.push({name:t,args:Array.prototype.slice.call(arguments,0)}),this}},s=function(e,t,r){return function(n){e._q.push({name:t,args:Array.prototype.slice.call(arguments,0),resolve:n,reject:r})}},o=function(e,t,r){e._q.push({name:t,args:Array.prototype.slice.call(arguments,0)})},i=function(e,t,r){e[t]=function(){if(r)return{promise:new Promise(s(e,t))};o(e,t,Array.prototype.slice.call(arguments,0))}},a=function(e){for(var t=0;t<m.length;t++)i(e,m[t],!1);for(var r=0;r<g.length;r++)i(e,g[r],!0)};r.invoked=!0;var c=t.createElement("script");c.type="text/javascript",c.integrity="sha384-PPfHw98myKtJkA9OdPBMQ6n8yvUaYk0EyUQccFSIQGmB05K6aAMZwvv8z50U2gT2",c.crossOrigin="anonymous",c.async=!0,c.src="https://cdn.amplitude.com/libs/analytics-browser-2.3.3-min.js.gz",c.onload=function(){e.amplitude.runQueuedFunctions||console.log("[Amplitude] Error: could not load SDK")};var u=t.getElementsByTagName("script")[0];u.parentNode.insertBefore(c,u);for(var l=function(){return this._q=[],this},p=["add","append","clearAll","prepend","set","setOnce","unset","preInsert","postInsert","remove","getUserProperties"],d=0;d<p.length;d++)n(l,p[d]);r.Identify=l;for(var f=function(){return this._q=[],this},v=["getEventProperties","setProductId","setQuantity","setPrice","setRevenue","setRevenueType","setEventProperties"],y=0;y<v.length;y++)n(f,v[y]);r.Revenue=f;var m=["getDeviceId","setDeviceId","getSessionId","setSessionId","getUserId","setUserId","setOptOut","setTransport","reset"],g=["init","add","remove","track","logEvent","identify","groupIdentify","setGroup","revenue","flush"];a(r),r.createInstance=function(e){return r._iq[e]={_q:[]},a(r._iq[e]),r._iq[e]},e.amplitude=r}}(window,document)}();

  amplitude.init(AMPLITUDE_KEY);
  console.log('[Analytics] Amplitude loaded');
})();
