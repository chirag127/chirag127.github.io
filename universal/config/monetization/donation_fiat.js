/**
 * Part 1: Monetization - Fiat Donations
 * @module config/monetization/donation_fiat
 */

export const donation_fiat = {
    buyMeACoffee: { username: 'chirag127', color: '#5F7FFF', emoji: '☕', message: 'Support!', enabled: true },  // YOUR ID
    kofi: { username: '', color: '#29abe0', enabled: true },
    paypal: { email: '', buttonId: '', currency: 'USD', enabled: true },
    patreon: { username: '', enabled: true },
    liberapay: { username: '', enabled: true }
};

export const donation_fiat_priority = ['buyMeACoffee', 'kofi', 'paypal', 'patreon', 'liberapay'];
