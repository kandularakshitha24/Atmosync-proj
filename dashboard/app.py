import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import joblib

# ============================================================
# PAGE CONFIG
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

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0b0f14;
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
        border-right: 1px solid #293440 !important;
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
    }

    .brand-subtitle {
        font-size: 10px;
        color: #7f8b99 !important;
        letter-spacing: 1.5px;
        margin-top: -4px;
    }

    .nav-heading {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.8px;
        color: #7f8b99 !important;
        margin: 8px 0 12px 4px;
    }

    .nav-divider {
        height: 1px;
        background-color: #202832;
        margin: 18px 0;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] {
        gap: 5px;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label {
        background-color: transparent !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        margin-bottom: 4px !important;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label:hover {
        background-color: #18212b !important;
        border-color: #293542 !important;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label:has(input:checked) {
        background-color: #1b2632 !important;
        border-color: #344353 !important;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label:has(input:checked) p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"] label p {
        color: #aeb8c4 !important;
        font-size: 13px !important;
    }

    .sidebar-spacer {
        height: 30px;
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
        margin-bottom: 18px;
    }

    .section-title {
        font-size: 19px;
        font-weight: 650;
        margin-top: 28px;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #71808e;
        font-size: 12px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA FILES
# ============================================================

SUMMARY_FILE = (
    "data/processed/dashboard_container_summary.csv"
)

TELEMETRY_FILE = (
    "data/processed/kafka_processed_telemetry.csv"
)

MODEL_FILE = (
    "ml/models/spoilage_risk_model.pkl"
)

ENCODER_FILE = (
    "ml/models/risk_label_encoder.pkl"
)


# ============================================================
# LOAD DATA
# ============================================================

try:

    telemetry = pd.read_csv(TELEMETRY_FILE)

except FileNotFoundError:

    st.error(
        "Kafka telemetry file was not found."
    )

    st.stop()


# ============================================================
# BUILD CONTAINER SUMMARY FROM KAFKA TELEMETRY
# ============================================================

telemetry["temperature"] = pd.to_numeric(
    telemetry["temperature"],
    errors="coerce"
)

telemetry["humidity"] = pd.to_numeric(
    telemetry["humidity"],
    errors="coerce"
)

telemetry["vibration"] = pd.to_numeric(
    telemetry["vibration"],
    errors="coerce"
)

telemetry["SPOILAGE_SCORE"] = 0

telemetry.loc[
    (telemetry["temperature"] > 30) &
    (telemetry["humidity"] > 75),
    "SPOILAGE_SCORE"
] = 80

telemetry.loc[
    (
        (telemetry["temperature"] > 30) &
        (telemetry["humidity"] <= 75)
    ) |
    (
        (telemetry["temperature"] <= 30) &
        (telemetry["humidity"] > 75)
    ),
    "SPOILAGE_SCORE"
] = 40

data = (
    telemetry
    .groupby(
        [
            "container_id",
            "commodity",
            "origin",
            "destination"
        ],
        as_index=False
    )
    .agg(
        TOTAL_READINGS=("container_id", "count"),
        RISK_EVENTS=("risk_status", lambda x: (x == "RISK").sum()),
        AVG_TEMPERATURE=("temperature", "mean"),
        AVG_HUMIDITY=("humidity", "mean"),
        MAX_SPOILAGE_SCORE=("SPOILAGE_SCORE", "max"),
        AVG_SPOILAGE_SCORE=("SPOILAGE_SCORE", "mean")
    )
)

data["AVG_TEMPERATURE"] = (
    data["AVG_TEMPERATURE"].round(2)
)

data["AVG_HUMIDITY"] = (
    data["AVG_HUMIDITY"].round(2)
)

data["AVG_SPOILAGE_SCORE"] = (
    data["AVG_SPOILAGE_SCORE"].round(2)
)

data["OVERALL_RISK"] = data["MAX_SPOILAGE_SCORE"].apply(
    lambda score:
        "HIGH" if score >= 80
        else "MEDIUM" if score >= 40
        else "LOW"
)

data = data.sort_values(
    "MAX_SPOILAGE_SCORE",
    ascending=False
).reset_index(drop=True)


# Match the column names expected by the dashboard

data.columns = [
    "CONTAINER_ID",
    "COMMODITY",
    "ORIGIN",
    "DESTINATION",
    "TOTAL_READINGS",
    "RISK_EVENTS",
    "AVG_TEMPERATURE",
    "AVG_HUMIDITY",
    "MAX_SPOILAGE_SCORE",
    "AVG_SPOILAGE_SCORE",
    "OVERALL_RISK"
]

# ============================================================
# MARKET DATA
# ============================================================

MARKET_FILE = (
    "data/processed/market_opportunities.csv"
)

try:

    market_data = pd.read_csv(
        MARKET_FILE
    )

except FileNotFoundError:

    st.error(
        "Market opportunities file was not found."
    )

    st.stop()

# ============================================================
# PREPARE TELEMETRY
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
# MACHINE LEARNING RISK PREDICTION
# ============================================================

model = joblib.load(MODEL_FILE)
label_encoder = joblib.load(ENCODER_FILE)

ml_features = telemetry[
    [
        "TEMPERATURE",
        "HUMIDITY",
        "VIBRATION"
    ]
].copy()

ml_features.columns = [
    "temperature",
    "humidity",
    "vibration"
]

ml_predictions = model.predict(
    ml_features
)

telemetry["ML_RISK_PREDICTION"] = (
    label_encoder.inverse_transform(
        ml_predictions
    )
)


# ============================================================
# SPOILAGE SCORE
# ============================================================

def get_spoilage_score(row):

    temperature = row["TEMPERATURE"]
    humidity = row["HUMIDITY"]

    if pd.isna(temperature) or pd.isna(humidity):
        return 0

    if temperature > 30 and humidity > 75:
        return 80

    if temperature > 30 or humidity > 75:
        return 40

    return 0


telemetry["SPOILAGE_SCORE"] = telemetry.apply(
    get_spoilage_score,
    axis=1
)


telemetry["SPOILAGE_LEVEL"] = telemetry[
    "SPOILAGE_SCORE"
].map(
    {
        0: "LOW",
        40: "MEDIUM",
        80: "HIGH"
    }
)


# ============================================================
# TELEMETRY STATUS
# ============================================================

telemetry_readings = len(telemetry)

containers_monitored = telemetry[
    "container_id"
].nunique()

latest_timestamp = telemetry[
    "TIMESTAMP"
].max()

if pd.notna(latest_timestamp):

    latest_telemetry_text = (
        latest_timestamp.strftime(
            "%d %b %Y · %H:%M:%S"
        )
    )

else:

    latest_telemetry_text = "Unavailable"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

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

    st.markdown(
        "<div class='nav-divider'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-heading">CONTROL TOWER</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
    "NAVIGATION",
    [
        "Executive Overview",
        "Container Intelligence",
        "Analytics",
        "Market & Arbitrage"
    ],
    label_visibility="collapsed"
)

    st.markdown(
        "<div class='nav-divider'></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-heading">SYSTEM</div>',
        unsafe_allow_html=True
    )

    st.success(
        "SYSTEM OPERATIONAL"
    )

    st.caption(
        f"Telemetry: {telemetry_readings} readings"
    )

    st.caption(
        f"Containers: {containers_monitored}"
    )

    st.caption(
        f"Last update: {latest_telemetry_text}"
    )

    st.markdown(
        "<div class='sidebar-spacer'></div>",
        unsafe_allow_html=True
    )

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


# ============================================================
# TELEMETRY STATUS BAR
# ============================================================

status_col1, status_col2, status_col3 = st.columns(
    [1.2, 1, 1.4]
)

with status_col1:

    st.success(
        "●  TELEMETRY STREAM OPERATIONAL"
    )

with status_col2:

    st.caption(
        f"{telemetry_readings} readings · "
        f"{containers_monitored} containers"
    )

with status_col3:

    st.caption(
        f"Last telemetry: {latest_telemetry_text}"
    )


# ============================================================
# GLOBAL KPIs
# ============================================================

total_containers = len(data)

high_risk_containers = len(
    data[
        data["OVERALL_RISK"] == "HIGH"
    ]
)

medium_risk_containers = len(
    data[
        data["OVERALL_RISK"] == "MEDIUM"
    ]
)

average_spoilage_score = (
    data["AVG_SPOILAGE_SCORE"].mean()
)

total_risk_events = int(
    data["RISK_EVENTS"].sum()
)


k1, k2, k3, k4, k5 = st.columns(5)


with k1:

    st.metric(
        "Active Containers",
        f"{total_containers:02d}",
        "Tracked shipments"
    )


with k2:

    st.metric(
        "High Risk",
        f"{high_risk_containers:02d}",
        "Immediate attention"
    )


with k3:

    st.metric(
        "Medium Risk",
        f"{medium_risk_containers:02d}",
        "Monitor closely"
    )


with k4:

    st.metric(
        "Avg Spoilage Score",
        f"{average_spoilage_score:.1f}",
        "Risk indicator"
    )


with k5:

    st.metric(
        "Risk Events",
        f"{total_risk_events:02d}",
        "Environmental alerts"
    )


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

if page == "Executive Overview":

    st.markdown(
        '<div class="section-title">'
        'Container Risk Monitor'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Current shipment health across the monitored fleet'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # RISK TABLE
    # --------------------------------------------------------

    risk_table = data[
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


    risk_table.columns = [
        "Container",
        "Commodity",
        "Origin",
        "Destination",
        "Risk Events",
        "Avg Temperature °C",
        "Avg Humidity %",
        "Max Spoilage Score",
        "Risk Level"
    ]


    st.dataframe(
        risk_table,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # RISK DISTRIBUTION
    # --------------------------------------------------------

    chart_col1, chart_col2 = st.columns(2)


    with chart_col1:

        risk_counts = (
            data["OVERALL_RISK"]
            .value_counts()
            .reindex(
                ["HIGH", "MEDIUM", "LOW"],
                fill_value=0
            )
        )


        fig = px.bar(
            x=risk_counts.index,
            y=risk_counts.values,
            title="Fleet Risk Distribution"
        )


        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            xaxis_title="Risk Level",
            yaxis_title="Containers"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with chart_col2:

        fig = px.scatter(
            data,
            x="AVG_TEMPERATURE",
            y="AVG_HUMIDITY",
            size="MAX_SPOILAGE_SCORE",
            hover_name="CONTAINER_ID",
            hover_data=[
                "COMMODITY",
                "ORIGIN",
                "DESTINATION"
            ],
            title="Environmental Exposure"
        )


        fig.add_vline(
            x=30,
            line_dash="dash"
        )


        fig.add_hline(
            y=75,
            line_dash="dash"
        )


        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8"),
            xaxis_title="Average Temperature °C",
            yaxis_title="Average Humidity %"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # TELEMETRY INTELLIGENCE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Telemetry Intelligence'
        '</div>',
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
            telemetry_readings
        )


    with t2:

        st.metric(
            "High-Risk Readings",
            int(
                (
                    telemetry["SPOILAGE_LEVEL"]
                    == "HIGH"
                ).sum()
            )
        )


    with t3:

        st.metric(
            "Containers Monitored",
            containers_monitored
        )

            # --------------------------------------------------------
    # AI RISK PREDICTION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'AI Risk Prediction'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Random Forest predictions based on temperature, humidity and vibration'
        '</div>',
        unsafe_allow_html=True
    )

    ml_counts = (
        telemetry["ML_RISK_PREDICTION"]
        .value_counts()
        .reindex(
            ["HIGH", "MEDIUM", "LOW"],
            fill_value=0
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "AI HIGH RISK",
            int(ml_counts["HIGH"])
        )

    with col2:

        st.metric(
            "AI MEDIUM RISK",
            int(ml_counts["MEDIUM"])
        )

    with col3:

        st.metric(
            "AI LOW RISK",
            int(ml_counts["LOW"])
        )

    ml_chart = px.bar(
        x=ml_counts.index,
        y=ml_counts.values,
        labels={
            "x": "Predicted Risk",
            "y": "Telemetry Readings"
        },
        title="ML Risk Prediction Distribution"
    )

    ml_chart.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe2e8")
    )

    st.plotly_chart(
        ml_chart,
        use_container_width=True
    )


    # --------------------------------------------------------
    # TELEMETRY CHART
    # --------------------------------------------------------

    telemetry_chart = go.Figure()


    telemetry_chart.add_trace(
        go.Scatter(
            x=telemetry["TIMESTAMP"],
            y=telemetry["TEMPERATURE"],
            mode="lines+markers",
            name="Temperature"
        )
    )


    telemetry_chart.add_trace(
        go.Scatter(
            x=telemetry["TIMESTAMP"],
            y=telemetry["HUMIDITY"],
            mode="lines+markers",
            name="Humidity"
        )
    )


    telemetry_chart.update_layout(
        title="Fleet Environmental Telemetry",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe2e8"),
        hovermode="x unified"
    )


    st.plotly_chart(
        telemetry_chart,
        use_container_width=True
    )


    # --------------------------------------------------------
    # ACTIVE ALERTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Active Alerts'
        '</div>',
        unsafe_allow_html=True
    )


    active_alerts = data[
        data["OVERALL_RISK"] == "HIGH"
    ]


    if active_alerts.empty:

        st.success(
            "No high-risk shipments are currently detected."
        )

    else:

        for _, row in active_alerts.iterrows():

            st.error(
                f'{row["CONTAINER_ID"]} · '
                f'{row["COMMODITY"]} · '
                f'{row["ORIGIN"]} → '
                f'{row["DESTINATION"]}\n\n'
                f'Maximum spoilage score: '
                f'{int(row["MAX_SPOILAGE_SCORE"])} · '
                f'Risk events: '
                f'{int(row["RISK_EVENTS"])}'
            )


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
    # SELECT CONTAINER
    # --------------------------------------------------------

    selected_container = st.selectbox(
        "Select container",
        data["CONTAINER_ID"].tolist()
    )


    container = data[
        data["CONTAINER_ID"]
        == selected_container
    ].iloc[0]


    container_telemetry = telemetry[
        telemetry["container_id"]
        == selected_container
    ].sort_values(
        "TIMESTAMP"
    ).copy()


    # --------------------------------------------------------
    # ACTIVE SHIPMENT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Active Shipment'
        '</div>',
        unsafe_allow_html=True
    )


    h1, h2 = st.columns([4, 1])


    with h1:

        st.subheader(
            container["CONTAINER_ID"]
        )

        st.caption(
            f'{container["COMMODITY"]} · '
            f'{container["ORIGIN"]} → '
            f'{container["DESTINATION"]}'
        )


    with h2:

        st.metric(
            "Risk Level",
            container["OVERALL_RISK"]
        )


    # --------------------------------------------------------
    # CONTAINER SUMMARY
    # --------------------------------------------------------

    s1, s2, s3, s4 = st.columns(4)


    with s1:

        st.metric(
            "Commodity",
            container["COMMODITY"]
        )


    with s2:

        st.metric(
            "Risk Level",
            container["OVERALL_RISK"]
        )


    with s3:

        st.metric(
            "Max Spoilage Score",
            int(
                container["MAX_SPOILAGE_SCORE"]
            )
        )


    with s4:

        st.metric(
            "Risk Events",
            int(
                container["RISK_EVENTS"]
            )
        )


    # --------------------------------------------------------
    # SHIPMENT PROFILE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Shipment Profile'
        '</div>',
        unsafe_allow_html=True
    )


    route_col, env_col = st.columns(2)


    with route_col:

        st.subheader("Shipment Route")

        st.write(
            f'**Origin:** '
            f'{container["ORIGIN"]}'
        )

        st.write("↓")

        st.write(
            f'**Destination:** '
            f'{container["DESTINATION"]}'
        )


    with env_col:

        st.subheader(
            "Environmental Profile"
        )

        e1, e2 = st.columns(2)


        with e1:

            st.metric(
                "Avg Temperature",
                f'{container["AVG_TEMPERATURE"]:.2f} °C'
            )


        with e2:

            st.metric(
                "Avg Humidity",
                f'{container["AVG_HUMIDITY"]:.2f} %'
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
        'Environmental movement captured from container telemetry'
        '</div>',
        unsafe_allow_html=True
    )


    if container_telemetry.empty:

        st.warning(
            "No telemetry data available for this container."
        )

    else:

        temp_col, humidity_col = st.columns(2)


        with temp_col:

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
                annotation_text="Risk threshold · 30°C"
            )


            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#dbe2e8"),
                height=340
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        with humidity_col:

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
                annotation_text="Risk threshold · 75%"
            )


            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#dbe2e8"),
                height=340
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # ----------------------------------------------------
        # RISK SIGNALS
        # ----------------------------------------------------

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


        with vibration_col:

            fig = px.line(
                container_telemetry,
                x="TIMESTAMP",
                y="VIBRATION",
                markers=True,
                title="Vibration Trend"
            )


            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#dbe2e8"),
                height=340
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        with spoilage_col:

            fig = px.bar(
                container_telemetry,
                x="TIMESTAMP",
                y="SPOILAGE_SCORE",
                title="Spoilage Risk Trend"
            )


            fig.update_yaxes(
                range=[0, 85]
            )


            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#dbe2e8"),
                height=340
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


        # ----------------------------------------------------
        # RISK SUMMARY
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Risk Summary'
            '</div>',
            unsafe_allow_html=True
        )


        total_readings = len(
            container_telemetry
        )


        high_count = int(
            (
                container_telemetry[
                    "SPOILAGE_LEVEL"
                ] == "HIGH"
            ).sum()
        )


        medium_count = int(
            (
                container_telemetry[
                    "SPOILAGE_LEVEL"
                ] == "MEDIUM"
            ).sum()
        )


        low_count = int(
            (
                container_telemetry[
                    "SPOILAGE_LEVEL"
                ] == "LOW"
            ).sum()
        )


        r1, r2, r3 = st.columns(3)


        with r1:

            st.metric(
                "High-Risk Readings",
                high_count,
                f"{high_count}/{total_readings}"
            )


        with r2:

            st.metric(
                "Medium-Risk Readings",
                medium_count,
                f"{medium_count}/{total_readings}"
            )


        with r3:

            st.metric(
                "Normal Readings",
                low_count,
                f"{low_count}/{total_readings}"
            )


        # ----------------------------------------------------
        # TELEMETRY READINGS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Telemetry Readings'
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
            use_container_width=True,
            hide_index=True,
            height=360
        )


        # ----------------------------------------------------
        # OPERATIONAL ALERT
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Operational Alert'
            '</div>',
            unsafe_allow_html=True
        )


        if container["OVERALL_RISK"] == "HIGH":

            st.error(
                f'⚠ High-Risk Shipment Detected\n\n'
                f'{container["CONTAINER_ID"]} carrying '
                f'{container["COMMODITY"]} requires operational '
                f'attention. Maximum spoilage score: '
                f'{int(container["MAX_SPOILAGE_SCORE"])}.'
            )


        elif container["OVERALL_RISK"] == "MEDIUM":

            st.warning(
                f'◐ Monitoring Required\n\n'
                f'{container["CONTAINER_ID"]} is showing '
                f'moderate environmental exposure.'
            )


        else:

            st.success(
                f'✓ Shipment Environment Stable\n\n'
                f'{container["CONTAINER_ID"]} currently shows '
                f'low spoilage exposure.'
            )


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
        'Fleet-level environmental and spoilage-risk analysis'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # ANALYTICS KPIs
    # --------------------------------------------------------

    a1, a2, a3, a4 = st.columns(4)


    with a1:

        st.metric(
            "Telemetry Readings",
            len(telemetry)
        )


    with a2:

        st.metric(
            "Average Temperature",
            f'{telemetry["TEMPERATURE"].mean():.2f} °C'
        )


    with a3:

        st.metric(
            "Average Humidity",
            f'{telemetry["HUMIDITY"].mean():.2f} %'
        )


    with a4:

        st.metric(
            "Risk Events",
            total_risk_events
        )


    # --------------------------------------------------------
    # RISK SCORE + ENVIRONMENT
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    with col1:

        fig = px.bar(
            data,
            x="CONTAINER_ID",
            y="AVG_SPOILAGE_SCORE",
            color="OVERALL_RISK",
            hover_data=[
                "COMMODITY",
                "RISK_EVENTS"
            ],
            title="Average Spoilage Score by Container"
        )


        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8")
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with col2:

        fig = go.Figure()


        fig.add_trace(
            go.Scatter(
                x=telemetry["TIMESTAMP"],
                y=telemetry["TEMPERATURE"],
                mode="lines+markers",
                name="Temperature"
            )
        )


        fig.add_trace(
            go.Scatter(
                x=telemetry["TIMESTAMP"],
                y=telemetry["HUMIDITY"],
                mode="lines+markers",
                name="Humidity"
            )
        )


        fig.update_layout(
            title="Telemetry Environmental Conditions",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8")
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # ENVIRONMENTAL ANALYSIS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Environmental Analysis'
        '</div>',
        unsafe_allow_html=True
    )


    e1, e2 = st.columns(2)


    with e1:

        fig = px.histogram(
            telemetry,
            x="TEMPERATURE",
            nbins=10,
            title="Temperature Distribution"
        )


        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8")
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    with e2:

        fig = px.histogram(
            telemetry,
            x="HUMIDITY",
            nbins=10,
            title="Humidity Distribution"
        )


        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#dbe2e8")
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )


    # --------------------------------------------------------
    # RISK EVENTS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Risk Events by Container'
        '</div>',
        unsafe_allow_html=True
    )


    risk_events = (
        telemetry
        .groupby("container_id")
        .agg(
            Total_Readings=(
                "container_id",
                "size"
            ),
            High_Risk_Readings=(
                "SPOILAGE_LEVEL",
                lambda x: (
                    x == "HIGH"
                ).sum()
            ),
            Medium_Risk_Readings=(
                "SPOILAGE_LEVEL",
                lambda x: (
                    x == "MEDIUM"
                ).sum()
            ),
            Average_Score=(
                "SPOILAGE_SCORE",
                "mean"
            )
        )
        .reset_index()
    )


    risk_events[
        "Average_Score"
    ] = risk_events[
        "Average_Score"
    ].round(2)


    risk_events.columns = [
        "Container",
        "Total Readings",
        "High-Risk Readings",
        "Medium-Risk Readings",
        "Average Score"
    ]


    st.dataframe(
        risk_events,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # ENVIRONMENTAL RISK RELATIONSHIP
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Environmental Risk Relationship'
        '</div>',
        unsafe_allow_html=True
    )


    fig = px.scatter(
        telemetry,
        x="TEMPERATURE",
        y="HUMIDITY",
        size="SPOILAGE_SCORE",
        color="SPOILAGE_LEVEL",
        hover_data=[
            "container_id",
            "commodity",
            "vibration"
        ],
        title="Temperature vs Humidity Risk"
    )


    fig.add_vline(
        x=30,
        line_dash="dash"
    )


    fig.add_hline(
        y=75,
        line_dash="dash"
    )


    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#dbe2e8")
    )


    st.plotly_chart(
        fig,
        use_container_width=True
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


    commodity_data = (
        data
        .groupby("COMMODITY")
        .agg(
            Containers=(
                "CONTAINER_ID",
                "nunique"
            ),
            Risk_Events=(
                "RISK_EVENTS",
                "sum"
            ),
            Average_Spoilage_Score=(
                "AVG_SPOILAGE_SCORE",
                "mean"
            ),
            Maximum_Spoilage_Score=(
                "MAX_SPOILAGE_SCORE",
                "max"
            )
        )
        .reset_index()
    )


    commodity_data[
        "Average_Spoilage_Score"
    ] = commodity_data[
        "Average_Spoilage_Score"
    ].round(2)


    commodity_display = commodity_data.copy()


    commodity_display.columns = [
        "Commodity",
        "Containers",
        "Risk Events",
        "Average Spoilage Score",
        "Maximum Spoilage Score"
    ]


    st.dataframe(
        commodity_display,
        use_container_width=True,
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


    route_data = (
        data
        .groupby(
            [
                "ORIGIN",
                "DESTINATION"
            ]
        )
        .agg(
            Containers=(
                "CONTAINER_ID",
                "nunique"
            ),
            Risk_Events=(
                "RISK_EVENTS",
                "sum"
            ),
            Average_Spoilage_Score=(
                "AVG_SPOILAGE_SCORE",
                "mean"
            ),
            Maximum_Spoilage_Score=(
                "MAX_SPOILAGE_SCORE",
                "max"
            )
        )
        .reset_index()
    )


    route_data[
        "Average_Spoilage_Score"
    ] = route_data[
        "Average_Spoilage_Score"
    ].round(2)


    route_display = route_data.copy()


    route_display["Route"] = (
        route_display["ORIGIN"]
        + " → "
        + route_display["DESTINATION"]
    )


    route_display = route_display[
        [
            "Route",
            "Containers",
            "Risk_Events",
            "Average_Spoilage_Score",
            "Maximum_Spoilage_Score"
        ]
    ]


    route_display.columns = [
        "Route",
        "Containers",
        "Risk Events",
        "Average Spoilage Score",
        "Maximum Spoilage Score"
    ]


    st.dataframe(
        route_display,
        use_container_width=True,
        hide_index=True
    )


    # --------------------------------------------------------
    # CONTAINER RISK MATRIX
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Container Risk Matrix'
        '</div>',
        unsafe_allow_html=True
    )


    matrix = data[
        [
            "CONTAINER_ID",
            "COMMODITY",
            "TOTAL_READINGS",
            "RISK_EVENTS",
            "AVG_SPOILAGE_SCORE",
            "MAX_SPOILAGE_SCORE",
            "OVERALL_RISK"
        ]
    ].copy()


    matrix.columns = [
        "Container",
        "Commodity",
        "Total Readings",
        "Risk Events",
        "Average Score",
        "Maximum Score",
        "Risk Level"
    ]


    st.dataframe(
        matrix,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # OPERATIONAL INSIGHTS
    # ========================================================

    st.markdown(
        '<div class="section-title">'
        'Operational Insights'
        '</div>',
        unsafe_allow_html=True
    )


    st.markdown(
        '<div class="section-subtitle">'
        'Automated observations generated from current telemetry and risk data'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # HIGHEST RISK CONTAINER
    # --------------------------------------------------------

    highest_risk_container = data.loc[
        data["MAX_SPOILAGE_SCORE"].idxmax()
    ]


    # --------------------------------------------------------
    # HIGHEST RISK COMMODITY
    # --------------------------------------------------------

    highest_risk_commodity = (
        data
        .groupby("COMMODITY")[
            "AVG_SPOILAGE_SCORE"
        ]
        .mean()
        .reset_index()
        .sort_values(
            "AVG_SPOILAGE_SCORE",
            ascending=False
        )
        .iloc[0]
    )


    # --------------------------------------------------------
    # HIGHEST RISK ROUTE
    # --------------------------------------------------------

    highest_risk_route = (
        data
        .groupby(
            [
                "ORIGIN",
                "DESTINATION"
            ]
        )[
            "AVG_SPOILAGE_SCORE"
        ]
        .mean()
        .reset_index()
        .sort_values(
            "AVG_SPOILAGE_SCORE",
            ascending=False
        )
        .iloc[0]
    )


    i1, i2, i3 = st.columns(3)


    with i1:

        st.subheader(
            "Highest Risk Container"
        )

        st.metric(
            "Container",
            highest_risk_container[
                "CONTAINER_ID"
            ]
        )

        st.write(
            f'Commodity: '
            f'{highest_risk_container["COMMODITY"]}'
        )

        st.write(
            f'Maximum score: '
            f'{int(highest_risk_container["MAX_SPOILAGE_SCORE"])}'
        )

        st.write(
            f'Risk level: '
            f'{highest_risk_container["OVERALL_RISK"]}'
        )


    with i2:

        st.subheader(
            "Highest Risk Commodity"
        )

        st.metric(
            "Commodity",
            highest_risk_commodity[
                "COMMODITY"
            ]
        )

        st.write(
            f'Average spoilage score: '
            f'{highest_risk_commodity["AVG_SPOILAGE_SCORE"]:.2f}'
        )


    with i3:

        st.subheader(
            "Highest Risk Route"
        )

        st.metric(
            "Route",
            f'{highest_risk_route["ORIGIN"]} '
            f'→ '
            f'{highest_risk_route["DESTINATION"]}'
        )

        st.write(
            f'Average spoilage score: '
            f'{highest_risk_route["AVG_SPOILAGE_SCORE"]:.2f}'
        )


    # --------------------------------------------------------
    # DECISION SUPPORT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Decision Support'
        '</div>',
        unsafe_allow_html=True
    )


    if high_risk_containers > 0:

        st.warning(
            f'{high_risk_containers} container(s) currently '
            f'show HIGH overall risk. These shipments should '
            f'be prioritized for operational review.'
        )

    elif medium_risk_containers > 0:

        st.info(
            f'{medium_risk_containers} container(s) currently '
            f'show MEDIUM risk. Continue monitoring environmental '
            f'conditions.'
        )

    else:

        st.success(
            'The monitored fleet currently shows stable '
            'environmental conditions.'
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


    latest_analytics = (
        telemetry
        .sort_values(
            "TIMESTAMP",
            ascending=False
        )
        .head(20)
    )


    latest_display = latest_analytics[
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


    latest_display.columns = [
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
        latest_display,
        use_container_width=True,
        hide_index=True
    )
# ============================================================
# MARKET & SPOILAGE ARBITRAGE
# ============================================================

elif page == "Market & Arbitrage":

    st.markdown(
        '<div class="section-title">'
        'Market & Spoilage Arbitrage'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Scenario-based decision support combining spoilage risk, '
        'market value and logistics cost'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Scenario model: market prices, quantities and logistics "
        "costs are prototype assumptions and are not live market data."
    )


    # --------------------------------------------------------
    # SELECT COMMODITY
    # --------------------------------------------------------

    available_commodities = sorted(
        market_data["COMMODITY"].unique()
    )

    selected_commodity = st.selectbox(
        "Select commodity",
        available_commodities
    )


    # --------------------------------------------------------
    # FIND CURRENT SHIPMENT
    # --------------------------------------------------------

    commodity_containers = data[
        data["COMMODITY"] == selected_commodity
    ].copy()


    if commodity_containers.empty:

        st.warning(
            "No active shipment found for this commodity."
        )

    else:

        selected_shipment = commodity_containers.loc[
            commodity_containers["MAX_SPOILAGE_SCORE"].idxmax()
        ]


        container_id = selected_shipment[
            "CONTAINER_ID"
        ]

        current_market = selected_shipment[
            "DESTINATION"
        ]

        current_risk = selected_shipment[
            "OVERALL_RISK"
        ]

        current_score = float(
            selected_shipment[
                "MAX_SPOILAGE_SCORE"
            ]
        )


        # ----------------------------------------------------
        # SHIPMENT OVERVIEW
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-title">'
            'Shipment Under Assessment'
            '</div>',
            unsafe_allow_html=True
        )


        s1, s2, s3, s4 = st.columns(4)


        with s1:

            st.metric(
                "Container",
                container_id
            )


        with s2:

            st.metric(
                "Commodity",
                selected_commodity
            )


        with s3:

            st.metric(
                "Current Market",
                current_market
            )


        with s4:

            st.metric(
                "Spoilage Score",
                int(current_score)
            )


        st.caption(
            f"Current shipment risk level: {current_risk}"
        )


        # ----------------------------------------------------
        # MARKET OPTIONS
        # ----------------------------------------------------

        market_options = market_data[
            (
                market_data["COMMODITY"]
                == selected_commodity
            )
            &
            (
                market_data["CURRENT_MARKET"]
                == current_market
            )
        ].copy()


        if market_options.empty:

            st.warning(
                "No alternative market scenarios are available "
                "for the selected shipment."
            )

        else:

            # ------------------------------------------------
            # ARBITRAGE CALCULATION
            # ------------------------------------------------

            market_options[
                "CURRENT_VALUE"
            ] = (
                market_options[
                    "CURRENT_PRICE_PER_KG"
                ]
                *
                market_options[
                    "QUANTITY_KG"
                ]
            )


            market_options[
                "ALTERNATIVE_VALUE"
            ] = (
                market_options[
                    "ALTERNATIVE_PRICE_PER_KG"
                ]
                *
                market_options[
                    "QUANTITY_KG"
                ]
            )


            market_options[
                "CURRENT_LOGISTICS"
            ] = (
                market_options[
                    "CURRENT_LOGISTICS_COST"
                ]
                *
                market_options[
                    "QUANTITY_KG"
                ]
            )


            market_options[
                "ALTERNATIVE_LOGISTICS"
            ] = (
                market_options[
                    "ALTERNATIVE_LOGISTICS_COST"
                ]
                *
                market_options[
                    "QUANTITY_KG"
                ]
            )


            # Estimated value impact of current spoilage risk.
            spoilage_factor = current_score / 100


            market_options[
                "CURRENT_RISK_ADJUSTED_VALUE"
            ] = (
                market_options[
                    "CURRENT_VALUE"
                ]
                *
                (1 - spoilage_factor)
            )


            market_options[
                "ALTERNATIVE_NET_VALUE"
            ] = (
                market_options[
                    "ALTERNATIVE_VALUE"
                ]
                -
                market_options[
                    "ALTERNATIVE_LOGISTICS"
                ]
            )


            market_options[
                "ARBITRAGE_BENEFIT"
            ] = (
                market_options[
                    "ALTERNATIVE_NET_VALUE"
                ]
                -
                market_options[
                    "CURRENT_RISK_ADJUSTED_VALUE"
                ]
            )


            # ------------------------------------------------
            # BEST ALTERNATIVE
            # ------------------------------------------------

            best_option = market_options.loc[
                market_options[
                    "ARBITRAGE_BENEFIT"
                ].idxmax()
            ]


            best_market = best_option[
                "ALTERNATIVE_MARKET"
            ]

            best_benefit = float(
                best_option[
                    "ARBITRAGE_BENEFIT"
                ]
            )


            # ------------------------------------------------
            # DECISION
            # ------------------------------------------------

            if current_risk == "HIGH" and best_benefit > 0:

                decision = "REROUTE RECOMMENDED"

            elif current_risk == "MEDIUM" and best_benefit > 0:

                decision = "MONITOR & CONSIDER REROUTE"

            elif best_benefit > 0:

                decision = "ALTERNATIVE MARKET AVAILABLE"

            else:

                decision = "CONTINUE CURRENT ROUTE"


            # ------------------------------------------------
            # ARBITRAGE KPI ROW
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                'Arbitrage Opportunity'
                '</div>',
                unsafe_allow_html=True
            )


            a1, a2, a3, a4 = st.columns(4)


            with a1:

                st.metric(
                    "Best Alternative",
                    best_market
                )


            with a2:

                st.metric(
                    "Alternative Price",
                    f'₹{best_option["ALTERNATIVE_PRICE_PER_KG"]:.0f}/kg'
                )


            with a3:

                st.metric(
                    "Potential Benefit",
                    f'₹{best_benefit:,.0f}'
                )


            with a4:

                st.metric(
                    "Decision",
                    decision
                )


            # ------------------------------------------------
            # MARKET COMPARISON
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                'Market Comparison'
                '</div>',
                unsafe_allow_html=True
            )


            comparison_display = market_options[
                [
                    "ALTERNATIVE_MARKET",
                    "CURRENT_PRICE_PER_KG",
                    "ALTERNATIVE_PRICE_PER_KG",
                    "CURRENT_LOGISTICS_COST",
                    "ALTERNATIVE_LOGISTICS_COST",
                    "ARBITRAGE_BENEFIT"
                ]
            ].copy()


            comparison_display.columns = [
                "Alternative Market",
                "Current Price ₹/kg",
                "Alternative Price ₹/kg",
                "Current Logistics ₹/kg",
                "Alternative Logistics ₹/kg",
                "Potential Benefit ₹"
            ]


            comparison_display[
                "Potential Benefit ₹"
            ] = comparison_display[
                "Potential Benefit ₹"
            ].round(0)


            st.dataframe(
                comparison_display,
                use_container_width=True,
                hide_index=True
            )


            # ------------------------------------------------
            # PRICE COMPARISON CHART
            # ------------------------------------------------

            chart_data = market_options[
                [
                    "ALTERNATIVE_MARKET",
                    "CURRENT_PRICE_PER_KG",
                    "ALTERNATIVE_PRICE_PER_KG"
                ]
            ].copy()


            chart_data = chart_data.rename(
                columns={
                    "ALTERNATIVE_MARKET": "Market",
                    "CURRENT_PRICE_PER_KG": "Current Market",
                    "ALTERNATIVE_PRICE_PER_KG": "Alternative Market"
                }
            )


            chart_data = chart_data.melt(
                id_vars="Market",
                var_name="Price Type",
                value_name="Price"
            )


            fig = px.bar(
                chart_data,
                x="Market",
                y="Price",
                color="Price Type",
                barmode="group",
                title="Current vs Alternative Market Price"
            )


            fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#dbe2e8"),
                yaxis_title="Price ₹/kg",
                xaxis_title="Market"
            )


            st.plotly_chart(
                fig,
                use_container_width=True
            )


            # ------------------------------------------------
            # DECISION SUPPORT
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                'Operational Recommendation'
                '</div>',
                unsafe_allow_html=True
            )


            if current_risk == "HIGH" and best_benefit > 0:

                st.warning(
                    f'⚠ High-risk shipment detected. '
                    f'{container_id} has a spoilage score of '
                    f'{int(current_score)}. '
                    f'The scenario model identifies '
                    f'{best_market} as the strongest alternative '
                    f'market with an estimated benefit of '
                    f'₹{best_benefit:,.0f}. '
                    f'Rerouting should be evaluated.'
                )


            elif best_benefit > 0:

                st.info(
                    f'◐ An alternative market may provide an '
                    f'estimated benefit of ₹{best_benefit:,.0f}. '
                    f'Consider market conditions and logistics '
                    f'before rerouting.'
                )


            else:

                st.success(
                    '✓ The current route remains economically '
                    'preferable under the selected scenario.'
                )


            # ------------------------------------------------
            # MODEL EXPLANATION
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                'How the Arbitrage Model Works'
                '</div>',
                unsafe_allow_html=True
            )


            st.write(
                "The model compares the risk-adjusted value of "
                "selling at the current destination with the "
                "net value of an alternative market."
            )


            st.code(
                "Current Risk-Adjusted Value = "
                "Current Market Value × "
                "(1 − Spoilage Score / 100)\n\n"
                "Alternative Net Value = "
                "Alternative Market Value - "
                "Alternative Logistics Cost\n\n"
                "Arbitrage Benefit = "
                "Alternative Net Value − "
                "Current Risk-Adjusted Value"
            )