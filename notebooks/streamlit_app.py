
import streamlit as st

from analytical_engine import route_question

from ai_business_analyst import (
    MODEL_NAME,
    generate_rule_based_explanation,
    get_final_explanation,
    export_dashboard_insight,
)


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Business Analyst",
    page_icon="🤖",
    layout="centered"
)


# ============================================================
# 2. APPLICATION HEADER
# ============================================================

st.title("🤖 AI Business Analyst")

st.caption(
    "Ask business questions and receive verified "
    "Python analytics with AI-powered explanations."
)

st.divider()

st.caption(f"AI Model: {MODEL_NAME}")


# ============================================================
# 3. QUESTION INPUT
# ============================================================

with st.form("business_question_form"):

    question = st.text_input(
        "Enter your business question:",
        placeholder="Which product has the highest revenue?"
    )

    submitted = st.form_submit_button(
        "Ask AI",
        use_container_width=True
    )


# ============================================================
# 4. PROCESS QUESTION
# ============================================================

if submitted:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("Analyzing your business question..."):

                # Step 1: Python Analytical Engine

                analysis = route_question(
                    question.strip()
                )

                if analysis is None:

                    st.session_state["latest_response"] = {
                        "status": "unsupported",
                        "question": question.strip()
                    }

                else:

                    # Step 2: Rule-Based Explanation

                    base_explanation = (
                        generate_rule_based_explanation(
                            analysis
                        )
                    )

                    # Step 3: Ollama AI Explanation

                    final_explanation, source, error = (
                        get_final_explanation(
                            base_explanation
                        )
                    )

                    # Step 4: Export Latest Insight to CSV

                    export_dashboard_insight(
                        question.strip(),
                        analysis,
                        final_explanation,
                        source
                    )

                    # Step 5: Save Only Latest Result

                    st.session_state["latest_response"] = {

                        "status": "success",

                        "question": question.strip(),

                        "metric": analysis["metric"],

                        "result": analysis["result"],

                        "explanation": final_explanation,

                        "source": source,

                        "error": error
                    }

        except Exception as error:

            st.session_state["latest_response"] = {
                "status": "error",
                "message": str(error)
            }


# ============================================================
# 5. DISPLAY LATEST RESPONSE
# ============================================================

response = st.session_state.get("latest_response")


if response:

    st.divider()

    if response["status"] == "unsupported":

        st.warning(
            "This question is not supported yet. "
            "Please ask about one of the supported business topics."
        )

    elif response["status"] == "error":

        st.error(
            "An error occurred while processing your question."
        )

        st.caption(response["message"])

    elif response["status"] == "success":

        st.subheader("Your Question")

        st.write(response["question"])

        st.subheader("Verified Python Result")

        st.write(
            f"**Metric:** {response['metric']}"
        )

        st.json(
            response["result"]
        )

        st.subheader("AI Business Explanation")

        st.write(
            response["explanation"]
        )

        st.caption(
            f"Response Source: {response['source']}"
        )

        if response["error"]:

            st.info(
                "Python fallback was used because "
                "the AI response was unavailable or invalid."
            )

        st.success(
            "Latest question and answer exported to Power BI CSV."
        )
