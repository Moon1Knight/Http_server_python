import requests
import time

def check_server():
    url = "http://localhost:4221"
    while True:
        try:
            # Test root endpoint
            response = requests.get(url)
            if response.status_code == 200:
                print("Root endpoint is working.")
            else:
                print(f"Unexpected response at root endpoint: {response.status_code}")

            # Test file upload (POST request)
            test_file_content = "This is a test file content."
            test_file_name = "testfile.txt"
            files_url = f"{url}/files/{test_file_name}"
            response = requests.post(files_url, data=test_file_content)
            if response.status_code == 201:
                print("File upload (POST) is working.")
            else:
                print(f"Unexpected response at file upload: {response.status_code}")

            # Test file retrieval (GET request)
            response = requests.get(files_url)
            if response.status_code == 200 and response.text == test_file_content:
                print("File retrieval (GET) is working.")
            else:
                print(f"Unexpected response at file retrieval: {response.status_code}")

            # Test echo endpoint
            echo_message = "HelloServer"
            echo_url = f"{url}/echo/{echo_message}"
            response = requests.get(echo_url)
            if response.status_code == 200 and response.text == echo_message:
                print("Echo endpoint is working.")
            else:
                print(f"Unexpected response at echo endpoint: {response.status_code}")

            # Test user-agent endpoint
            user_agent_url = f"{url}/user-agent"
            response = requests.get(user_agent_url)
            if response.status_code == 200:
                print("User-agent endpoint is working.")
            else:
                print(f"Unexpected response at user-agent endpoint: {response.status_code}")

        except Exception as e:
            print(f"Server check failed: {e}")

        # Wait for a minute before the next check
        time.sleep(60)

if __name__ == "__main__":
    check_server()
