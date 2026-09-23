import streamlit as st
import pandas as pd

st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ["About", "Skills", "Experience", "Education", "Contact"])


#            ABOUT SECTION

if section == "About":
    st.title("Desmond")
    st.subheader("Data Analyst | Data Pipelines  &  Analytics")



    st.write("""Welcome to my interactive portfolio!
                                    
                                    
        I am an information science and technology student at the **University of Cape Coast(UCC)**,
        specializing data manipulation,
        exploratory data analysis, and building data web applications.
        My goal is to bridge the gab between raw data retrieval
        and clear interactive business insight.""")
    st.info("**Current Sprint:** Building end-to-end data pipelines using **Python, Pandas, and Streamlit**")


elif section == "Skills":
    st.title("Technical Stack & Tools")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("## **Data Wrangling** & web Applications")
    st.write("* **Python:** Core scripting &" 
    " data manipulation")
    st.write("* **Pandas:** Data cleaning, aggregation," 
    " logic filtering")
    st.write("* **Streamlit:** Interactive dashboard",
    " UI deployment")

    with col2:
        st.markdown("### Analytics & Foundations")
    st.write("* **Core Concepts:** Statistics & Applied Linear Algebra")
    st.write("* **Languages:** English, Ghanaian Sign Language")



#            EXPERIENCE SECTION

elif section == "Experience":
    st.title("Experience & project")

    st.markdown("### Portfolio Projects")
    with st.expander("Streamlit Data web Application (Current)"):
        st.write(""" * Designed an interactive web application
    using Python, Pandas and Streamlit.
      * Implemented dynamic filtering 
    and custom data processing with pandas.
    * Structure optimized for rapid deployment and user  
    navigation.""")

    with st.expander(" Exploratory Data Analysis Practice, & Visualization"):
        
     st.write(""" * Conducted staistical analyses, calculated means,
    and handled dataset outliers. 
   * Structured clean tabular data for analysis and visualization.
    """)
    st.markdown("### Work History")
    st.write("""Managed equipment operation and material movement with high 
    attention to precision and safety.
    * Building strong work discipline, task planning, and 
    operational reliability""")


#            EDUCATION SECTION
elif section == "Education":
    st.title("Education")

    st.markdown("### Bachelor of Arts (BA) in information science and technology,")
    st.caption("University of Cape Coast (UCC), Ghana")
    st.write(""" * **Core Focus:** Information systems, Data Analytics,
           & System management, Web development.
            * **Relevance Coursework:**
            Statistics, Computer Architecture, system Design,digital literacy, marketing of information services,
            Database Management""")
    
    
    #          CONTACT SECTION
elif section == "Contact":
    st.header("Get In Touch")
    col1, col2 = st.columns(2)
    with col1:
        email = st.text_input("Email")
        phone = st.text_input("Contact")

    with col2:
        linkedin = st.text_input("Linkedin")
        Discord = st.text_input("Discord")  
        
    message = st.text_area("Leave a message")
if st.button("Send"):
    st.success("Thanks for reaching out, we will be in contact shortly")


