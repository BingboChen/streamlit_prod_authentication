import os
import streamlit as st
import google_auth_oauthlib.flow
import webbrowser
import json
import urllib.parse

# Initialize session state variables
if 'credentials' not in st.session_state:
    st.session_state['credentials'] = None

redirect_uri = "https://appappappentication-nkut58a4ijjpd75cuelejh.streamlit.app/"
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly', 'https://www.googleapis.com/auth/yt-analytics.readonly']


def main():
    st.write("Welcome to My App!")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        "client_secrets.json", 
        scopes=SCOPES,
        redirect_uri=redirect_uri,
    )
    
    if st.button("Sign in with Google"):
        # Generate the authorization URL and direct the user to it
        authorization_url, state = flow.authorization_url(
            access_type="online",
            include_granted_scopes="true",
        )
        # Generate a clickable link for the user
        link = f'<a href="{authorization_url}" target="_blank">Authorize with Google</a>'
        st.markdown(link, unsafe_allow_html=True)
        
    full_url = st.text_input(
        "Enter some text 👇"
    )
    
    if full_url:
        parsed_url = urllib.parse.urlparse(full_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        
        # Extract the authorization code from the query parameters
        if 'code' in query_params:
            # The query params are returned as lists, so get the first item
            auth_code = query_params['code'][0]
            # Decode the URL-encoded authorization code
            decoded_code = urllib.parse.unquote(auth_code)
            st.write(decoded_code)
            # Use this decoded_code to fetch the token as before
            flow.fetch_token(code=decoded_code)
            
            credentials = flow.credentials
            st.session_state['credentials'] = credentials
            
            # 5. Save the Credentials
            credentials_dict = {
                'token': credentials.token,
                'refresh_token': credentials.refresh_token,
                'token_uri': credentials.token_uri,
                'client_id': credentials.client_id,
                'client_secret': credentials.client_secret,
                'scopes': credentials.scopes,
            }
            credentials_json = json.dumps(credentials_dict, indent=4)
            st.text_area("Credentials JSON", credentials_json, height=500)

            print("Credentials saved to credentials.json")


if __name__ == '__main__':
    main()