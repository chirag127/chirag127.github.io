/**
 * Visual A/B Experiments Module
 * Handles specific visual experiments: Button Colors, Layouts, CTA Text.
 * @module integrations/engagement/ab_testing/experiments
 */

/**
 * Run all visual experiments
 * @param {Object} growthbook - The initialized GrowthBook SDK instance
 */
export function runVisualExperiments(growthbook) {
    if (!growthbook || typeof growthbook.getFeatureValue !== 'function') {
        return;
    }

    console.log('[APEX Experiments] Running visual experiments...');

    // 1. Button Color Experiment
    // Feature key: 'button_color_test'
    const buttonColor = growthbook.getFeatureValue('button_color_test', 'default');
    if (buttonColor !== 'default') {
        const buttons = document.querySelectorAll('button, .btn, input[type="submit"], [role="button"]');
        buttons.forEach(btn => {
            // Respect existing classes but override specifics
            switch (buttonColor) {
                case 'variant_a': // Purple/Blue Gradient
                    btn.style.background = 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)';
                    btn.style.boxShadow = '0 8px 32px rgba(102, 126, 234, 0.4)';
                    btn.style.borderColor = 'transparent';
                    break;
                case 'variant_b': // Pink/Red Gradient
                    btn.style.background = 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)';
                    btn.style.boxShadow = '0 8px 32px rgba(240, 147, 251, 0.4)';
                    btn.style.borderColor = 'transparent';
                    break;
                case 'variant_c': // Blue/Cyan Gradient
                    btn.style.background = 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)';
                    btn.style.boxShadow = '0 8px 32px rgba(79, 172, 254, 0.4)';
                    btn.style.borderColor = 'transparent';
                    break;
            }
        });
    }

    // 2. Layout Density Experiment
    // Feature key: 'layout_test'
    const layout = growthbook.getFeatureValue('layout_test', 'default');
    if (layout === 'compact') {
        document.body.style.fontSize = '0.9rem';
        document.documentElement.style.setProperty('--spacing-unit', '0.8rem');
    } else if (layout === 'spacious') {
        document.body.style.fontSize = '1.1rem';
        document.documentElement.style.setProperty('--spacing-unit', '1.5rem');
    }

    // 3. CTA Text Experiment
    // Feature key: 'cta_text_test'
    const ctaText = growthbook.getFeatureValue('cta_text_test', 'default');
    if (ctaText !== 'default') {
        const ctaElements = document.querySelectorAll('[data-cta], .cta, button[type="submit"]');
        ctaElements.forEach(el => {
            const original = el.textContent.trim();
            // regex to replace common action verbs
            if (ctaText === 'urgent') {
                el.textContent = original.replace(/Get|Start|Try|Download|Use/i, 'Get Instant');
            } else if (ctaText === 'benefit') {
                el.textContent = original.replace(/Get|Start|Try|Download|Use/i, 'Unlock Free');
            }
        });
    }

    // 4. Color Scheme Experiment
    // Feature key: 'color_scheme_test'
    const colorScheme = growthbook.getFeatureValue('color_scheme_test', 'default');
    if (colorScheme !== 'default') {
        const root = document.documentElement;
        switch(colorScheme) {
            case 'warm':
                root.style.setProperty('--primary-color', '#ff6b6b');
                root.style.setProperty('--secondary-color', '#feca57');
                break;
            case 'cool':
                root.style.setProperty('--primary-color', '#3742fa');
                root.style.setProperty('--secondary-color', '#2ed573');
                break;
            case 'monochrome':
                root.style.setProperty('--primary-color', '#2f3542');
                root.style.setProperty('--secondary-color', '#57606f');
                break;
        }
    }
}
