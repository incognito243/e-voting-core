import argparse
import json
import uvicorn

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Run the FastAPI service with a configuration file.")
    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="Path to the configuration file (e.g., config.json)."
    )
    args = parser.parse_args()

    # Load configuration from the file
    with open(args.config, "r") as config_file:
        config = json.load(config_file)

    # Run the FastAPI application with the loaded configuration
    uvicorn.run(
        "client.api_https:app",
        host=config.get("host", "127.0.0.1"),
        port=config.get("port", 8000),
        reload=config.get("reload", False)
    )

if __name__ == "__main__":
    main()