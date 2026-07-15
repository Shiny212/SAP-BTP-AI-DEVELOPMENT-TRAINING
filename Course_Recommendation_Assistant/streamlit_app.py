import streamlit as st

from rag_engine import recommend_course
from tools import calculate_total_learning_hours

# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="Course Recommendation Assistant",
    page_icon="🎓",
    layout="wide"
)

# ---------------------------------------
# Title
# ---------------------------------------

st.title("🎓 Course Recommendation Assistant")

st.markdown(
    """
Ask questions about AI learning, SAP Business AI, LangChain,
RAG, SAP BTP, Joule, or AI Agents.

**Example:**

>I am an SAP ABAP developer with no AI experience.
>Which course should I take first to learn SAP Business AI?
"""
)

# ---------------------------------------
# User Input
# ---------------------------------------

question = st.text_area(
    "Enter your question",
    height=120,
    placeholder="Type your question here..."
)

# ---------------------------------------
# Recommendation Button
# ---------------------------------------

if st.button("🚀 Recommend Courses", use_container_width=True):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    with st.spinner("Finding the best courses for you..."):

        response = recommend_course(question)

    # ---------------------------------------
    # Recommended Courses
    # ---------------------------------------

    st.subheader("📘 Recommended Courses")

    for course in response["recommended_courses"]:
        st.success(course)

    # ---------------------------------------
    # Reason
    # ---------------------------------------

    st.subheader("📝 Why these courses?")

    st.write(response["reason"])

    # ---------------------------------------
    # Prerequisites
    # ---------------------------------------

    st.subheader("📚 Prerequisites")

    for prerequisite in response["prerequisites"]:
        st.write(f"• {prerequisite}")

    # ---------------------------------------
    # Learning Sequence
    # ---------------------------------------

    st.subheader("🛣 Recommended Learning Path")

    for i, course in enumerate(
        response["learning_sequence"],
        start=1
    ):
        st.write(f"**{i}.** {course}")

    # ---------------------------------------
    # Confidence Score
    # ---------------------------------------

    st.subheader("🎯 Confidence")

    confidence = response["confidence"]

    st.progress(int(confidence * 100))

    st.metric(
        label="Confidence Score",
        value=f"{confidence * 100:.0f}%"
    )

    # ---------------------------------------
    # Source Metadata
    # ---------------------------------------

    st.subheader("📂 Retrieved Source Courses")

    durations = []

    for metadata in response["source_metadata"]:

        durations.append(metadata["duration"])

        with st.expander(metadata["course_name"]):

            st.write(f"**Course ID:** {metadata['course_id']}")
            st.write(f"**Experience Level:** {metadata['experience_level']}")
            st.write(f"**Duration:** {metadata['duration']}")

    # ---------------------------------------
    # Total Learning Hours
    # ---------------------------------------

    total_hours = calculate_total_learning_hours.invoke(
        {
            "durations": durations
        }
    )

    st.subheader("⏱ Total Learning Hours")

    st.metric(
        label="Estimated Hours",
        value=f"{total_hours} Hours"
    )

    # ---------------------------------------
    # Success Message
    # ---------------------------------------

    st.success("✅ Recommendation generated successfully!")