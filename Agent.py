import streamlit as st
from utils import apply_custom_theme

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="AI Insights",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_custom_theme()

# ---------- CUSTOM STYLES TO MATCH FIGMA ----------
st.markdown(
    """

<style>
/* Container for the whole insights panel */
.ai-panel {
    background: #020814;
    border-radius: 18px;
    border: 1px solid #1f2933;
    padding: 1.5rem 1.75rem;
    position: relative;
    margin-top: 0.75rem;
    box-shadow: 0 22px 50px rgba(0,0,0,0.65);
}

/* Green left border like Figma */
.ai-panel::before {
    content: "";
    position: absolute;
    left: 0;
    top: 14px;
    bottom: 14px;
    width: 3px;
    border-radius: 999px;
    background: linear-gradient(180deg, #16a34a, #22c55e);
}

/* Section headings */
.ai-section-title {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 0.15rem;
}

.ai-section-title span.icon {
    background: rgba(34,197,94,0.1);
    color: #22c55e;
    width: 24px;
    height: 24px;
    border-radius: 999px;
    display: grid;
    place-items: center;
    font-size: 14px;
}

.ai-section-sub {
    font-size: 0.8rem;
    color: #9ca3af;
    margin-bottom: 0.9rem;
}

/* Insight cards */
.insight-card {
    background: #050b16;
    border-radius: 14px;
    border: 1px solid #111827;
    padding: 0.9rem 1rem 0.85rem;
    display: grid;
    grid-template-columns: auto 1fr auto;
    gap: 0.9rem;
    align-items: flex-start;
    margin-bottom: 0.7rem;
}

.insight-avatar {
    width: 32px;
    height: 32px;
    border-radius: 999px;
    display: grid;
    place-items: center;
    font-size: 18px;
    background: #022c22;
    color: #6ee7b7;
}

.insight-content-title {
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.1rem;
}

.insight-content-body {
    font-size: 0.78rem;
    color: #d1d5db;
    margin-bottom: 0.35rem;
}

.insight-content-meta {
    font-size: 0.78rem;
    color: #22c55e;
    font-weight: 500;
    margin-bottom: 0.4rem;
}

/* Right-hand meta column */
.insight-meta-col {
    text-align: right;
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
    align-items: flex-end;
}

/* Priority badges */
.badge-priority-high,
.badge-priority-med {
    font-size: 0.68rem;
    padding: 0.18rem 0.55rem;
    border-radius: 999px;
    text-transform: capitalize;
}

.badge-priority-high {
    background: rgba(248,113,113,0.08);
    color: #fecaca;
    border: 1px solid rgba(248,113,113,0.5);
}

.badge-priority-med {
    background: rgba(250,204,21,0.08);
    color: #facc15;
    border: 1px solid rgba(234,179,8,0.5);
}

/* Action buttons on cards */
.card-cta {
    font-size: 0.75rem;
    padding: 0.25rem 0.8rem;
    border-radius: 999px;
    border: 0;
    background: #16a34a;
    color: #022c22;
    font-weight: 600;
    cursor: pointer;
}

.card-cta.secondary {
    background: #111827;
    color: #e5e7eb;
    border: 1px solid #374151;
}

/* Confidence label + mini chat icon row */
.confidence-row {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.7rem;
    color: #9ca3af;
}

.chat-bubble-mini {
    width: 20px;
    height: 20px;
    border-radius: 999px;
    background: #022c22;
    color: #a7f3d0;
    display: grid;
    place-items: center;
    font-size: 11px;
}

/* Progress bar */
.conf-bar {
    width: 100%;
    height: 4px;
    border-radius: 999px;
    background: #020617;
    overflow: hidden;
}

.conf-bar-fill {
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, #22c55e, #4ade80);
}

/* Header row */
.ai-header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.ai-header-title {
    font-size: 1.2rem;
    font-weight: 600;
}

.ai-header-sub {
    font-size: 0.8rem;
    color: #9ca3af;
}

/* Generate report button */
.btn-generate-report {
    background: #16a34a;
    border-radius: 999px;
    padding: 0.4rem 0.95rem;
    border: 0;
    font-size: 0.8rem;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    cursor: pointer;
}

/* Top pill switch (Performance vs All Recommendations) */
.rec-toggle {
    display: flex;
    background: #020617;
    border-radius: 999px;
    padding: 0.18rem;
    margin-bottom: 0.8rem;
    border: 1px solid #111827;
    width: fit-content;
}

.rec-pill {
    padding: 0.3rem 0.9rem;
    font-size: 0.75rem;
    border-radius: 999px;
    color: #e5e7eb;
}

.rec-pill.active {
    background: linear-gradient(90deg,#a855f7,#ec4899);
    color: #020617;
    font-weight: 600;
}
.rec-pill.inactive {
    color: #9ca3af;
}

/* Growth recommendation cards */
.growth-card {
    background: #050b16;
    border-radius: 14px;
    border: 1px solid #111827;
    padding: 0.9rem 1rem 0.85rem;
    display: grid;
    grid-template-columns: 1.8fr auto;
    gap: 0.6rem;
    margin-bottom: 0.7rem;
}

.growth-title {
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 0.15rem;
}

.growth-body {
    font-size: 0.78rem;
    color: #d1d5db;
    margin-bottom: 0.35rem;
}

.growth-meta {
    font-size: 0.75rem;
    color: #9ca3af;
}

.growth-meta span.label {
    color: #6b7280;
}

.growth-right {
    text-align: right;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 0.35rem;
}

.badge-effort {
    font-size: 0.7rem;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    background: rgba(250,204,21,0.08);
    color: #facc15;
    border: 1px solid rgba(250,204,21,0.5);
}

.badge-effort.low {
    background: rgba(52,211,153,0.08);
    color: #6ee7b7;
    border-color: rgba(52,211,153,0.5);
}

.badge-impact {
    font-size: 0.72rem;
    padding: 0.18rem 0.7rem;
    border-radius: 999px;
    background: rgba(22,163,74,0.12);
    color: #bbf7d0;
    border: 1px solid rgba(34,197,94,0.6);
}

/* small chat icon on growth cards */
.growth-chat {
    width: 22px;
    height: 22px;
    border-radius: 999px;
    background: #022c22;
    color: #a7f3d0;
    display: grid;
    place-items: center;
    font-size: 11px;
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------- HEADER ----------
header_left, header_right = st.columns([4, 1])

with header_left:
    st.markdown(
        """
<div class="ai-header-row">
  <div>
    <div class="ai-header-title">AI Insights</div>
    <div class="ai-header-sub">
      AI-powered recommendations and predictions for your business.
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

with header_right:
    st.write("")
    st.write("")
    chat_clicked = st.button("💬 Chat with GURU!", key="chat_with_guru")

    if chat_clicked:
        st.switch_page("AIAgent.py")


st.markdown("---")

# ---------- TABS ----------
tab_alerts, tab_recs = st.tabs(["Key Insights & Alerts", "All Recommendations"])

# ---------- TAB 1: KEY INSIGHTS & ALERTS ----------
with tab_alerts:
    st.markdown(
        """
<div class="ai-panel">
  <div class="ai-section-title">
    <span class="icon">💡</span>
    <span>Key Insights &amp; Alerts</span>
  </div>
  <div class="ai-section-sub">
    AI-generated insights based on your recent sales, inventory, and staffing data.
  </div>

  <!-- Card 1 -->
  <div class="insight-card">
    <div class="insight-avatar">🥤</div>
    <div>
      <div class="insight-content-title">Increase Coca-Cola Classic Inventory</div>
      <div class="insight-content-body">
        Coca-Cola Classic 24-packs are selling 40% faster than predicted.
        Consider increasing stock by <b>60 units</b> to avoid stockouts.
      </div>
      <div class="insight-content-meta">
        Potential revenue increase of <b>$900</b>
      </div>
      <div class="conf-bar">
        <div class="conf-bar-fill" style="width: 92%;"></div>
      </div>
    </div>
    <div class="insight-meta-col">
      <span class="badge-priority-high">high Priority</span>
      <button class="card-cta">Reorder now</button>
      <div class="confidence-row">
        <span>92% confidence</span>
        <div class="chat-bubble-mini">💬</div>
      </div>
    </div>
  </div>

  <!-- Card 2 -->
  <div class="insight-card">
    <div class="insight-avatar">🧃</div>
    <div>
      <div class="insight-content-title">Dr Pepper Stock Critical</div>
      <div class="insight-content-body">
        Current sales velocity will exhaust <b>Dr Pepper 6-pack</b> stock in
        approximately <b>3 days</b>. Immediate reorder recommended.
      </div>
      <div class="insight-content-meta">
        Potential lost sales: <b>$350</b>
      </div>
      <div class="conf-bar">
        <div class="conf-bar-fill" style="width: 88%;"></div>
      </div>
    </div>
    <div class="insight-meta-col">
      <span class="badge-priority-high">high Priority</span>
      <button class="card-cta">Urgent restock</button>
      <div class="confidence-row">
        <span>88% confidence</span>
        <div class="chat-bubble-mini">💬</div>
      </div>
    </div>
  </div>

  <!-- Card 3 -->
  <div class="insight-card">
    <div class="insight-avatar">⏰</div>
    <div>
      <div class="insight-content-title">Peak Hours Staffing</div>
      <div class="insight-content-body">
        Soda sales peak between <b>12–2 PM</b>. Consider adding
        <b>+1 staff member</b> during these hours to reduce lines and missed sales.
      </div>
      <div class="insight-content-meta">
        Estimated <b>15% reduction</b> in wait times
      </div>
      <div class="conf-bar">
        <div class="conf-bar-fill" style="width: 85%;"></div>
      </div>
    </div>
    <div class="insight-meta-col">
      <span class="badge-priority-med">medium Priority</span>
      <button class="card-cta secondary">Schedule review</button>
      <div class="confidence-row">
        <span>85% confidence</span>
        <div class="chat-bubble-mini">💬</div>
      </div>
    </div>
  </div>

  <!-- Card 4 -->
  <div class="insight-card">
    <div class="insight-avatar">🌞</div>
    <div>
      <div class="insight-content-title">Summer Seasonal Demand</div>
      <div class="insight-content-body">
        Warmer weather is driving increased demand for
        <b>citrus and fruit sodas</b>. Consider a front-of-store display
        for Fanta, Sprite, and Mountain Dew.
      </div>
      <div class="insight-content-meta">
        Projected <b>+18% lift</b> vs. baseline over the next 4 weeks
      </div>
      <div class="conf-bar">
        <div class="conf-bar-fill" style="width: 80%;"></div>
      </div>
    </div>
    <div class="insight-meta-col">
      <span class="badge-priority-med">medium Priority</span>
      <button class="card-cta secondary">Plan promotion</button>
      <div class="confidence-row">
        <span>80% confidence</span>
        <div class="chat-bubble-mini">💬</div>
      </div>
    </div>
  </div>

</div>
""",
        unsafe_allow_html=True,
    )

# ---------- TAB 2: PERFORMANCE PREDICTIONS / ALL RECOMMENDATIONS ----------
with tab_recs:
    st.markdown(
        """
<div class="ai-panel">
  <div class="rec-toggle">
    <div class="rec-pill inactive">⚙ Performance Predictions</div>
    <div class="rec-pill active">⚡ All Recommendations</div>
  </div>

  <div class="ai-section-title">
    <span class="icon">💲</span>
    <span>Growth Recommendations</span>
  </div>
  <div class="ai-section-sub">
    Actionable strategies suggested by GURU to boost soda revenue and reduce costs.
  </div>

  <!-- Growth card 1 -->
  <div class="growth-card">
    <div>
      <div class="growth-title">Dynamic Pricing for Premium Sodas</div>
      <div class="growth-body">
        Implement time-based pricing to maximize revenue during
        <b>peak evening hours</b> for specialty and energy drinks.
      </div>
      <div class="growth-meta">
        <span class="label">Category:</span> Pricing Strategy<br/>
        <span class="label">Timeline:</span> 2–3 weeks
      </div>
    </div>
    <div class="growth-right">
      <span class="badge-effort">Medium Effort</span>
      <span class="badge-impact">+8–12% revenue</span>
      <div style="display:flex; align-items:center; gap:0.3rem;">
        <button class="card-cta">Implement</button>
        <div class="growth-chat">💬</div>
      </div>
    </div>
  </div>

  <!-- Growth card 2 -->
  <div class="growth-card">
    <div>
      <div class="growth-title">Just-in-Time Ordering for Soft Drinks</div>
      <div class="growth-body">
        Reduce holding costs by implementing automated reorder points
        for <b>fast-moving cola and citrus SKUs</b> based on real sales velocity.
      </div>
      <div class="growth-meta">
        <span class="label">Category:</span> Inventory Optimization<br/>
        <span class="label">Timeline:</span> 1 week
      </div>
    </div>
    <div class="growth-right">
      <span class="badge-effort low">Low Effort</span>
      <span class="badge-impact">+5–8% revenue</span>
      <div style="display:flex; align-items:center; gap:0.3rem;">
        <button class="card-cta">Implement</button>
        <div class="growth-chat">💬</div>
      </div>
    </div>
  </div>

  <!-- Growth card 3 -->
  <div class="growth-card">
    <div>
      <div class="growth-title">Loyalty Program for Frequent Buyers</div>
      <div class="growth-body">
        Target repeat customers with personalized <b>soda bundle offers</b>
        and refill reminders based on purchase history.
      </div>
      <div class="growth-meta">
        <span class="label">Category:</span> Customer Experience<br/>
        <span class="label">Timeline:</span> 3–4 weeks
      </div>
    </div>
    <div class="growth-right">
      <span class="badge-effort">Medium Effort</span>
      <span class="badge-impact">+10–15% lifetime value</span>
      <div style="display:flex; align-items:center; gap:0.3rem;">
        <button class="card-cta">Implement</button>
        <div class="growth-chat">💬</div>
      </div>
    </div>
  </div>

</div>
""",
        unsafe_allow_html=True,
    )

