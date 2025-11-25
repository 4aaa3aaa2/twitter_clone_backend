import requests


class UserIdentityUtils:
    @staticmethod
    def parse_google_display_name(firstname: str, lastname: str, suffix: int)->str:
        if firstname and firstname!="":
            if lastname and lastname!="":
                return firstname+" "+lastname
            else:
                return firstname
        else:
            return f"temp account {suffix}"
    @staticmethod
    def parse_google_user_name(first_name: str | None, last_name: str | None, suffix: int) -> str:
        base_name = first_name.lower() if first_name and first_name.strip() else "user"
        return f"{base_name}{suffix}"
    
    @staticmethod
    def parse_google_user_info(access_token: str)->dict:
        google_user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"

        headers = {
            "Authorization": f"Bearer {access_token}"
        }

        response = requests.get(google_user_info_url, headers=headers)
        response.raise_for_status()  # raise an error if the request failed

        return response.json()
    