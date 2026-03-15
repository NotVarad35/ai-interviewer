import os
from google import genai

def test_llm():
    # 1. Initialize the client 
    client = genai.Client()
    # 2. UPDATED Seed Data: Jellyfin, Immich, ARR stack, and TrueNAS SMB
    candidate_transcript = (
        "In my current homelab setup, I'm running a Proxmox cluster across three bare-metal nodes. "
        "I've segregated my network using pfSense, setting up strict firewall rules and dedicated VLANs "
        "for my IoT devices, guest Wi-Fi, and my management interfaces. For storage, I have a TrueNAS "
        "virtual machine utilizing PCIe passthrough for the HBA card. I host most of my services using Docker, "
        "exposed to the outside world via Traefik as a reverse proxy, secured behind Cloudflare Tunnels. "
        "Lately, I've been expanding my media and backup setup with Jellyfin, Immich, and the full ARR stack. "
        "They are all running in separate Docker containers, but I'm running into some frustrating permission denied errors "
        "and volume path-mapping issues when the ARR apps try to move completed files over to my TrueNAS SMB shares."
    )

    # 3. UPDATED Prompt 1: Explicitly guiding the LLM toward UID/GID and path-mapping scenarios
    prompt = f"""You are an expert IT technical interviewer evaluating a senior professional. 

    Based on the following transcript provided by the candidate, identify the core technologies they mentioned. 
    Generate one highly realistic, complex troubleshooting scenario involving those specific technologies. 
    Focus the scenario specifically on Docker container volume mapping, UID/GID permission mismatches across network shares (TrueNAS), and reverse proxy routing.
    Do not ask for definitions. End your response with a direct question asking how they would resolve the scenario.

    Candidate Transcript:
    "{candidate_transcript}"
    """

    print("Sending updated candidate transcript to Gemini 2.5 Flash...")
    
    try:
        # 4. Send the prompt to the model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt
        )
        
        print("\n--- AI Interviewer Response ---")
        print(response.text)
        print("-------------------------------")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_llm()