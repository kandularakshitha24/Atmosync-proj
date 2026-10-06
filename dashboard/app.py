import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AtmoSync | Supply Chain Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM DARK THEME
# ============================================================

st.markdown("""
<style>

    .stApp {
        background: #0b0f14;
        color: #f4f7fa;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1500px;
    }

    section[data-testid="stSidebar"] {
    background-color: #111820 !important;
    border-right: 2px solid #34404d !important;
    min-width: 280px !important;
    width: 280px !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem !important;
}

section[data-testid="stSidebar"] * {
    color: #f5f7fa !important;
}

    .brand {
        font-size: 28px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #f4f7fa;
    }

    .brand-subtitle {
        font-size: 12px;
        color: #7f8b99;
        letter-spacing: 1.5px;
        margin-top: -5px;
    }

    .page-title {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: -0.5px;
        margin-bottom: 3px;
    }

    .page-subtitle {
        color: #8995a3;
        font-size: 14px;
        margin-bottom: 28px;
    }

    .status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #111a17;
        border: 1px solid #24372f;
        padding: 7px 12px;
        border-radius: 20px;
        color: #9ed7b8;
        font-size: 12px;
        font-weight: 600;
    }

    .status-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background: #56c596;
        display: inline-block;
    }

    .metric-card {
        background: #11161d;
        border: 1px solid #202832;
        border-radius: 14px;
        padding: 20px 22px;
        min-height: 120px;
    }

    .metric-label {
        color: #7f8b99;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
    }

    .metric-value {
        color: #f4f7fa;
        font-size: 32px;
        font-weight: 700;
        margin-top: 8px;
    }

    .metric-caption {
        color: #687583;
        font-size: 12px;
        margin-top: 5px;
    }

    .section-title {
        font-size: 18px;
        font-weight: 650;
        margin-top: 30px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #71808e;
        font-size: 12px;
        margin-bottom: 15px;
    }

    .alert-card {
        background: #151318;
        border: 1px solid #392c32;
        border-left: 3px solid #d96c73;
        border-radius: 10px;
        padding: 15px 18px;
        margin-bottom: 10px;
    }

    .alert-title {
        color: #f1d7da;
        font-size: 13px;
        font-weight: 650;
    }

    .alert-detail {
        color: #7f8995;
        font-size: 12px;
        margin-top: 4px;
    }

    .telemetry-card {
        background: #11161d;
        border: 1px solid #202832;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #202832;
        border-radius: 12px;
        overflow: hidden;
    }

    .stButton > button {
        border-radius: 8px;
        border: 1px solid #29333e;
        background: #151b23;
        color: #dbe2e8;
    }

    .stButton > button:hover {
        border-color: #566474;
        color: #ffffff;
    }

/* ============================================================
   PREMIUM SIDEBAR NAVIGATION
   ============================================================ */

.nav-heading {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.8px;
    color: #7f8b99;
    margin: 8px 0 12px 4px;
}

.nav-divider {
    height: 1px;
    background: #202832;
    margin: 18px 0;
}

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 6px;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label {
    background: transparent !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 11px 12px !important;
    margin: 0 0 5px 0 !important;
    transition: all 0.2s ease;
    cursor: pointer;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
    background: #18212b !important;
    border-color: #273341 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
    background: #1b2632 !important;
    border-color: #344353 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) p {
    color: #ffffff !important;
    font-weight: 700 !important;
}

section[data-testid="stSidebar"] div[role="radiogroup"] label p {
    color: #aeb8c4 !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}

.sidebar-spacer {
    height: 30px;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATA
# ============================================================

SUMMARY_PATH = "data/processed/dashboard_container_summary.csv"
TELEMETRY_PATH = "data/processed/kafka_processed_telemetry.csv"


# Load container summary
try:
    data = pd.read_csv(SUMMARY_PATH)

except FileNotFoundError:
    st.error(
        f"Dashboard summary file not found: {SUMMARY_PATH}"
    )
    st.stop()


# Load telemetry data
try:
    telemetry = pd.read_csv(TELEMETRY_PATH)

except FileNotFoundError:
    st.error(
        f"Telemetry file not found: {TELEMETRY_PATH}"
    )
    st.stop()


# ============================================================
# DATA CLEANING
# ============================================================

telemetry["TIMESTAMP"] = pd.to_datetime(
    telemetry["timestamp"],
    errors="coerce"
)

telemetry["TEMPERATURE"] = pd.to_numeric(
    telemetry["temperature"],
    errors="coerce"
)

telemetry["HUMIDITY"] = pd.to_numeric(
    telemetry["humidity"],
    errors="coerce"
)

telemetry["VIBRATION"] = pd.to_numeric(
    telemetry["vibration"],
    errors="coerce"
)


# ============================================================
# SPOILAGE SCORE CALCULATION
# ============================================================

def calculate_spoilage_score(row):

    temperature = row["TEMPERATURE"]
    humidity = row["HUMIDITY"]

    if temperature > 30 and humidity > 75:
        return 80

    elif temperature > 30 or humidity > 75:
        return 40

    return 0


telemetry["SPOILAGE_SCORE"] = telemetry.apply(
    calculate_spoilage_score,
    axis=1
)


telemetry["SPOILAGE_LEVEL"] = telemetry[
    "SPOILAGE_SCORE"
].map({
    0: "LOW",
    40: "MEDIUM",
    80: "HIGH"
})


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # ============================================================
    # ATMOSYNC BRAND
    # ============================================================

    st.markdown(
        '<div class="brand">ATMOSYNC</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="brand-subtitle">'
        'MICRO-CLIMATE INTELLIGENCE'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)

    # ============================================================
    # NAVIGATION
    # ============================================================

    st.markdown(
        '<div class="nav-heading">CONTROL TOWER</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "NAVIGATION",
        [
            "Executive Overview",
            "Container Intelligence",
            "Analytics"
        ],
        key="dashboard_page",
        label_visibility="collapsed"
    )

    st.markdown("<div class='nav-divider'></div>", unsafe_allow_html=True)

    # ============================================================
    # SYSTEM STATUS
    # ============================================================

    st.markdown(
        '<div class="nav-heading">SYSTEM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="status">'
        '<span class="status-dot"></span>'
        '<span>SYSTEM OPERATIONAL</span>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown("<div class='sidebar-spacer'></div>", unsafe_allow_html=True)

    st.caption("AtmoSync v1.0")
    st.caption("Supply Chain Risk Intelligence")


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="page-title">'
    'Supply Chain Control Tower'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="page-subtitle">'
    'Micro-climate intelligence for perishable agricultural logistics'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="status">'
    '<span class="status-dot"></span>'
    'LIVE TELEMETRY MONITORING'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# KPI CALCULATIONS
# ============================================================

total_containers = len(data)

high_risk = len(
    data[data["OVERALL_RISK"] == "HIGH"]
)

medium_risk = len(
    data[data["OVERALL_RISK"] == "MEDIUM"]
)

avg_score = data["AVG_SPOILAGE_SCORE"].mean()

total_risk_events = data["RISK_EVENTS"].sum()

total_telemetry = len(telemetry)

high_risk_readings = len(
    telemetry[
        telemetry["SPOILAGE_LEVEL"] == "HIGH"
    ]
)


# ============================================================
# KPI ROW
# ============================================================

col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Active Containers</div>
            <div class="metric-value">{total_containers:02d}</div>
            <div class="metric-caption">Tracked shipments</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">High Risk</div>
            <div class="metric-value">{high_risk:02d}</div>
            <div class="metric-caption">Immediate attention</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Medium Risk</div>
            <div class="metric-value">{medium_risk:02d}</div>
            <div class="metric-caption">Monitor closely</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Avg Spoilage Score</div>
            <div class="metric-value">{avg_score:.1f}</div>
            <div class="metric-caption">Risk indicator</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col5:

    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Risk Events</div>
            <div class="metric-value">{total_risk_events:02d}</div>
            <div class="metric-caption">Environmental alerts</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    # ============================================================
    # EXECUTIVE OVERVIEW
    # ============================================================

    st.markdown(
        '<div class="section-title">Container Risk Monitor</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Real-time shipment health across the monitored agricultural fleet'
        '</div>',
        unsafe_allow_html=True
    )

    # ============================================================
    # FLEET RISK TABLE
    # ============================================================

    display_data = data[
        [
            "CONTAINER_ID",
            "COMMODITY",
            "ORIGIN",
            "DESTINATION",
            "RISK_EVENTS",
            "AVG_TEMPERATURE",
            "AVG_HUMIDITY",
            "MAX_SPOILAGE_SCORE",
            "OVERALL_RISK"
        ]
    ].copy()

    display_data.columns = [
        "Container",
        "Commodity",
        "Origin",
        "Destination",
        "Risk Events",
        "Avg Temp °C",
        "Avg Humidity %",
        "Max Score",
        "Risk"
    ]

    st.dataframe(
        display_data,
        width="stretch",
        hide_index=True,
        height=310
    )

    # ============================================================
    # FLEET ANALYTICS
    # ============================================================

    st.markdown(
        '<div class="section-title">Fleet Analytics</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Environmental exposure and risk distribution across active shipments'
        '</div>',
        unsafe_allow_html=True
    )

    chart1, chart2 = st.columns(2)

    # ------------------------------------------------------------
    # RISK DISTRIBUTION
    # ------------------------------------------------------------

    with chart1:

        risk_counts = (
            data["OVERALL_RISK"]
            .value_counts()
            .reindex(["HIGH", "MEDIUM", "LOW"], fill_value=0)
        )

        fig = px.bar(
            x=risk_counts.index,
            y=risk_counts.values,
            labels={
                "x": "Risk Level",
                "y": "Containers"
            }
        )

        fig.update_traces(
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Containers: %{y}<extra></extra>"
        )

        fig.update_layout(
            title="Fleet Risk Distribution",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=350,
            margin=dict(l=20, r=20, t=60, b=30),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ------------------------------------------------------------
    # ENVIRONMENTAL EXPOSURE
    # ------------------------------------------------------------

    with chart2:

        fig = px.scatter(
            data,
            x="AVG_TEMPERATURE",
            y="AVG_HUMIDITY",
            size="MAX_SPOILAGE_SCORE",
            hover_name="CONTAINER_ID",
            text="COMMODITY",
            labels={
                "AVG_TEMPERATURE": "Average Temperature °C",
                "AVG_HUMIDITY": "Average Humidity %"
            }
        )

        fig.update_traces(
            textposition="top center",
            marker=dict(
                opacity=0.85,
                line=dict(width=1)
            )
        )

        fig.update_layout(
            title="Environmental Exposure Map",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=350,
            margin=dict(l=20, r=20, t=60, b=30),
            showlegend=False
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # ============================================================
    # TELEMETRY INTELLIGENCE
    # ============================================================

    st.markdown(
        '<div class="section-title">Telemetry Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Environmental readings captured from the Kafka telemetry stream'
        '</div>',
        unsafe_allow_html=True
    )

    t1, t2, t3 = st.columns(3)

    with t1:
        st.metric(
            "Telemetry Readings",
            total_telemetry
        )

    with t2:
        st.metric(
            "High-Risk Readings",
            high_risk_readings
        )

    with t3:
        st.metric(
            "Containers Monitored",
            telemetry["container_id"].nunique()
        )

    # ============================================================
    # LATEST TELEMETRY
    # ============================================================

    latest = (
        telemetry
        .sort_values("TIMESTAMP", ascending=False)
        .head(10)
    )

    latest_display = latest[
        [
            "TIMESTAMP",
            "container_id",
            "commodity",
            "temperature",
            "humidity",
            "vibration",
            "SPOILAGE_SCORE",
            "SPOILAGE_LEVEL"
        ]
    ].copy()

    latest_display.columns = [
        "Timestamp",
        "Container",
        "Commodity",
        "Temperature °C",
        "Humidity %",
        "Vibration",
        "Spoilage Score",
        "Level"
    ]

    st.dataframe(
        latest_display,
        width="stretch",
        hide_index=True,
        height=360
    )

    # ============================================================
    # ACTIVE ALERTS
    # ============================================================

    st.markdown(
        '<div class="section-title">Active Alerts</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Containers requiring operational attention'
        '</div>',
        unsafe_allow_html=True
    )

    high_risk_data = data[
        data["OVERALL_RISK"] == "HIGH"
    ]

    if high_risk_data.empty:

        st.success("No high-risk containers detected.")

    else:

        for _, row in high_risk_data.iterrows():

            st.html(f"""
            <div class="alert-card">

                <div class="alert-title">
                    {row["CONTAINER_ID"]} · {row["COMMODITY"]}
                </div>

                <div class="alert-detail">
                    Route: {row["ORIGIN"]} → {row["DESTINATION"]}
                    &nbsp; • &nbsp;
                    Maximum spoilage score:
                    {row["MAX_SPOILAGE_SCORE"]}
                    &nbsp; • &nbsp;
                    Risk events:
                    {row["RISK_EVENTS"]}
                </div>

            </div>
            """)



# ============================================================
# CONTAINER INTELLIGENCE
# ============================================================

# ============================================================
# CONTAINER INTELLIGENCE
# ============================================================

elif page == "Container Intelligence":

    st.markdown(
        '<div class="section-title">'
        'Container Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Deep environmental analysis for individual shipments'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # CONTAINER SELECTOR
    # --------------------------------------------------------

    selected_container = st.selectbox(
        "Select container",
        data["CONTAINER_ID"].tolist(),
        key="container_selector"
    )

    container = data[
        data["CONTAINER_ID"] == selected_container
    ].iloc[0]

    container_telemetry = telemetry[
        telemetry["container_id"] == selected_container
    ].sort_values("TIMESTAMP").copy()

    st.write("")

    # --------------------------------------------------------
    # CONTAINER HEADER
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="telemetry-card">
            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
                gap:20px;
                flex-wrap:wrap;
            ">

                <div>
                    <div style="
                        color:#7f8b99;
                        font-size:11px;
                        letter-spacing:1.5px;
                        text-transform:uppercase;
                    ">
                        Active Shipment
                    </div>

                    <div style="
                        color:#f4f7fa;
                        font-size:25px;
                        font-weight:700;
                        margin-top:5px;
                    ">
                        {container["CONTAINER_ID"]}
                    </div>

                    <div style="
                        color:#8995a3;
                        font-size:13px;
                        margin-top:4px;
                    ">
                        {container["COMMODITY"]} ·
                        {container["ORIGIN"]} →
                        {container["DESTINATION"]}
                    </div>
                </div>

                <div style="
                    background:#1b2632;
                    border:1px solid #344353;
                    border-radius:20px;
                    padding:8px 15px;
                    color:#f1d7da;
                    font-size:12px;
                    font-weight:700;
                    letter-spacing:.7px;
                ">
                    {container["OVERALL_RISK"]} RISK
                </div>

            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # CONTAINER KPIs
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "Commodity",
            container["COMMODITY"]
        )

    with c2:

        st.metric(
            "Risk Level",
            container["OVERALL_RISK"]
        )

    with c3:

        st.metric(
            "Max Spoilage Score",
            int(container["MAX_SPOILAGE_SCORE"])
        )

    with c4:

        st.metric(
            "Risk Events",
            int(container["RISK_EVENTS"])
        )

    st.write("")

    # --------------------------------------------------------
    # SHIPMENT PROFILE
    # --------------------------------------------------------

    profile_col1, profile_col2 = st.columns(2)

    with profile_col1:

        st.markdown(
            '<div class="section-title">'
            'Shipment Route'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="telemetry-card">

                <div style="
                    color:#7f8b99;
                    font-size:10px;
                    text-transform:uppercase;
                    letter-spacing:1.3px;
                ">
                    Origin
                </div>

                <div style="
                    color:#f4f7fa;
                    font-size:18px;
                    font-weight:650;
                    margin-top:4px;
                ">
                    {container["ORIGIN"]}
                </div>

                <div style="
                    color:#667481;
                    font-size:20px;
                    margin:6px 0;
                ">
                    ↓
                </div>

                <div style="
                    color:#7f8b99;
                    font-size:10px;
                    text-transform:uppercase;
                    letter-spacing:1.3px;
                ">
                    Destination
                </div>

                <div style="
                    color:#f4f7fa;
                    font-size:18px;
                    font-weight:650;
                    margin-top:4px;
                ">
                    {container["DESTINATION"]}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with profile_col2:

        st.markdown(
            '<div class="section-title">'
            'Environmental Profile'
            '</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="telemetry-card">

                <div style="
                    display:grid;
                    grid-template-columns:1fr 1fr;
                    gap:18px;
                ">

                    <div>
                        <div style="
                            color:#7f8b99;
                            font-size:10px;
                            text-transform:uppercase;
                            letter-spacing:1.3px;
                        ">
                            Avg Temperature
                        </div>

                        <div style="
                            color:#f4f7fa;
                            font-size:22px;
                            font-weight:700;
                            margin-top:5px;
                        ">
                            {container["AVG_TEMPERATURE"]} °C
                        </div>
                    </div>

                    <div>
                        <div style="
                            color:#7f8b99;
                            font-size:10px;
                            text-transform:uppercase;
                            letter-spacing:1.3px;
                        ">
                            Avg Humidity
                        </div>

                        <div style="
                            color:#f4f7fa;
                            font-size:22px;
                            font-weight:700;
                            margin-top:5px;
                        ">
                            {container["AVG_HUMIDITY"]} %
                        </div>
                    </div>

                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # ENVIRONMENTAL TELEMETRY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Environmental Telemetry'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Live environmental movement captured from container telemetry'
        '</div>',
        unsafe_allow_html=True
    )

    trend_col1, trend_col2 = st.columns(2)

    # --------------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------------

    with trend_col1:

        fig = px.line(
            container_telemetry,
            x="TIMESTAMP",
            y="TEMPERATURE",
            markers=True,
            title="Temperature"
        )

        fig.add_hline(
            y=30,
            line_dash="dash",
            annotation_text="Risk threshold · 30°C",
            annotation_position="top left"
        )

        fig.update_traces(
            line=dict(width=2),
            marker=dict(size=7)
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=340,
            margin=dict(l=20, r=20, t=55, b=35),
            hovermode="x unified"
        )

        fig.update_xaxes(
            showgrid=False,
            title=""
        )

        fig.update_yaxes(
            gridcolor="#202832",
            title="Temperature °C"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # HUMIDITY
    # --------------------------------------------------------

    with trend_col2:

        fig = px.line(
            container_telemetry,
            x="TIMESTAMP",
            y="HUMIDITY",
            markers=True,
            title="Humidity"
        )

        fig.add_hline(
            y=75,
            line_dash="dash",
            annotation_text="Risk threshold · 75%",
            annotation_position="top left"
        )

        fig.update_traces(
            line=dict(width=2),
            marker=dict(size=7)
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=340,
            margin=dict(l=20, r=20, t=55, b=35),
            hovermode="x unified"
        )

        fig.update_xaxes(
            showgrid=False,
            title=""
        )

        fig.update_yaxes(
            gridcolor="#202832",
            title="Humidity %"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # VIBRATION + SPOILAGE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Risk Signals'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Mechanical movement and calculated spoilage exposure'
        '</div>',
        unsafe_allow_html=True
    )

    vibration_col, spoilage_col = st.columns(2)

    # --------------------------------------------------------
    # VIBRATION
    # --------------------------------------------------------

    with vibration_col:

        fig = px.line(
            container_telemetry,
            x="TIMESTAMP",
            y="VIBRATION",
            markers=True,
            title="Vibration Trend"
        )

        fig.update_traces(
            line=dict(width=2),
            marker=dict(size=7)
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=340,
            margin=dict(l=20, r=20, t=55, b=35),
            hovermode="x unified"
        )

        fig.update_xaxes(
            showgrid=False,
            title=""
        )

        fig.update_yaxes(
            gridcolor="#202832",
            title="Vibration"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # SPOILAGE SCORE
    # --------------------------------------------------------

    with spoilage_col:

        fig = px.bar(
            container_telemetry,
            x="TIMESTAMP",
            y="SPOILAGE_SCORE",
            title="Spoilage Risk Trend"
        )

        fig.update_yaxes(
            range=[0, 85],
            title="Spoilage Score"
        )

        fig.update_xaxes(
            showgrid=False,
            title=""
        )

        fig.update_traces(
            marker_line_width=0,
            opacity=0.9
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=340,
            margin=dict(l=20, r=20, t=55, b=35),
            hovermode="x unified"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # RISK SUMMARY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Risk Summary'
        '</div>',
        unsafe_allow_html=True
    )

    risk_summary_col1, risk_summary_col2, risk_summary_col3 = st.columns(3)

    total_readings = len(container_telemetry)

    high_count = int(
        (container_telemetry["SPOILAGE_LEVEL"] == "HIGH").sum()
    )

    medium_count = int(
        (container_telemetry["SPOILAGE_LEVEL"] == "MEDIUM").sum()
    )

    low_count = int(
        (container_telemetry["SPOILAGE_LEVEL"] == "LOW").sum()
    )

    with risk_summary_col1:

        st.metric(
            "High-Risk Readings",
            high_count,
            f"{high_count}/{total_readings} readings"
        )

    with risk_summary_col2:

        st.metric(
            "Medium-Risk Readings",
            medium_count,
            f"{medium_count}/{total_readings} readings"
        )

    with risk_summary_col3:

        st.metric(
            "Normal Readings",
            low_count,
            f"{low_count}/{total_readings} readings"
        )

    # --------------------------------------------------------
    # CONTAINER TELEMETRY TABLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Telemetry Readings'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Detailed environmental observations for the selected container'
        '</div>',
        unsafe_allow_html=True
    )

    telemetry_display = container_telemetry[
        [
            "TIMESTAMP",
            "container_id",
            "commodity",
            "temperature",
            "humidity",
            "vibration",
            "SPOILAGE_SCORE",
            "SPOILAGE_LEVEL"
        ]
    ].copy()

    telemetry_display.columns = [
        "Timestamp",
        "Container",
        "Commodity",
        "Temperature °C",
        "Humidity %",
        "Vibration",
        "Spoilage Score",
        "Risk Level"
    ]

    st.dataframe(
        telemetry_display,
        width="stretch",
        hide_index=True,
        height=360
    )

    # --------------------------------------------------------
    # OPERATIONAL ALERT
    # --------------------------------------------------------

    if container["OVERALL_RISK"] == "HIGH":

        st.markdown(
            f"""
            <div class="alert-card">

                <div class="alert-title">
                    ⚠ High-Risk Shipment Detected
                </div>

                <div class="alert-detail">
                    {container["CONTAINER_ID"]} carrying
                    {container["COMMODITY"]} requires operational attention.
                    Maximum spoilage score:
                    {int(container["MAX_SPOILAGE_SCORE"])}.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    elif container["OVERALL_RISK"] == "MEDIUM":

        st.markdown(
            f"""
            <div class="telemetry-card">

                <div style="
                    color:#d9c58a;
                    font-size:13px;
                    font-weight:650;
                ">
                    ◐ Monitoring Required
                </div>

                <div style="
                    color:#7f8995;
                    font-size:12px;
                    margin-top:5px;
                ">
                    {container["CONTAINER_ID"]} is showing moderate
                    environmental exposure.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            f"""
            <div class="telemetry-card">

                <div style="
                    color:#9ed7b8;
                    font-size:13px;
                    font-weight:650;
                ">
                    ✓ Shipment Environment Stable
                </div>

                <div style="
                    color:#7f8995;
                    font-size:12px;
                    margin-top:5px;
                ">
                    {container["CONTAINER_ID"]} currently shows
                    low spoilage exposure.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# ANALYTICS
# ============================================================

# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    st.markdown(
        '<div class="section-title">'
        'Risk Analytics'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Fleet-level environmental, commodity and spoilage-risk intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # ANALYTICS KPI ROW
    # --------------------------------------------------------

    total_readings = len(telemetry)

    avg_temperature = telemetry["TEMPERATURE"].mean()

    avg_humidity = telemetry["HUMIDITY"].mean()

    total_risk_events = int(
        (
            telemetry["SPOILAGE_LEVEL"]
            .isin(["HIGH", "MEDIUM"])
        ).sum()
    )

    a1, a2, a3, a4 = st.columns(4)

    with a1:

        st.metric(
            "Telemetry Readings",
            f"{total_readings:02d}"
        )

    with a2:

        st.metric(
            "Avg Temperature",
            f"{avg_temperature:.1f} °C"
        )

    with a3:

        st.metric(
            "Avg Humidity",
            f"{avg_humidity:.1f} %"
        )

    with a4:

        st.metric(
            "Risk Events",
            total_risk_events
        )

    st.write("")

    # --------------------------------------------------------
    # ENVIRONMENTAL ANALYSIS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Environmental Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Distribution of temperature and humidity across all monitored readings'
        '</div>',
        unsafe_allow_html=True
    )

    env_col1, env_col2 = st.columns(2)

    # --------------------------------------------------------
    # TEMPERATURE DISTRIBUTION
    # --------------------------------------------------------

    with env_col1:

        fig = px.histogram(
            telemetry,
            x="TEMPERATURE",
            nbins=12,
            title="Temperature Distribution"
        )

        fig.add_vline(
            x=30,
            line_dash="dash",
            annotation_text="Risk threshold · 30°C",
            annotation_position="top right"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=340,
            margin=dict(l=20, r=20, t=55, b=35)
        )

        fig.update_xaxes(
            title="Temperature °C",
            showgrid=False
        )

        fig.update_yaxes(
            title="Readings",
            gridcolor="#202832"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # HUMIDITY DISTRIBUTION
    # --------------------------------------------------------

    with env_col2:

        fig = px.histogram(
            telemetry,
            x="HUMIDITY",
            nbins=12,
            title="Humidity Distribution"
        )

        fig.add_vline(
            x=75,
            line_dash="dash",
            annotation_text="Risk threshold · 75%",
            annotation_position="top right"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=340,
            margin=dict(l=20, r=20, t=55, b=35)
        )

        fig.update_xaxes(
            title="Humidity %",
            showgrid=False
        )

        fig.update_yaxes(
            title="Readings",
            gridcolor="#202832"
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # SPOILAGE + RISK ANALYSIS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Spoilage Risk Analysis'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Calculated risk indicators across the monitored container fleet'
        '</div>',
        unsafe_allow_html=True
    )

    risk_col1, risk_col2 = st.columns(2)

    # --------------------------------------------------------
    # AVERAGE SPOILAGE SCORE
    # --------------------------------------------------------

    with risk_col1:

        score_data = data.sort_values(
            "AVG_SPOILAGE_SCORE",
            ascending=True
        )

        fig = px.bar(
            score_data,
            x="AVG_SPOILAGE_SCORE",
            y="CONTAINER_ID",
            orientation="h",
            title="Average Spoilage Score",
            hover_data=[
                "COMMODITY",
                "RISK_EVENTS",
                "OVERALL_RISK"
            ]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=360,
            margin=dict(l=20, r=20, t=55, b=35)
        )

        fig.update_xaxes(
            range=[0, 85],
            title="Average Spoilage Score",
            gridcolor="#202832"
        )

        fig.update_yaxes(
            title=""
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # RISK LEVEL DISTRIBUTION
    # --------------------------------------------------------

    with risk_col2:

        risk_counts = (
            telemetry["SPOILAGE_LEVEL"]
            .value_counts()
            .reindex(
                ["HIGH", "MEDIUM", "LOW"],
                fill_value=0
            )
        )

        fig = px.pie(
            values=risk_counts.values,
            names=risk_counts.index,
            hole=0.58,
            title="Telemetry Risk Distribution"
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            height=360,
            margin=dict(l=20, r=20, t=55, b=35),
            legend=dict(
                orientation="h",
                y=-0.05
            )
        )

        st.plotly_chart(
            fig,
            width="stretch"
        )

    # --------------------------------------------------------
    # ENVIRONMENT vs SPOILAGE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Environmental Risk Relationship'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Relationship between temperature, humidity and calculated spoilage exposure'
        '</div>',
        unsafe_allow_html=True
    )

    fig = px.scatter(
        telemetry,
        x="TEMPERATURE",
        y="HUMIDITY",
        size="SPOILAGE_SCORE",
        hover_name="container_id",
        hover_data=[
            "commodity",
            "origin",
            "destination",
            "SPOILAGE_LEVEL"
        ],
        title="Temperature vs Humidity Exposure"
    )

    fig.add_vline(
        x=30,
        line_dash="dash",
        annotation_text="30°C"
    )

    fig.add_hline(
        y=75,
        line_dash="dash",
        annotation_text="75%"
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe2e8"),
        height=430,
        margin=dict(l=20, r=20, t=55, b=35)
    )

    fig.update_xaxes(
        title="Temperature °C",
        gridcolor="#202832"
    )

    fig.update_yaxes(
        title="Humidity %",
        gridcolor="#202832"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    # --------------------------------------------------------
    # COMMODITY INTELLIGENCE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Commodity Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Risk exposure across different agricultural commodities'
        '</div>',
        unsafe_allow_html=True
    )

    commodity_data = (
        telemetry
        .groupby("commodity")
        .agg(
            Readings=("commodity", "size"),
            Average_Temperature=("TEMPERATURE", "mean"),
            Average_Humidity=("HUMIDITY", "mean"),
            Average_Spoilage_Score=("SPOILAGE_SCORE", "mean"),
            High_Risk_Readings=(
                "SPOILAGE_LEVEL",
                lambda x: (x == "HIGH").sum()
            ),
            Risk_Readings=(
                "SPOILAGE_LEVEL",
                lambda x: x.isin(
                    ["HIGH", "MEDIUM"]
                ).sum()
            )
        )
        .reset_index()
    )

    commodity_data[
        [
            "Average_Temperature",
            "Average_Humidity",
            "Average_Spoilage_Score"
        ]
    ] = commodity_data[
        [
            "Average_Temperature",
            "Average_Humidity",
            "Average_Spoilage_Score"
        ]
    ].round(2)

    commodity_display = commodity_data.copy()

    commodity_display.columns = [
        "Commodity",
        "Readings",
        "Avg Temperature °C",
        "Avg Humidity %",
        "Avg Spoilage Score",
        "High-Risk Readings",
        "Risk Readings"
    ]

    st.dataframe(
        commodity_display,
        width="stretch",
        hide_index=True
    )

    # --------------------------------------------------------
    # ROUTE INTELLIGENCE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Route Intelligence'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Environmental risk observed across active shipment routes'
        '</div>',
        unsafe_allow_html=True
    )

    route_data = (
        telemetry
        .groupby(
            ["origin", "destination"]
        )
        .agg(
            Readings=("container_id", "size"),
            Containers=("container_id", "nunique"),
            Average_Temperature=("TEMPERATURE", "mean"),
            Average_Humidity=("HUMIDITY", "mean"),
            Average_Spoilage_Score=("SPOILAGE_SCORE", "mean"),
            Risk_Readings=(
                "SPOILAGE_LEVEL",
                lambda x: x.isin(
                    ["HIGH", "MEDIUM"]
                ).sum()
            )
        )
        .reset_index()
    )

    route_data[
        [
            "Average_Temperature",
            "Average_Humidity",
            "Average_Spoilage_Score"
        ]
    ] = route_data[
        [
            "Average_Temperature",
            "Average_Humidity",
            "Average_Spoilage_Score"
        ]
    ].round(2)

    route_display = route_data.copy()

    route_display["Route"] = (
        route_display["origin"]
        + " → "
        + route_display["destination"]
    )

    route_display = route_display[
        [
            "Route",
            "Containers",
            "Readings",
            "Average_Temperature",
            "Average_Humidity",
            "Average_Spoilage_Score",
            "Risk_Readings"
        ]
    ]

    route_display.columns = [
        "Route",
        "Containers",
        "Readings",
        "Avg Temperature °C",
        "Avg Humidity %",
        "Avg Spoilage Score",
        "Risk Readings"
    ]

    st.dataframe(
        route_display,
        width="stretch",
        hide_index=True
    )

    # --------------------------------------------------------
    # RISK EVENTS BY CONTAINER
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Container Risk Matrix'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Detailed risk-event profile for every monitored container'
        '</div>',
        unsafe_allow_html=True
    )

    risk_events = (
        telemetry
        .groupby("container_id")
        .agg(
            Total_Readings=("container_id", "size"),

            High_Risk_Readings=(
                "SPOILAGE_LEVEL",
                lambda x: (x == "HIGH").sum()
            ),

            Medium_Risk_Readings=(
                "SPOILAGE_LEVEL",
                lambda x: (x == "MEDIUM").sum()
            ),

            Average_Score=(
                "SPOILAGE_SCORE",
                "mean"
            ),

            Maximum_Score=(
                "SPOILAGE_SCORE",
                "max"
            )
        )
        .reset_index()
    )

    risk_events[
        [
            "Average_Score",
            "Maximum_Score"
        ]
    ] = risk_events[
        [
            "Average_Score",
            "Maximum_Score"
        ]
    ].round(2)

    risk_events.columns = [
        "Container",
        "Total Readings",
        "High-Risk Readings",
        "Medium-Risk Readings",
        "Average Score",
        "Maximum Score"
    ]

    st.dataframe(
        risk_events,
        width="stretch",
        hide_index=True
    )

    # --------------------------------------------------------
    # AUTOMATED INSIGHTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Operational Insights'
        '</div>',
        unsafe_allow_html=True
    )

    highest_risk_container = data.loc[
        data["AVG_SPOILAGE_SCORE"].idxmax()
    ]

    highest_risk_commodity = commodity_data.loc[
        commodity_data["Average_Spoilage_Score"].idxmax()
    ]

    highest_risk_route = route_data.loc[
        route_data["Average_Spoilage_Score"].idxmax()
    ]

    insight_col1, insight_col2 = st.columns(2)

    with insight_col1:

        st.markdown(
            f"""
            <div class="alert-card">

                <div class="alert-title">
                    Highest Exposure Container
                </div>

                <div class="alert-detail">
                    {highest_risk_container["CONTAINER_ID"]}
                    · {highest_risk_container["COMMODITY"]}
                    has the highest average spoilage score
                    of {highest_risk_container["AVG_SPOILAGE_SCORE"]}.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with insight_col2:

        st.markdown(
            f"""
            <div class="telemetry-card">

                <div style="
                    color:#dbe2e8;
                    font-size:13px;
                    font-weight:650;
                ">
                    Highest-Risk Commodity
                </div>

                <div style="
                    color:#7f8995;
                    font-size:12px;
                    margin-top:5px;
                ">
                    {highest_risk_commodity["commodity"]}
                    shows the highest average spoilage score
                    at {highest_risk_commodity["Average_Spoilage_Score"]}.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="telemetry-card">

            <div style="
                color:#dbe2e8;
                font-size:13px;
                font-weight:650;
            ">
                Highest-Risk Route
            </div>

            <div style="
                color:#7f8995;
                font-size:12px;
                margin-top:5px;
            ">
                {highest_risk_route["origin"]}
                →
                {highest_risk_route["destination"]}
                currently shows the highest average spoilage
                score of {highest_risk_route["Average_Spoilage_Score"]}.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # LATEST TELEMETRY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Latest Telemetry'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Most recent environmental observations received from the telemetry stream'
        '</div>',
        unsafe_allow_html=True
    )

    latest_analytics = (
        telemetry
        .sort_values(
            "TIMESTAMP",
            ascending=False
        )
        .head(20)
    )

    latest_analytics_display = latest_analytics[
        [
            "TIMESTAMP",
            "container_id",
            "commodity",
            "origin",
            "destination",
            "temperature",
            "humidity",
            "vibration",
            "SPOILAGE_SCORE",
            "SPOILAGE_LEVEL"
        ]
    ].copy()

    latest_analytics_display.columns = [
        "Timestamp",
        "Container",
        "Commodity",
        "Origin",
        "Destination",
        "Temperature °C",
        "Humidity %",
        "Vibration",
        "Spoilage Score",
        "Risk Level"
    ]

    st.dataframe(
        latest_analytics_display,
        width="stretch",
        hide_index=True,
        height=420
    )