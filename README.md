# E Voting Core

This project implements a secure and privacy-preserving e-voting system based on elliptic curve
cryptography ([ECC](https://web.ua.es/es/recsi2014/documentos/papers/an-elliptic-curve-based-homomorphic-remote-voting-system.pdf)).
The system uses homomorphic encryption to ensure vote confidentiality while allowing vote tallying without decrypting
individual votes.

## Features

- **Elliptic Curve Cryptography (ECC):** Provides secure and efficient encryption.
- **Homomorphic Encryption:** Enables vote tallying without revealing individual votes.
- **REST API:** Built with FastAPI for managing voting servers, users, and votes.
- **Meet-in-the-Middle Algorithm:** Optimized vote decryption for efficient results.

## API Endpoints

### Voting Server Management

- **Create Voting Server:**  
  `POST /internal/v1/create_voting_server`  
  Creates a new voting server with specified parameters.

- **Publish Results:**  
  `GET /internal/v1/publish_result/{server_id}`  
  Publishes the results of a voting server.

### User Management

- **Create User:**  
  `POST /internal/v1/create_user`  
  Creates a new user for voting.

### Voting

- **Cast Vote:**  
  `POST /internal/v1/vote`  
  Allows a user to cast a vote for a candidate.

- **Open Vote:**  
  `POST /internal/v1/open_vote`  
  Opens the vote and computes the results.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate 
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
   ```

4. Set environment variables for ECC parameters:
    ```bash
    export ECC_A=<value>
    export ECC_B=<value>
    export ECC_P=<value>
    export ECC_ORDER=<value>
    ```
   
5. Run the application:
    ```bash
    python api_https.py --config config.json
    ```
## Usage
- Start the server using the above command.
- Use tools like Postman or curl to interact with the API endpoints.
- Create a voting server, users, and cast votes.
- Open the vote and publish results.

## References
[An Elliptic Curve-Based Homomorphic Remote Voting System](https://web.ua.es/es/recsi2014/documentos/papers/an-elliptic-curve-based-homomorphic-remote-voting-system.pdf)
