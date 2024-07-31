import pickle
import pandas as pd
import numpy as np
import streamlit as st
import base64

categorical_cols = ['area_type', 'loc_tag']
numerical_cols = ['bath', 'balcony', 'area_sqft', 'bedrooms', 'R2M']

pickle_in = open('house_price_blr_model.pkl', 'rb') 
model = pickle.load(pickle_in)

with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)



def predict_price(area_type, bath, balcony, area_sqft, bedrooms, R2M, loc_tag):
  new_data = {'area_type':[area_type], 'bath':[bath], 'balcony':[balcony], 'area_sqft':[area_sqft], 'bedrooms':[bedrooms], 'R2M':[R2M], 'loc_tag':[loc_tag]}
  new_df = pd.DataFrame(new_data)

  # Preprocess new data
  new_data_encoded = encoder.transform(new_df[categorical_cols])
  new_df_encoded = pd.concat([new_df[numerical_cols], pd.DataFrame(new_data_encoded, columns=encoder.get_feature_names_out())], axis=1)

  predicted_price = model.predict(new_df_encoded)
  return round(predicted_price[0]*1.5,2)



def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % encoded_string
    st.markdown(page_bg_img, unsafe_allow_html=True)


    

def main(): 
    
    html_temp = """ 
	<div style ="background-color:yellow;padding:13px"> 
	<h1 style ="color:black;text-align:center;">Bengaluru Flat Price Prediction App</h1> 
	</div> 
	"""
	# this line allows us to display the front end aspects we have 
	# defined in the above code 
    st.markdown(html_temp, unsafe_allow_html = True) 
    st.markdown("Caution: This app is trained on very less data and it may show unreliable prediction !")
	# the following lines create text boxes in which the user can enter 
	# the data required to make the prediction
	# Create the dropdown
    options_area_type = ['Carpet__Area', 'Built-up__Area', 'Super_built-up__Area', 'Plot__Area']
    area_type = st.selectbox('Select area type:', options_area_type)
    area_sqft = st.number_input('Area in squarefeet', min_value=150)
    bath_options = [1,2,3]
    bath = st.selectbox('Select number of bathrooms:', bath_options)
    bedroom_options = [1,2,3,4]
    bedrooms = st.selectbox('Select number of bedrooms:', bedroom_options)
    balcony_options = [1,2,3]
    balcony = st.selectbox('Select number of balconies:', balcony_options)
    R2M_options = ['Yes','No']
    R2M_dict = {'Yes':1,'No':0}
    R2M_ = st.selectbox('Select whether Ready to Move:', R2M_options)
    R2M = R2M_dict[R2M_]
    loc_tag_options = ['other', 'KR', 'Raja', 'Malleshwaram', 'Varthur', 'Hoodi', 'Thigalarapalya',
 'Haralur', 'Palaya', 'Thanisandra',  'Hebbal', 'Begur', 'Uttarahalli', 'Jakkur', 'Bisuvanahalli',
 'Koramangala', 'Bellandur', 'Kothanur', 'bhavi', 'Ramamurthy', 'Kaggadasapura', 'Yeshwanthpur', 'Jalahalli',
 'Bannerghatta', 'Marathahalli', 'Yelahanka', 'Sarjapur', 'Hormavu', 'Rachenahalli', 'Electronic', 'Kengeri',
 'Hosa', 'Madras', 'Puram', 'Akshaya', 'Kanakpura', 'Budigere', 'TC', 'JP', 'Harlur',
 'Whitefield', 'Kasavanhalli', 'Banashankari', 'Panathur', 'Chandapura', 'Hennur']
    loc_tag = st.selectbox('Select the location suitable otherwise select other:', loc_tag_options)
	#height = st.number_input(label="enter the height in cm (in integer format)", min_value=100) 
    result = 0 
	
	# the below line ensures that when the button called 'Predict' is clicked, 
	# the prediction function defined above is called to make the prediction 
	# and store it in the variable result 
    if st.button("Calculalte the predicted price"):
        result = predict_price(area_type, bath, balcony, area_sqft, bedrooms, R2M, loc_tag)
        st.markdown(
        f"""
        <div style='background-color: #006400; color: white; padding: 10px; border-radius: 5px;'>
        The predicted price is: {round(float(result),2)} Lakh INR
        </div>
        """,
        unsafe_allow_html=True)
    #st.success(f'The price is {round(float(result),2)} Lakh Rupees') 


if __name__=='__main__':
     image_file = "BLR01.PNG"  # Replace with your image path
     add_bg_from_local(image_file)
     main()