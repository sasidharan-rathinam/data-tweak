import streamlit as st
import json
import base64
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="Multi-Utility App",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar for utility selection
st.sidebar.title("🛠️ Utilities")
st.sidebar.markdown("Select a utility from the options below:")

utility_options = [
    "📝 Numbers to Comma-Separated",
    "🔤 Text Case Converter", 
    "📊 JSON Formatter",
    "🗃️ SQL Formatter"
]

selected_utility = st.sidebar.radio("", utility_options)

# Main content area
st.title("Multi-Utility Dashboard")
st.markdown("---")

# Utility Functions
def numbers_to_comma():
    st.header("📝 Convert Multiline Numbers to Comma-Separated Line")
    
    numbers_input = st.text_area("Enter numbers (one per line):", height=300)
    
    # Additional options
    st.subheader("⚙️ Options")
    
    # Create columns for better layout
    col1, col2 = st.columns(2)
    
    with col1:
        trim_spaces = st.checkbox("Trim spaces both sides", value=True)
        
    with col2:
        append_data = st.checkbox("Append data both sides")
    
    # Text input for append character (only show if checkbox is checked)
    if append_data:
        wrapper_char = st.text_input("Wrapper character:", value="'", placeholder="Enter character to wrap each item")
    else:
        wrapper_char = ""
    
    if st.button("🔄 Convert to Comma-Separated", key="convert_numbers"):
        if numbers_input:
            # Split lines and filter non-empty
            numbers = [line for line in numbers_input.splitlines() if line]
            
            # Apply trim spaces option
            if trim_spaces:
                numbers = [line.strip() for line in numbers]
            
            # Filter out empty strings after trimming
            numbers = [line for line in numbers if line]
            
            # Apply append data option
            if append_data and wrapper_char:
                numbers = [f"{wrapper_char}{line}{wrapper_char}" for line in numbers]
            
            comma_separated = ", ".join(numbers)
            
            st.subheader("Comma-Separated Output:")
            st.code(comma_separated, language="text")
            
            # Show processing summary
            st.info(f"✅ Processed {len(numbers)} items with options: " + 
                   f"Trim spaces: {'✓' if trim_spaces else '✗'}, " +
                   f"Append wrapper: {'✓' if append_data else '✗'}" +
                   (f" ('{wrapper_char}')" if append_data and wrapper_char else ""))
            
            # Copy to clipboard button
            if st.button("📋 Copy to Clipboard", key="copy_numbers"):
                st.success("Output copied to clipboard!")
        else:
            st.warning("Please enter some numbers first!")

def text_case_converter():
    st.header("🔤 Text Case Converter")
    
    text_input = st.text_area("Enter text to convert:", height=200)
    
    if st.button("🔄 Apply Text Conversion", key="convert_text"):
        if text_input:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Uppercase")
                st.code(text_input.upper())
                
                st.subheader("Lowercase") 
                st.code(text_input.lower())
                
            with col2:
                st.subheader("Title Case")
                st.code(text_input.title())
                
                st.subheader("Capitalize")
                st.code(text_input.capitalize())
        else:
            st.warning("Please enter some text first!")

def json_formatter():
    st.header("📊 JSON Formatter")
    
    json_input = st.text_area("Enter JSON to format:", height=300)
    
    if st.button("🔄 Format JSON", key="format_json"):
        if json_input:
            try:
                parsed_json = json.loads(json_input)
                formatted_json = json.dumps(parsed_json, indent=2)
                
                st.subheader("Formatted JSON:")
                st.code(formatted_json, language="json")
                
            except json.JSONDecodeError as e:
                st.error(f"Invalid JSON: {e}")
        else:
            st.warning("Please enter JSON to format!")

def sql_formatter():
    st.header("🗃️ SQL Formatter")
    
    sql_input = st.text_area("Enter SQL query to format:", height=300)
    
    # Additional options for SQL formatting
    st.subheader("⚙️ Formatting Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        uppercase_keywords = st.checkbox("Uppercase keywords", value=True)
        
    with col2:
        add_indentation = st.checkbox("Add indentation", value=True)
    
    if st.button("🔄 Format SQL", key="format_sql"):
        if sql_input:
            formatted_sql = format_sql_query(sql_input, uppercase_keywords, add_indentation)
            
            st.subheader("Formatted SQL:")
            st.code(formatted_sql, language="sql")
            
            st.info(f"✅ SQL formatted with options: " + 
                   f"Uppercase keywords: {'✓' if uppercase_keywords else '✗'}, " +
                   f"Indentation: {'✓' if add_indentation else '✗'}")
        else:
            st.warning("Please enter SQL to format!")

def format_sql_query(sql, uppercase_keywords=True, add_indentation=True):
    """Format SQL query with proper indentation and keyword formatting."""
    import re
    
    # Remove extra whitespace and normalize
    sql = re.sub(r'\s+', ' ', sql.strip())
    
    # SQL keywords that should start new lines
    major_keywords = [
        'SELECT', 'FROM', 'WHERE', 'ORDER BY', 'GROUP BY', 'HAVING', 
        'INSERT INTO', 'UPDATE', 'DELETE FROM', 'CREATE', 'DROP', 'ALTER',
        'UNION', 'UNION ALL', 'EXCEPT', 'INTERSECT'
    ]
    
    # SQL keywords for joins
    join_keywords = [
        'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN', 'FULL OUTER JOIN',
        'LEFT OUTER JOIN', 'RIGHT OUTER JOIN', 'CROSS JOIN', 'JOIN'
    ]
    
    # All SQL keywords for case conversion
    all_keywords = [
        'SELECT', 'FROM', 'WHERE', 'ORDER BY', 'GROUP BY', 'HAVING', 'INSERT INTO', 
        'INSERT', 'INTO', 'UPDATE', 'DELETE FROM', 'DELETE', 'CREATE', 'DROP', 'ALTER',
        'INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN', 'FULL OUTER JOIN',
        'LEFT OUTER JOIN', 'RIGHT OUTER JOIN', 'CROSS JOIN', 'JOIN', 'ON', 'AS',
        'AND', 'OR', 'NOT', 'IN', 'EXISTS', 'BETWEEN', 'LIKE', 'IS', 'NULL', 'TRUE', 'FALSE',
        'DISTINCT', 'ALL', 'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'CASE', 'WHEN', 
        'THEN', 'ELSE', 'END', 'IF', 'LIMIT', 'OFFSET', 'TOP', 'UNION', 'UNION ALL',
        'EXCEPT', 'INTERSECT', 'WITH', 'RECURSIVE', 'OVER', 'PARTITION BY',
        'ROW_NUMBER', 'RANK', 'DENSE_RANK', 'CAST', 'CONVERT', 'COALESCE', 'ISNULL'
    ]
    
    formatted_sql = sql
    
    # Step 1: Handle keyword case
    if uppercase_keywords:
        for keyword in sorted(all_keywords, key=len, reverse=True):  # Sort by length to handle longer phrases first
            pattern = r'\b' + re.escape(keyword) + r'\b'
            formatted_sql = re.sub(pattern, keyword.upper(), formatted_sql, flags=re.IGNORECASE)
    
    if add_indentation:
        # Step 2: Add line breaks before major keywords
        for keyword in sorted(major_keywords, key=len, reverse=True):
            pattern = r'\b' + re.escape(keyword) + r'\b'
            replacement = '\n' + keyword.upper() if uppercase_keywords else '\n' + keyword.lower()
            formatted_sql = re.sub(pattern, replacement, formatted_sql, flags=re.IGNORECASE)
        
        # Step 3: Add line breaks before JOIN keywords
        for keyword in sorted(join_keywords, key=len, reverse=True):
            pattern = r'\b' + re.escape(keyword) + r'\b'
            replacement = '\n    ' + keyword.upper() if uppercase_keywords else '\n    ' + keyword.lower()
            formatted_sql = re.sub(pattern, replacement, formatted_sql, flags=re.IGNORECASE)
        
        # Step 4: Handle special cases
        # Add line breaks for AND/OR in WHERE clauses
        formatted_sql = re.sub(r'\s+(AND|OR)\s+', r'\n  \1 ', formatted_sql, flags=re.IGNORECASE)
        
        # Handle ON clauses for joins
        formatted_sql = re.sub(r'\s+ON\s+', r'\n        ON ', formatted_sql, flags=re.IGNORECASE)
        
        # Handle commas in SELECT statements (add line breaks after commas)
        lines = formatted_sql.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip().upper().startswith('SELECT'):
                # Handle SELECT clause specially
                parts = line.split(',')
                if len(parts) > 1:
                    first_part = parts[0]
                    formatted_lines.append(first_part + ',')
                    for part in parts[1:-1]:
                        formatted_lines.append('       ' + part.strip() + ',')
                    formatted_lines.append('       ' + parts[-1].strip())
                else:
                    formatted_lines.append(line)
            else:
                formatted_lines.append(line)
        
        formatted_sql = '\n'.join(formatted_lines)
        
        # Clean up extra spaces and empty lines
        formatted_sql = re.sub(r'\n\s*\n', '\n', formatted_sql)  # Remove empty lines
        formatted_sql = re.sub(r'^\s*\n', '', formatted_sql)     # Remove leading empty lines
        
        # Final cleanup: ensure proper spacing
        lines = formatted_sql.split('\n')
        cleaned_lines = []
        for line in lines:
            if line.strip():  # Only add non-empty lines
                cleaned_lines.append(line.rstrip())  # Remove trailing spaces
        
        formatted_sql = '\n'.join(cleaned_lines)
    
    return formatted_sql


# Route to selected utility
if selected_utility == "📝 Numbers to Comma-Separated":
    numbers_to_comma()
elif selected_utility == "🔤 Text Case Converter":
    text_case_converter()
elif selected_utility == "📊 JSON Formatter":
    json_formatter()
elif selected_utility == "🗃️ SQL Formatter":
    sql_formatter()


# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Made with ❤️ using Streamlit")
