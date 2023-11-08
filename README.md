# Privacy Explorer

This repository describes a simple system that helps explore privacy policies.

## Setup

To set up the project, follow these steps:

1. Clone the repository.
2. Install the required packages. In your terminal, navigate to the project directory and run the following command:

```bash
pip install -r requirements.txt
```

3. Setup a file called `secrets.json`
   ```json
   {
     "API_KEY": "openaiapikey"
   }   
   ```


## Flows

This explorer exposes two main flows:


### Flow 1
- We use GPT to ask users questions in the Socratic tradition (may then augment this with Costa's Levels of Questioning)
- Users can ponder questions, or type in answers
- Compare student answers with privacy policy

### Flow 2 : Assistant

- Users can directly ask questions to the Assistant
- Assitant uses GPT to answer.
