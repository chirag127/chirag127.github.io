/**
 * GrowthBook A/B Testing Integration (Client-Side)
 *
 * Lightweight multi-armed bandit implementation for polymorph A/B testing.
 * Uses localStorage for persistence on static sites.
 *
 * Features:
 * - Visitor ID persistence for consistent bucketing
 * - Multi-armed bandit with Thompson Sampling
 * - Conversion tracking
 * - Auto-optimization to show best variants more often
 *
 * Free tier: No backend required
 * Best for: Static GitHub Pages sites
 */

export const name = 'GrowthBook';
export const configKey = 'growthbook';

const STORAGE_KEYS = {
    visitorId: 'gb_visitor_id',
    experimentData: 'gb_polymorph_ab',
    manualOverride: 'gb_polymorph_override'
};

/**
 * Generate UUID v4 for visitor identification
 */
function generateVisitorId() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

/**
 * Get or create visitor ID for consistent bucketing
 */
function getVisitorId() {
    let visitorId = localStorage.getItem(STORAGE_KEYS.visitorId);
    if (!visitorId) {
        visitorId = generateVisitorId();
        localStorage.setItem(STORAGE_KEYS.visitorId, visitorId);
    }
    return visitorId;
}

/**
 * Get experiment data from localStorage
 */
function getExperimentData() {
    try {
        const data = localStorage.getItem(STORAGE_KEYS.experimentData);
        return data ? JSON.parse(data) : null;
    } catch (e) {
        console.warn('[GrowthBook] Failed to parse experiment data:', e);
        return null;
    }
}

/**
 * Save experiment data to localStorage
 */
function saveExperimentData(data) {
    try {
        localStorage.setItem(STORAGE_KEYS.experimentData, JSON.stringify(data));
    } catch (e) {
        console.warn('[GrowthBook] Failed to save experiment data:', e);
    }
}

/**
 * Thompson Sampling for Multi-Armed Bandit
 * Uses Beta distribution approximation for each variant
 */
function thompsonSample(successes, failures) {
    // Simple approximation of Beta distribution sampling
    // Returns value between 0 and 1
    const alpha = successes + 1;
    const beta = failures + 1;

    // Use gamma function approximation for beta sampling
    let sum = 0;
    for (let i = 0; i < alpha; i++) {
        sum += -Math.log(Math.random());
    }
    let sum2 = 0;
    for (let i = 0; i < beta; i++) {
        sum2 += -Math.log(Math.random());
    }
    return sum / (sum + sum2);
}

/**
 * Select variant using multi-armed bandit (Thompson Sampling)
 */
function selectVariantBandit(variants, stats) {
    let bestScore = -1;
    let bestVariant = variants[0];

    for (const variant of variants) {
        const variantStats = stats[variant.id] || { impressions: 0, conversions: 0 };
        const successes = variantStats.conversions;
        const failures = variantStats.impressions - variantStats.conversions;
        const score = thompsonSample(successes, failures);

        if (score > bestScore) {
            bestScore = score;
            bestVariant = variant;
        }
    }

    return bestVariant;
}

/**
 * Select variant using simple weighted random (for initial exploration)
 */
function selectVariantWeighted(variants) {
    const totalWeight = variants.reduce((sum, v) => sum + (v.weight || 1), 0);
    let random = Math.random() * totalWeight;

    for (const variant of variants) {
        random -= variant.weight || 1;
        if (random <= 0) return variant;
    }

    return variants[0];
}

/**
 * Main A/B Testing Controller
 */
export const growthbook = {
    loaded: false,
    config: null,
    currentVariant: null,
    experimentId: 'polymorph_ab_v1',

    /**
     * Initialize the A/B testing system
     */
    init(config, loadScript) {
        if (!config.enabled || this.loaded) return;

        this.config = config;
        const variants = config.polymorphVariants || [];

        if (variants.length === 0) {
            console.log('[GrowthBook] No variants configured, skipping');
            return;
        }

        // Check for manual override (user selected a specific polymorph)
        const manualOverride = localStorage.getItem(STORAGE_KEYS.manualOverride);
        if (manualOverride) {
            console.log('[GrowthBook] Manual override active:', manualOverride);
            this.currentVariant = variants.find(v => v.id === manualOverride) || variants[0];
            this.loaded = true;
            return;
        }

        // Get or initialize experiment data
        let expData = getExperimentData();
        const visitorId = getVisitorId();

        if (!expData) {
            expData = {
                visitorId: visitorId,
                experimentId: this.experimentId,
                assignedVariant: null,
                stats: {},
                createdAt: Date.now()
            };
        }

        // Check if visitor already has an assignment
        if (expData.assignedVariant && expData.visitorId === visitorId) {
            this.currentVariant = variants.find(v => v.id === expData.assignedVariant);
            if (this.currentVariant) {
                console.log('[GrowthBook] Returning visitor, assigned:', this.currentVariant.id);
                this.loaded = true;
                this.trackImpression(expData);
                this.maybeRedirect();
                return;
            }
        }

        // New visitor - select variant using bandit or weighted random
        const totalImpressions = Object.values(expData.stats).reduce(
            (sum, s) => sum + (s.impressions || 0), 0
        );

        // Use pure exploration for first 50 impressions, then bandit
        if (config.enableBandit && totalImpressions > 50) {
            this.currentVariant = selectVariantBandit(variants, expData.stats);
        } else {
            this.currentVariant = selectVariantWeighted(variants);
        }

        // Save assignment
        expData.assignedVariant = this.currentVariant.id;
        expData.visitorId = visitorId;
        saveExperimentData(expData);

        console.log('[GrowthBook] New visitor assigned:', this.currentVariant.id);

        this.loaded = true;
        this.trackImpression(expData);
        this.maybeRedirect();
    },

    /**
     * Track impression for current variant
     */
    trackImpression(expData) {
        if (!this.currentVariant) return;

        const variantId = this.currentVariant.id;
        if (!expData.stats[variantId]) {
            expData.stats[variantId] = { impressions: 0, conversions: 0 };
        }
        expData.stats[variantId].impressions++;
        saveExperimentData(expData);
    },

    /**
     * Track conversion (user clicked a tool card)
     */
    trackConversion() {
        if (!this.currentVariant) return;

        const expData = getExperimentData();
        if (!expData) return;

        const variantId = this.currentVariant.id;
        if (!expData.stats[variantId]) {
            expData.stats[variantId] = { impressions: 1, conversions: 0 };
        }
        expData.stats[variantId].conversions++;
        saveExperimentData(expData);

        console.log('[GrowthBook] Conversion tracked for:', variantId);

        // Also fire to analytics if available
        if (window.gtag) {
            window.gtag('event', 'ab_test_conversion', {
                experiment_id: this.experimentId,
                variant_id: variantId
            });
        }
        if (window.posthog) {
            window.posthog.capture('ab_test_conversion', {
                experiment_id: this.experimentId,
                variant_id: variantId
            });
        }
    },

    /**
     * Redirect to polymorph variant if not control
     */
    maybeRedirect() {
        if (!this.currentVariant || !this.currentVariant.slug) {
            // Control variant or no slug - stay on current page
            return;
        }

        // Check if we're already on the correct polymorph page
        const currentPath = window.location.pathname;
        const expectedPath = `/polymorphs/${this.currentVariant.slug}.html`;

        if (!currentPath.includes('/polymorphs/') && currentPath !== expectedPath) {
            // On main index, but assigned to a polymorph variant - redirect
            console.log('[GrowthBook] Redirecting to variant:', expectedPath);
            window.location.href = expectedPath;
        }
    },

    /**
     * Set manual override (called from Polymorphs sidebar)
     */
    setManualOverride(variantId) {
        if (variantId) {
            localStorage.setItem(STORAGE_KEYS.manualOverride, variantId);
        } else {
            localStorage.removeItem(STORAGE_KEYS.manualOverride);
        }
    },

    /**
     * Clear manual override and re-enter A/B test
     */
    clearManualOverride() {
        localStorage.removeItem(STORAGE_KEYS.manualOverride);
    },

    /**
     * Get current experiment stats (for debugging)
     */
    getStats() {
        const expData = getExperimentData();
        return expData ? expData.stats : {};
    },

    /**
     * Get current variant ID
     */
    getCurrentVariantId() {
        return this.currentVariant ? this.currentVariant.id : 'control';
    }
};

export default growthbook;
