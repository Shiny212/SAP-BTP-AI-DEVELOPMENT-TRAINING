from rag_engine import recommend_course
from tools import calculate_total_learning_hours

print("=" * 60)
print("🎓 Course Recommendation Assistant")
print("=" * 60)

while True:

    question = input("\nAsk your question (type 'exit' to quit): ")

    if question.lower() == "exit":
        print("\nThank you for using Course Recommendation Assistant!")
        break

    response = recommend_course(question)

    print("\nRecommended Courses")
    print("-" * 30)

    for course in response["recommended_courses"]:
        print(f"• {course}")

    print("\nReason")
    print("-" * 30)
    print(response["reason"])

    print("\nPrerequisites")
    print("-" * 30)

    for prerequisite in response["prerequisites"]:
        print(f"• {prerequisite}")

    print("\nLearning Sequence")
    print("-" * 30)

    for index, course in enumerate(response["learning_sequence"], start=1):
        print(f"{index}. {course}")

    print("\nConfidence")
    print("-" * 30)
    print(response["confidence"])

    print("\nSource Metadata")
    print("-" * 30)

    durations = []

    for metadata in response["source_metadata"]:
        print(metadata)
        durations.append(metadata["duration"])

    total_hours = calculate_total_learning_hours.invoke(
        {"durations": durations}
    )

    print("\nTotal Learning Hours")
    print("-" * 30)
    print(total_hours)