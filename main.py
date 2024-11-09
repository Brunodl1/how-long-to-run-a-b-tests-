import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Define discrete confidence levels and their z-scores
confidence_levels = {
    0.80: 1.28,
    0.85: 1.44,
    0.90: 1.645,
    0.95: 1.96,
    0.99: 2.576
}

def calculate_sample_size(baseline_conversion, improvement, confidence_level, power=0.8):
    p1 = baseline_conversion
    p2 = baseline_conversion * (1 + improvement)
    z_alpha = confidence_levels[confidence_level]  # Use the new dictionary
    z_beta = 0.84
    n = ((z_alpha * np.sqrt(2 * p1 * (1 - p1)) + z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2) / ((p1 - p2) ** 2)
    return int(np.ceil(n))

# Set the dark background style
plt.style.use('dark_background')

# Create figure with single plot
fig, ax = plt.subplots(figsize=(12, 7))
plt.subplots_adjust(bottom=0.3)  # More room for sliders

# Create slider axes
ax_baseline = plt.axes([0.15, 0.15, 0.65, 0.03])
ax_confidence = plt.axes([0.15, 0.11, 0.65, 0.03])
ax_traffic = plt.axes([0.15, 0.07, 0.65, 0.03])
ax_variants = plt.axes([0.15, 0.03, 0.65, 0.03])

# Create sliders
s_baseline = Slider(ax_baseline, 'Baseline Conv', 0.5, 15.0, valinit=1.5, valfmt='%.1f%%')
s_confidence = Slider(
    ax_confidence,
    'Confidence',
    80,
    99,
    valinit=95,
    valstep=[80, 85, 90, 95, 99],  # Discrete steps
    valfmt='%d%%'  # Format as percentage
)
s_traffic = Slider(ax_traffic, 'Monthly Traffic', 5000, 30000, valinit=6000, valfmt='%0.0f')
s_variants = Slider(ax_variants, 'Variants', 2, 5, valinit=2, valfmt='%0.0f')

def update(val):
    ax.clear()

    baseline = s_baseline.val / 100
    confidence = s_confidence.val / 100
    monthly_traffic = s_traffic.val
    daily_traffic = monthly_traffic / 30  # Convert monthly to daily for calculations
    num_variants = int(s_variants.val)

    improvements = np.linspace(0.05, 0.3, 100)
    sample_sizes = [calculate_sample_size(baseline, imp, confidence) for imp in improvements]
    test_duration_weeks = [(num_variants * size) / monthly_traffic / 4 for size in sample_sizes]

    ax.plot(improvements * 100, test_duration_weeks, color='cyan', linewidth=2)
    ax.set_xlabel('Expected Improvement (%)')
    ax.set_ylabel('Test Duration (weeks)')
    ax.set_title(f'A/B Test Duration Calculator\nBaseline Conv: {baseline*100:.1f}%, Confidence: {confidence:.0%}, '
                f'Traffic: {monthly_traffic:,.0f}/month, Variants: {num_variants}')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(5, 30)

    ax.axhline(y=1, color='r', linestyle='--', alpha=0.3, label='1 week')
    ax.axhline(y=2, color='y', linestyle='--', alpha=0.3, label='2 weeks')
    ax.axhline(y=4, color='g', linestyle='--', alpha=0.3, label='4 weeks')

    ax.legend()

    fig.canvas.draw_idle()

# Register the update function with the sliders
s_baseline.on_changed(update)
s_confidence.on_changed(update)
s_traffic.on_changed(update)
s_variants.on_changed(update)

# Initial plot
update(None)

plt.show()