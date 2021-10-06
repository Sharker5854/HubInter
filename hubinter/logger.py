from loguru import logger

logger.add(
	"logs/log.log",
	# rotation="1 GB"
)