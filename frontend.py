import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/analyze"

st.set_page_config(
    page_title="AI Cybersecurity Assistant",
    page_icon="SEC",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------
# Session analysis history
# -----------------------------

if "analysis_history" not in st.session_state:
    st.session_state.analysis_history = []

# -----------------------------
# Custom styling
# -----------------------------

st.markdown(
    """
    <style>
        .main {
            background-color: #0e1117;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 3rem;
            max-width: 1200px;
        }

        .header-box {
            padding: 1.5rem;
            border: 1px solid #30363d;
            border-radius: 12px;
            background-color: #161b22;
            margin-bottom: 1.5rem;
        }

        .status {
            color: #3fb950;
            font-weight: 600;
        }

        .section-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin-top: 1.5rem;
            margin-bottom: 0.75rem;
        }

        .result-box {
            padding: 1rem;
            border: 1px solid #30363d;
            border-radius: 10px;
            background-color: #161b22;
            margin-bottom: 1rem;
        }

        .footer {
            text-align: center;
            color: #8b949e;
            font-size: 0.85rem;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #30363d;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Header
# -----------------------------

st.markdown(
    """
    <div class="header-box">
        <h1>AI Cybersecurity Assistant</h1>
        <p>
            Analyze security events using a locally hosted Large Language Model.
        </p>
        <p class="status">● Analysis API: ONLINE</p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.header("System Information")

    st.write("**Architecture**")
    st.code(
        "Streamlit\n"
        "   ↓\n"
        "FastAPI\n"
        "   ↓\n"
        "Local LLM\n"
        "   ↓\n"
        "Structured Analysis"
    )

    st.divider()

    st.write("**Analysis Capabilities**")
    st.write("• Threat identification")
    st.write("• Severity assessment")
    st.write("• Confidence estimation")
    st.write("• Evidence extraction")
    st.write("• Inference generation")
    st.write("• Unknown identification")
    st.write("• Defensive recommendations")

    st.divider()

    st.write("**Recent Analyses**")

    if st.session_state.analysis_history:
        for index, item in enumerate(
            reversed(st.session_state.analysis_history[-5:]),
            start=1
        ):
            st.write(
                f"**{index}. {item['severity']}** — "
                f"{item['threat']}"
            )
            st.caption(
                f"Confidence: {item['confidence']}"
            )
    else:
        st.caption("No analyses yet.")

# -----------------------------
# Event input
# -----------------------------

st.markdown(
    '<div class="section-title">Security Event</div>',
    unsafe_allow_html=True
)

event = st.text_area(
    "Enter a security event, alert, or log description:",
    placeholder=(
        "Example: A Windows computer received 500 failed login "
        "attempts from the same external IP address within 5 minutes."
    ),
    height=180,
    label_visibility="collapsed"
)

analyze = st.button(
    "Analyze Security Event",
    type="primary",
    use_container_width=True
)

# -----------------------------
# Analysis
# -----------------------------

if analyze:

    if not event.strip():
        st.warning("Please enter a security event first.")

    else:

        with st.spinner("Analyzing security event..."):

            try:
                response = requests.post(
                    API_URL,
                    json={"event": event},
                    timeout=120
                )

                response.raise_for_status()

                result = response.json()

                if not isinstance(result, dict):
                    raise ValueError("API response is not a valid object.")

                analysis = result.get("analysis")

                if not isinstance(analysis, dict):
                    raise ValueError(
                        "API response does not contain valid analysis data."
                    )

                # Normalize confidence
                confidence = analysis.get("confidence", 0)

                if isinstance(confidence, (int, float)):
                    confidence_value = max(0, min(1, float(confidence)))
                    confidence_display = f"{confidence_value:.0%}"
                elif isinstance(confidence, str):
                    confidence_display = confidence.strip()
                else:
                    confidence_display = "Unknown"

                # Normalize structured list fields
                def normalize_items(value):
                    if value is None:
                        return []

                    if isinstance(value, list):
                        return [str(item) for item in value if item]

                    if isinstance(value, str):
                        return [value] if value.strip() else []

                    return [str(value)]

                facts = normalize_items(
                    analysis.get("observed_facts")
                )

                inferences = normalize_items(
                    analysis.get("inferences")
                )

                unknowns = normalize_items(
                    analysis.get("unknowns")
                )

                recommendations = normalize_items(
                    analysis.get("recommendations")
                )

                threat = str(
                    analysis.get("threat", "Unknown")
                )

                severity = str(
                    analysis.get("severity", "Unknown")
                )

                st.session_state.analysis_history.append(
                    {
                        "threat": threat,
                        "severity": severity,
                        "confidence": confidence_display
                    }
                )

                st.success("Security analysis completed.")

                # -----------------------------
                # Summary metrics
                # -----------------------------

                st.markdown(
                    '<div class="section-title">Threat Assessment</div>',
                    unsafe_allow_html=True
                )

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Threat",
                        threat
                    )

                with col2:
                    st.metric(
                        "Severity",
                        severity
                    )

                with col3:
                    st.metric(
                        "Confidence",
                        confidence_display
                    )

                # -----------------------------
                # Observed facts
                # -----------------------------

                st.markdown(
                    '<div class="section-title">Observed Facts</div>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    if facts:
                        for fact in facts:
                            st.write(f"• {fact}")
                    else:
                        st.write("No observed facts provided.")

                # -----------------------------
                # Inferences
                # -----------------------------

                st.markdown(
                    '<div class="section-title">Inferences</div>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    if inferences:
                        for inference in inferences:
                            st.write(f"• {inference}")
                    else:
                        st.write("No inferences provided.")

                # -----------------------------
                # Unknowns
                # -----------------------------

                st.markdown(
                    '<div class="section-title">Unknown Information</div>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    if unknowns:
                        for unknown in unknowns:
                            st.write(f"• {unknown}")
                    else:
                        st.write("No unknowns identified.")

                # -----------------------------
                # Recommendations
                # -----------------------------

                st.markdown(
                    '<div class="section-title">Recommended Actions</div>',
                    unsafe_allow_html=True
                )

                with st.container(border=True):
                    if recommendations:
                        for recommendation in recommendations:
                            st.write(f"• {recommendation}")
                    else:
                        st.write("No recommendations provided.")

            except requests.exceptions.RequestException as error:

                st.error(
                    "Could not connect to the cybersecurity analysis API."
                )

                st.code(str(error))

            except (KeyError, ValueError, TypeError) as error:

                st.error(
                    "The API returned an unexpected response."
                )

                st.code(str(error))

# -----------------------------
# Footer
# -----------------------------

st.markdown(
    """
    <div class="footer">
        AI Cybersecurity Assistant • Local LLM Security Analysis
    </div>
    """,
    unsafe_allow_html=True
)
