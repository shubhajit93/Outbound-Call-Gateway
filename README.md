# Outbound-Call-Gateway

Outbound-Call-Gateway is a Python project that implements NATS JetStream consumers and publishers. It provides a model to handle messaging in a distributed system, particularly focusing on work queue retention policies.

### Directory Breakdown

- **nats_consumer**: Contains the implementation for the NATS consumer.
  - `consumer.py`: The main consumer class that connects to a NATS JetStream server, pulls messages, and processes them.
  
- **nats_publisher**: Contains the implementation for the NATS publisher.
  - `publisher.py`: The main publisher class that connects to a NATS JetStream server and publishes messages to a specified subject.
  
- **scripts**: Contains scripts to run the consumer and publisher.
  - `run_consumer.py`: A script to run the NATS consumer.
  - `run_streamCreation.py`: A script to create NATS stream.
  - `run_publisher.py`: A script to run the NATS publisher.
  
- **.env**: Environment variables file used to configure the application.
  
- **requirements.txt**: Lists the Python dependencies required for the project.
 
- **MANIFEST.in**: Includes additional files in the package distribution.

## Setup

### Prerequisites

- Python 3.6 or higher
- NATS server (JetStream enabled)
- Docker command to run NATS server: docker run -d --name nats-server -p 4222:4222 -p 8222:8222 nats --js
- Virtual environment (optional but recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/outbound-gateway.git
   cd outbound-gateway
   ```

2. **Create and activate a virtual environment:**:
   ```bash
   python -m venv .venv 
   source .venv/bin/activate On Windows: .venv\Scripts\activate
   ```
3. **Create and activate a virtual environment:**:
   ```bash
   pip install -r requirements.txt
   ```  
### Configuration
**Configure the environment variables in the `.env` file:**
```env
  NATS_URL=nats://localhost:4222
  STREAM_NAME=outbounds
  BASE_SUBJECT=outbounds
  PORT=8000
  BATCH_SIZE=500
  CONSUMER_WORKER_COUNT=4
```
### Creating a NATS stream
```commandline
   python scripts/run_streamCreation.py
```
### Running the Publisher
```commandline
   python scripts/run_publisher.py
```
### Running the Consumer
```commandline
python scripts/run_consumer.py consumer-1
```
