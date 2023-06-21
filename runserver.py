import uvicorn
import logging




def main():
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    # logging.basicConfig(format='{levelname:7} {message}', style='{', level=logging.INFO)
    #del log_config["loggers"][""]
    uvicorn.run(
        "prometheus_fast_api.main:app",
        host="0.0.0.0",
        port=3030,
        # log_level="info",
        reload=True,
        log_config=log_config
    )