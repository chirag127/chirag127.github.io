/**
 * Rollbar Error Monitoring Provider
 * @module monitoring/rollbar
 */

export const name = 'rollbar';
export const configKey = 'rollbar';

export function init(config, loadScript) {
    if (!config.accessToken) return;

    var _rollbarConfig = {
        accessToken: config.accessToken,
        captureUncaught: true,
        captureUnhandledRejections: true,
        payload: {
            environment: config.environment || 'production',
            client: {
                javascript: {
                    source_map_enabled: true,
                    code_version: config.codeVersion || '1.0.0'
                }
            }
        }
    };

    !function(r){function e(n){if(o[n])return o[n].exports;var t=o[n]={exports:{},id:n,loaded:!1};return r[n].call(t.exports,t,t.exports,e),t.loaded=!0,t.exports}var o={};return e.m=r,e.c=o,e.p="",e(0)}([function(r,e,o){"use strict";var n=o(1),t=o(4);_rollbarConfig=_rollbarConfig||{},_rollbarConfig.rollbarJsUrl=_rollbarConfig.rollbarJsUrl||"https://cdn.rollbar.com/rollbarjs/refs/tags/v2.26.0/rollbar.min.js",_rollbarConfig.async=void 0===_rollbarConfig.async||_rollbarConfig.async;var a=n.setupShim(window,_rollbarConfig),l=t(_rollbarConfig);window.rollbar=n.Rollbar,a.loadFull(window,document,!_rollbarConfig.async,_rollbarConfig,l)}]);

    // Load Rollbar script
    loadScript('https://cdn.rollbar.com/rollbarjs/refs/tags/v2.26.0/rollbar.min.js')
        .then(() => {
            if (window.Rollbar) {
                Rollbar.init(_rollbarConfig);
            }
        });
}
