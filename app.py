import streamlit as st
import pandas as pd
import plotly.express as px

# Set the page config as the first Streamlit command
st.set_page_config(
    page_title="Live Movies Ranking in Riyadh",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Define the CSS style
custom_css = """
<style>
body {
    direction: rtl;
    text-align: right;
    font-family: Arial, sans-serif;
}

.sidebar .sidebar-content {
    direction: ltr;
    text-align: left;
}
</style>
"""

# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar configuration
page = st.sidebar.radio("Navigation", ["Home", "Movie Details", "Feedback", "Contact with us"])

if page == "Home":
    # Main page title
    st.title("ايش الناس تشوف الحين؟ 🎥 ")
    st.markdown("---")

    st.markdown("### خذ الزبدة من عندنا ! ")

    # Load movie details from CSV
    movie_details = pd.read_csv("movie_details.csv")

    # Get the top 1 movie
    top_movie = movie_details.head(1).iloc[0]

    # Define a custom CSS style for centering text
    custom_css = """
    <style>
    .centered-text {
        text-align: center;
    }
    </style>
    """

    # Apply the custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Displaying the text with the fire emoji in the middle
    st.markdown(
        """
        <h3 class="centered-text">🔥 فلم الليلة 🔥</h3>
        """,
        unsafe_allow_html=True
    )

      # Define a custom CSS style for background# Define a custom CSS style for background with bigger font and centered text
    custom_css = """
    <style>
    .box {
        background-color: #005050; /* Set background color */
        padding: 10px; /* Add padding for spacing */
        border-radius: 5px; /* Add rounded corners */
        margin-bottom: 10px; /* Add margin for spacing */
        text-align: center; /* Center align text */
    }

    .box p {
        font-size: 20px; /* Set font size */
        margin: 0; /* Remove default margin */
    }
    </style>
    """

    # Apply the custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Displaying each element in a box with background
    st.markdown(
        f"""
        <div class="box">
            <p> {top_movie['Movie Title']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="box">
            <p> {top_movie['Rating']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="box">
            <p> {top_movie['Genres']}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Load seat availability data
    today_data = pd.read_csv("seat_counts_unique_WEDNESDAY.csv")
    yesterday_data = pd.read_csv("seat_counts_unique_MONDAY.csv")
    last_two_days_data = pd.concat([today_data, yesterday_data])

    # Calculate percentage of unavailable seats for each time frame
    today_unavailable_percent = (today_data["Unavailable Seats"] / (today_data["Available Seats"] + today_data["Unavailable Seats"])) * 100
    yesterday_unavailable_percent = (yesterday_data["Unavailable Seats"] / (yesterday_data["Available Seats"] + yesterday_data["Unavailable Seats"])) * 100
    last_two_days_unavailable_percent = (last_two_days_data["Unavailable Seats"] / (last_two_days_data["Available Seats"] + last_two_days_data["Unavailable Seats"])) * 100
    st.markdown("---")

    busy_hours_css = """
    <style>
    .busy-hours-container {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
    }

    .busy-hours-item {
        background-color: #005050;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        width: 30%;
    }

    .busy-hours-title {
        font-weight: bold;
        font-size: 20px;
        margin-bottom: 10px;
    }

    .busy-hours-value {
        font-size: 18px;
    }
    </style>
    """

    # Apply the custom CSS
    st.markdown(busy_hours_css, unsafe_allow_html=True)

    # Display busy hours section
    st.subheader("نسبات  ' الزحمة 😵‍💫 ' ")
    st.markdown(
        """
        <div class="busy-hours-container">
            <div class="busy-hours-item">
                <p class="busy-hours-title">الآن</p>
                <p class="busy-hours-value">70%</p>
            </div>
            <div class="busy-hours-item">
                <p class="busy-hours-title">أمس</p>
                <p class="busy-hours-value">65%</p>
            </div>
            <div class="busy-hours-item">
                <p class="busy-hours-title">آخر يومين</p>
                <p class="busy-hours-value">75%</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")  # Add a line to separate the busy hours section

    # Buttons for different time frames
    st.subheader("اختر الفترة الزمنية:")

    col1, col2, col3 = st.columns(3)

    if col1.button("الآن"):
        st.write("عرض بيانات المقاعد المتاحة الآن.")
        top_today_data = today_data.sort_values(by="Available Seats", ascending=False).head(5)
        fig = px.pie(top_today_data, values='Available Seats', names='Movie Name')
        st.plotly_chart(fig)

    if col2.button("أمس"):
        st.write("عرض بيانات المقاعد المتاحة في أمس.")
        top_yesterday_data = yesterday_data.sort_values(by="Available Seats", ascending=False).head(5)
        fig = px.pie(top_yesterday_data, values='Available Seats', names='Movie Name')
        st.plotly_chart(fig)

    if col3.button("آخر يومين"):
        st.write("عرض بيانات المقاعد المتاحة في اليومين الأخيرين.")
        top_last_two_days_data = last_two_days_data.sort_values(by="Available Seats", ascending=False).head(5)
        fig = px.pie(top_last_two_days_data, values='Available Seats', names='Movie Name')
        st.plotly_chart(fig)

elif page == "Movie Details":
    # Sidebar movie information
    st.title("🎬 تفاصيل الفيلم")

    # Load movie details from CSV
    movie_details = pd.read_csv("movie_details.csv")

    # Display dropdown to select movie
    selected_movie = st.selectbox("اختر فيلمًا:", movie_details["Movie Title"].tolist(), key="movie_dropdown")

    # Filter movie details based on selected movie
    movie_info = movie_details[movie_details["Movie Title"] == selected_movie].iloc[0]

    # Create a container to hold movie details
    details_container = st.container()

    # Display movie rating
    with details_container:
        st.subheader("التقييم")
        st.markdown(f"<p style='font-size: 20px; text-align: center;'>{movie_info['Rating']}</p>", unsafe_allow_html=True)

    # Display movie genres
    with details_container:
        st.subheader("النوع")
        st.markdown(f"<p style='font-size: 20px; text-align: center;'>{movie_info['Genres']}</p>", unsafe_allow_html=True)

    # Display movie plot
    with details_container:
        st.subheader("القصة")
        st.write(movie_info['Plot'])

    # Add interactivity - show additional information on button click
    if st.button("عرض معلومات إضافية"):
        # Additional information to display
        additional_info = {
            "Directors": movie_info.get("Directors", "غير معروف"),
            "Actors": movie_info.get("Actors", "غير معروف"),
            "Release Date": movie_info.get("Release Date", "غير معروف"),
            "Runtime": movie_info.get("Runtime", "غير معروف"),
        }

        # Display additional information
        with details_container:
            st.subheader("معلومات إضافية")
            for key, value in additional_info.items():
                st.markdown(f"**{key}:** {value}")

elif page == "Feedback":
    # Sidebar for feedback
    st.title("اكتب رايك ترا مانعلم احد 🤐")

    # Rating scale with emoji ratings
    st.subheader("كيف تقيم تجربتك مع التطبيق؟")
    ratings = {
        "😞": "😞 ضعيف",
        "😐": "😐 مقبول",
        "😊": "😊 جيد",
        "😍": "😍 ممتاز"
    }
    rating = st.radio("", list(ratings.keys()), format_func=lambda x: ratings[x], key="rating")
    st.markdown("---")

    # Feedback comment textbox
    st.subheader("فضفض هنا ..")
    comment = st.text_area(" ", key="feedback", height=150)

    # Send feedback button
    if st.button("إرسال", key="send_feedback", help="ارسل"):
        # Save feedback to CSV file
        feedback_data = {"Rating": [ratings[rating]], "Comment": [comment]}
        feedback_df = pd.DataFrame(feedback_data)
        feedback_df.to_csv("feedback.csv", index=False, mode="a", header=not st.session_state.get("csv_exists", False))
        st.session_state["csv_exists"] = True  # Flag to prevent adding headers after the first entry

        # Success message
        st.success("ابو خالد وصله العلم ..")

elif page == "Contact with us":
    # Sidebar for contact information
    st.subheader("يمكنك التواصل معنا على LinkedIn:")

    # Define LinkedIn profiles
    linkedin_profiles = {
        "Mohammed Alaklabi": "https://www.linkedin.com/in/mohammed-alaklabi-0450092a4",
        "Ahmed Alhassan": "https://www.linkedin.com/in/ahmed-alhassan-4b86242b9/",
        "Abdullah Altuwayjiri": "https://www.linkedin.com/in/abdullah-aaltuwayjiri/",
        "Faisal Alossaimi": "https://www.linkedin.com/in/faisal-alossaimi-1313542a4/"
    }

    # Define custom CSS style for larger font size
    custom_css = """
    <style>
    .larger-text {
        font-size: 40px;
    }
    </style>
    """

    # Apply the custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Display LinkedIn profiles with larger font size
    for name, profile_link in linkedin_profiles.items():
        st.markdown(f"- <span class='larger-text'><a href='{profile_link}'>{name}</a></span>", unsafe_allow_html=True)

# Footer
st.markdown("---")
