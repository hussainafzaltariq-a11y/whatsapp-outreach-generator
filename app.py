import streamlit as st
import pandas as pd
from message_generator import MessageGenerator
from utils.csv_handler import CSVHandler
from utils.templates import MessageTemplates
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="WhatsApp Outreach Generator",
    page_icon="💬",
    layout="wide"
)

def load_csv_safe(file):
    """Load CSV with automatic encoding detection"""
    try:
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']:
            try:
                if hasattr(file, 'seek'):
                    file.seek(0)
                df = pd.read_csv(file, encoding=encoding)
                return df
            except:
                continue
        raise Exception("Could not read CSV file")
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def main():
    # Title and description
    st.title("💬 WhatsApp Outreach Message Generator")
    st.markdown("Generate personalized WhatsApp messages for your leads using AI")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Use AI Generation toggle
        use_ai = st.checkbox("Use AI Generation (OpenAI)", value=True)
        
        # OpenAI API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv("OPENAI_API_KEY", ""),
            help="Get your API key from https://platform.openai.com/api-keys"
        )
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        
        # Temperature slider
        temperature = st.slider(
            "Creativity (Temperature)",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.1,
            help="Higher = more creative, Lower = more focused"
        )
        
        # Message Style
        st.subheader("Message Style")
        style = st.selectbox(
            "Select Style",
            ["Professional", "Casual", "Friendly", "Formal", "Persuasive"]
        )
        
        st.divider()
        st.markdown("### 📊 Statistics")
        if 'generated_df' in st.session_state and st.session_state['generated_df'] is not None:
            df = st.session_state['generated_df']
            st.metric("Total Leads", len(df))
            st.metric("Messages Generated", len(df[df['generated_message'].notna()]))

    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Generate", "📋 View Messages", "ℹ️ How to Use"])

    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Upload Leads Data")
            st.markdown("Upload CSV file with leads")
            
            uploaded_file = st.file_uploader(
                "Choose a CSV file",
                type=['csv'],
                help="CSV must contain: business_name, business_type, pain_point, contact_name (optional)",
                label_visibility="collapsed"
            )
            
            if uploaded_file is not None:
                df = load_csv_safe(uploaded_file)
                
                if df is not None:
                    st.success(f"✅ Loaded {len(df)} leads")
                    
                    # Display preview
                    st.subheader("📊 Data Preview")
                    st.dataframe(df.head())
                    
                    # Generate messages button
                    if st.button("🚀 Generate Messages", type="primary", use_container_width=True):
                        if not api_key and use_ai:
                            st.error("⚠️ Please enter your OpenAI API key in the sidebar")
                        else:
                            with st.spinner("Generating personalized messages..."):
                                generator = MessageGenerator(api_key=api_key, temperature=temperature)
                                
                                # Generate messages
                                df = generator.generate_messages(df)
                                
                                # Store in session state
                                st.session_state['generated_df'] = df
                                
                                st.success(f"✅ Generated messages for {len(df)} leads!")
                                st.balloons()
                                
                                # Download button
                                csv = CSVHandler.save_csv(df)
                                st.download_button(
                                    label="📥 Download CSV with Messages",
                                    data=csv,
                                    file_name="generated_messages.csv",
                                    mime="text/csv",
                                    use_container_width=True
                                )
            
            # Sample data section
            st.divider()
            st.subheader("Or use sample data to preview:")
            
            if st.button("📊 Load Sample Data & Generate", type="secondary", use_container_width=True):
                try:
                    # Try to load sample data
                    try:
                        sample_df = pd.read_csv('sample_leads.csv', encoding='utf-8')
                    except:
                        try:
                            sample_df = pd.read_csv('sample_leads.csv', encoding='latin-1')
                        except:
                            # Create sample data if file doesn't exist
                            sample_data = {
                                'business_name': ['Taste of Italy', 'CloudSync Solutions', 'Digital Spark Media', 'GreenLeaf Organics', 'TechTutors Inc'],
                                'business_type': ['Restaurant', 'SaaS', 'Agency', 'Retail', 'Education'],
                                'pain_point': ['high employee turnover and inconsistent food quality', 
                                              'difficulty retaining customers after initial signup',
                                              'managing multiple client campaigns with limited resources',
                                              'supply chain disruptions affecting inventory',
                                              'low student engagement in online courses'],
                                'contact_name': ['Marco', 'Sarah', 'James', 'Emma', 'David']
                            }
                            sample_df = pd.DataFrame(sample_data)
                            sample_df.to_csv('sample_leads.csv', index=False)
                    
                    st.session_state['sample_df'] = sample_df
                    
                    # Generate messages
                    if not api_key and use_ai:
                        st.error("⚠️ Please enter your OpenAI API key in the sidebar")
                    else:
                        with st.spinner("Generating sample messages..."):
                            generator = MessageGenerator(api_key=api_key, temperature=temperature)
                            sample_df = generator.generate_messages(sample_df)
                            st.session_state['generated_df'] = sample_df
                        
                        st.success("✅ Sample data loaded and messages generated!")
                        st.balloons()
                        
                except Exception as e:
                    st.error(f"Error loading sample data: {str(e)}")

    with tab2:
        if 'generated_df' in st.session_state and st.session_state['generated_df'] is not None:
            df = st.session_state['generated_df']
            
            # Show all generated messages
            for idx, row in df.iterrows():
                with st.expander(f"💬 {row.get('business_name', 'Business')} - {row.get('contact_name', 'Contact')}"):
                    st.markdown(f"**Message:**\n\n{row.get('generated_message', 'No message generated')}")
                    
                    # Copy button
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if st.button(f"📋 Copy", key=f"copy_{idx}"):
                            st.write("✅ Copied to clipboard!")
                            st.code(row.get('generated_message', ''))
        else:
            st.info("📭 No messages generated yet. Upload a CSV and generate messages in the Upload tab.")

    with tab3:
        st.markdown("""
        ### 📖 How to Use This Tool
        
        **Step 1: Prepare your CSV file** with the following columns:
        - `business_name`: Name of the business (required)
        - `business_type`: Type of business (required)
        - `pain_point`: The problem you're solving for them (required)
        - `contact_name`: Name of the contact person (optional)
        
        **Step 2: Get your OpenAI API Key**:
        - Sign up at [OpenAI Platform](https://platform.openai.com)
        - Go to API Keys section
        - Create a new key and copy it
        
        **Step 3: Enter your API Key** in the sidebar
        
        **Step 4: Upload your CSV** and click Generate
        
        **Step 5: Download** the results or copy individual messages
        
        ### 🎯 Tips for Best Results
        - Be specific with pain points
        - Add a contact name for personalization
        - Adjust temperature for different tones
        - Review and customize messages before sending
        - Use sample data to test first
        
        ### 🛠️ Tech Stack
        - Python 3.13
        - Streamlit
        - OpenAI API
        - Pandas
        """)

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: gray; padding: 20px;'>
        Made with ❤️ for Internship Project | WhatsApp Outreach Message Generator
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()