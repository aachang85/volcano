import streamlit as st
import feedparser
import time

# Set up clean, mobile-friendly page layout
st.set_page_config(
    page_title="Kīlauea Episode 49 Tracker",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("🌋 Kīlauea Summit Real-Time Monitor")
st.caption("Tracking short-term indicators for Episode 49 | Data sourced directly from USGS HVO")

# ---------------------------------------------------------
# SECTION 1: CRITICAL RECENT ALERTS (USGS HANS RSS FEED)
# ---------------------------------------------------------
st.header("1. Latest USGS Activity Notices")

@st.cache_data(ttl=300)  # Cache for 5 minutes to avoid spamming the feed
def fetch_usgs_alerts():
    # USGS Volcano Activity Notices RSS feed
    feed_url = "https://volcanoes.usgs.gov/hans2/rss/feed"
    feed = feedparser.parse(feed_url)
    hvo_alerts = []
    
    for entry in feed.entries:
        # Filter for Hawaiian Volcano Observatory alerts
        if "HVO" in entry.title or "Kilauea" in entry.title:
            hvo_alerts.append({
                "title": entry.title,
                "updated": entry.updated,
                "link": entry.link
            })
    return hvo_alerts[:3]  # Return top 3 most recent

try:
    alerts = fetch_usgs_alerts()
    if alerts:
        for alert in alerts:
            with st.expander(f"🔔 {alert['title']}", expanded=True):
                st.write(f"**Published:** {alert['updated']}")
                st.markdown(f"[View Full Official Notice]({alert['link']})")
    else:
        st.info("No recent high-priority HVO alerts. Status is likely still 'Paused'.")
except Exception as e:
    st.warning("Could not refresh live RSS feed. Check network connection.")

st.markdown("---")

# ---------------------------------------------------------
# SECTION 2: THE REAL-TIME SHORT TERM INDICATORS
# ---------------------------------------------------------
st.header("2. Short-Term Eruption Indicators")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Summit Tiltmeter (UWD)")
    st.markdown(
        "**What to watch for:** Look for the line to bend **sharply downward**. "
        "A rapid drop means the subsurface plug has failed, and magma is rushing up. "
        "Fountaining usually starts 30-90 minutes after the drop begins."
    )
    # Direct live URL to the past 2 days tilt plot at Uēkahuna (UWD)
# Direct live URL to the past 2 days tilt plot at Uēkahuna (UWD)
    tilt_url = "https://volcanoes.usgs.gov/vsc/images/vsc_images/KILAUEA_summit_tilt_2day.png"
    st.image(tilt_url, caption="Real-time 2-Day Summit Tilt (UWD) - Refresh page to update", use_container_width=True)

with col2:
    st.subheader("Live Thermal Rim View (K2cam)")
    st.markdown(
        "**What to watch for:** Look for minor glowing **precursor overflows** "
        "around the vents or a sudden bright white/pink flash indicating the floor is flooding."
    )
    # Direct live URL to the thermal webcam
    thermal_cam_url = "https://volcanoes.usgs.gov/vsc/captures/kilauea/k2cam.jpg"
    st.image(thermal_cam_url, caption="Live Halemaʻumaʻu Thermal Webcam", use_container_width=True)

# ---------------------------------------------------------
# SECTION 3: VISUAL CONFIRMATION & SAFETY QUICK-LINKS
# ---------------------------------------------------------
st.markdown("---")
st.header("3. Visual Confirmation & Quick Links")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Visual Wide-Angle (V1cam)")
    # Direct live URL to the visual webcam looking into the caldera
    visual_cam_url = "https://volcanoes.usgs.gov/vsc/captures/kilauea/v1cam.jpg"
    st.image(visual_cam_url, caption="Live Summit Caldera Wide View", use_container_width=True)

with col4:
    st.subheader("Essential Mobile Bookmarks")
    st.markdown("""
    Keep these links open on your phone browser for quick refreshing while on the trails:
    *   [USGS Kīlauea Real-Time Monitoring Page](https://www.usgs.gov/volcanoes/kilauea/monitoring-data)
    *   [HVO Daily Written Updates](https://www.usgs.gov/volcanoes/kilauea/volcano-updates)
    *   [Hawaiʻi Volcanoes National Park Temporary Closures](https://www.nps.gov/havo/planyourvisit/conditions.htm)
    """)
    
    # Simple manual refresh button for the cached elements
    if st.button("🔄 Force Refresh Dashboard Data"):
        st.cache_data.clear()
        st.rerun()