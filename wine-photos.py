 #   import os
#    import sys
import streamlit as st
  #  import pandas as pd 
  #  from io import BytesIO_StringIO
  #
# Display a local image
#st.image("./images/wine1.png", caption="Image Caption", use_column_width=True)
#st.image("./images/wine2.png", caption="Image Caption", use_column_width=True)
# st.image("./images/wine5.png", caption="Image Caption", use_column_width=True)

# Create six columns
col1, col2, col3, col4, col5, col6 = st.columns(6)

# Display images in columns
with col1:
    st.image("./images/wine1.png", caption="Image 1")

with col2:
    st.image("./images/wine2.png", caption="Image 2")
    
with col3:
    st.image("./images/wine10.png", caption="Image 3")
    
with col4:
    st.image("./images/wine8.png", caption="Image 4")
    
with col5:
    st.image("./images/wine9.png", caption="Image 5")
    
with col6:
    st.image ("./images/wine3.png", caption="Image 6")
    
    
    
    
    


    

    