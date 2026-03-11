document.addEventListener("DOMContentLoaded", () => {
  // =========================================================================
  // Tab navigation
  // =========================================================================
  const tabBtns = document.querySelectorAll(".tab-btn");
  const tabContents = document.querySelectorAll(".tab-content");

  tabBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      tabBtns.forEach((b) => b.classList.remove("active"));
      tabContents.forEach((c) => c.classList.add("hidden"));
      btn.classList.add("active");
      document.getElementById(`tab-${btn.dataset.tab}`).classList.remove("hidden");
    });
  });

  // =========================================================================
  // Activities tab
  // =========================================================================
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      activitiesList.innerHTML = "";

      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        activityCard.className = "activity-card";

        const spotsLeft = details.max_participants - details.participants.length;

        activityCard.innerHTML = `
          <h4>${name}</h4>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
        `;

        activitiesList.appendChild(activityCard);

        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        { method: "POST" }
      );

      const result = await response.json();

      if (response.ok) {
        messageDiv.textContent = result.message;
        messageDiv.className = "success";
        signupForm.reset();
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "error";
      }

      messageDiv.classList.remove("hidden");

      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // =========================================================================
  // Insights tab – sub-navigation
  // =========================================================================
  const subnavBtns = document.querySelectorAll(".subnav-btn");
  const insightsSections = document.querySelectorAll(".insights-section");

  subnavBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      subnavBtns.forEach((b) => b.classList.remove("active"));
      insightsSections.forEach((s) => s.classList.add("hidden"));
      btn.classList.add("active");
      document.getElementById(`section-${btn.dataset.section}`).classList.remove("hidden");
    });
  });

  // =========================================================================
  // Helper utilities
  // =========================================================================

  function sentimentBadge(sentiment) {
    const classes = { positive: "badge-positive", neutral: "badge-neutral", negative: "badge-negative" };
    return `<span class="badge ${classes[sentiment] || ""}">${sentiment}</span>`;
  }

  function sentimentBar(breakdown) {
    return `
      <div class="sentiment-bar">
        <div class="bar-positive" style="width:${breakdown.positive}%" title="Positive ${breakdown.positive}%"></div>
        <div class="bar-neutral"  style="width:${breakdown.neutral}%"  title="Neutral ${breakdown.neutral}%"></div>
        <div class="bar-negative" style="width:${breakdown.negative}%" title="Negative ${breakdown.negative}%"></div>
      </div>
      <div class="bar-legend">
        <span class="legend-positive">▇ Positive ${breakdown.positive}%</span>
        <span class="legend-neutral">▇ Neutral ${breakdown.neutral}%</span>
        <span class="legend-negative">▇ Negative ${breakdown.negative}%</span>
      </div>`;
  }

  // =========================================================================
  // Fan Sentiments
  // =========================================================================
  async function fetchFanSentiments() {
    try {
      const res = await fetch("/insights/fan-sentiments");
      const data = await res.json();
      const el = document.getElementById("fan-sentiments-content");

      const topicsHtml = data.top_topics.map((t) =>
        `<tr>
          <td>${t.topic}</td>
          <td>${sentimentBadge(t.sentiment)}</td>
          <td>${t.mentions.toLocaleString()}</td>
        </tr>`
      ).join("");

      const highlightsHtml = data.community_highlights.map((h) => `<li>${h}</li>`).join("");

      el.innerHTML = `
        <div class="insight-card">
          <h4>Overall Sentiment <span class="trend-badge">${data.overall.trend}</span></h4>
          <p>${data.overall.summary}</p>
          ${sentimentBar(data.overall)}
        </div>
        <div class="insight-card">
          <h4>Top Topics</h4>
          <table class="insight-table">
            <thead><tr><th>Topic</th><th>Sentiment</th><th>Mentions</th></tr></thead>
            <tbody>${topicsHtml}</tbody>
          </table>
        </div>
        <div class="insight-card">
          <h4>Community Highlights</h4>
          <ul>${highlightsHtml}</ul>
        </div>`;
    } catch (err) {
      document.getElementById("fan-sentiments-content").innerHTML = "<p>Failed to load fan sentiments.</p>";
      console.error(err);
    }
  }

  // =========================================================================
  // Driver Sentiments
  // =========================================================================
  async function fetchDriverSentiments() {
    try {
      const res = await fetch("/insights/driver-sentiments");
      const data = await res.json();
      const el = document.getElementById("driver-sentiments-content");

      el.innerHTML = Object.entries(data).map(([name, d]) => `
        <div class="insight-card">
          <h4>${name} ${sentimentBadge(d.overall_sentiment)}</h4>
          <p><strong>Fan Approval:</strong> ${d.fan_approval}% &nbsp;|&nbsp; <strong>Performance Rating:</strong> ${d.performance_rating}/10</p>
          <p>${d.key_insight}</p>
          ${sentimentBar(d.sentiment_breakdown)}
          <p class="tags">${d.trending_topics.map((t) => `<span class="tag">${t}</span>`).join("")}</p>
        </div>`
      ).join("");
    } catch (err) {
      document.getElementById("driver-sentiments-content").innerHTML = "<p>Failed to load driver sentiments.</p>";
      console.error(err);
    }
  }

  // =========================================================================
  // Team Sentiments
  // =========================================================================
  async function fetchTeamSentiments() {
    try {
      const res = await fetch("/insights/team-sentiments");
      const data = await res.json();
      const el = document.getElementById("team-sentiments-content");

      el.innerHTML = Object.entries(data).map(([name, d]) => `
        <div class="insight-card">
          <h4>${name} ${sentimentBadge(d.overall_sentiment)}</h4>
          <p><strong>Manufacturer:</strong> ${d.manufacturer} &nbsp;|&nbsp; <strong>Fan Support:</strong> ${d.fan_support}% &nbsp;|&nbsp; <strong>Performance:</strong> ${d.performance_rating}/10</p>
          ${sentimentBar(d.sentiment_breakdown)}
          <ul>${d.key_insights.map((i) => `<li>${i}</li>`).join("")}</ul>
        </div>`
      ).join("");
    } catch (err) {
      document.getElementById("team-sentiments-content").innerHTML = "<p>Failed to load team sentiments.</p>";
      console.error(err);
    }
  }

  // =========================================================================
  // Manufacturer Sentiments
  // =========================================================================
  async function fetchManufacturerSentiments() {
    try {
      const res = await fetch("/insights/manufacturer-sentiments");
      const data = await res.json();
      const el = document.getElementById("manufacturer-sentiments-content");

      el.innerHTML = Object.entries(data).map(([name, d]) => `
        <div class="insight-card">
          <h4>${name} ${sentimentBadge(d.overall_sentiment)}</h4>
          <p><strong>Brand Reputation:</strong> ${d.brand_reputation}/100 &nbsp;|&nbsp; <strong>Innovation Score:</strong> ${d.innovation_score}/10 &nbsp;|&nbsp; <strong>Market Perception:</strong> ${d.market_perception}</p>
          ${sentimentBar(d.sentiment_breakdown)}
          <ul>${d.key_insights.map((i) => `<li>${i}</li>`).join("")}</ul>
          <div class="industry-impact">
            <strong>Industry Impact:</strong> ${d.industry_impact}
          </div>
        </div>`
      ).join("");
    } catch (err) {
      document.getElementById("manufacturer-sentiments-content").innerHTML = "<p>Failed to load manufacturer sentiments.</p>";
      console.error(err);
    }
  }

  // =========================================================================
  // Technical Innovations
  // =========================================================================
  async function fetchTechnicalInnovations() {
    try {
      const res = await fetch("/insights/technical-innovations");
      const data = await res.json();
      const el = document.getElementById("innovations-content");

      el.innerHTML = data.map((item) => `
        <div class="insight-card innovation-card">
          <h4>${item.name} <span class="category-badge">${item.category}</span></h4>
          <p>${item.description}</p>
          <div class="impact-grid">
            <div class="impact-box motorcycle">
              <strong>🏍️ Motorcycle Industry Impact</strong>
              <p>${item.motorcycle_industry_impact}</p>
            </div>
            <div class="impact-box manufacturing">
              <strong>🏭 Manufacturing Industry Impact</strong>
              <p>${item.manufacturing_industry_impact}</p>
            </div>
          </div>
          <p class="meta">Introduced: ${item.year_introduced} &nbsp;|&nbsp; Adoption: <strong>${item.adoption_rate}</strong></p>
        </div>`
      ).join("");
    } catch (err) {
      document.getElementById("innovations-content").innerHTML = "<p>Failed to load technical innovations.</p>";
      console.error(err);
    }
  }

  // =========================================================================
  // Initialise
  // =========================================================================
  fetchActivities();
  fetchFanSentiments();
  fetchDriverSentiments();
  fetchTeamSentiments();
  fetchManufacturerSentiments();
  fetchTechnicalInnovations();
});
