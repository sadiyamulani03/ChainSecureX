import logging
import os

# Create logs folder automatically
if not os.path.exists("logs"):
    os.makedirs("logs")

# Logger configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler("logs/server.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("ChainSecureX")