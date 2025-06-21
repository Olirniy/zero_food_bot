from utils.logger import setup_logger


def log_dependencies():
    import sys
    from pathlib import Path

    logger = setup_logger("dependencies")

    logger.info("Пути Python:")
    for p in sys.path:
        logger.info(f"  {p}")

    logger.info("Импортированные модули:")
    for name, module in sorted(sys.modules.items()):
        if name.startswith('zero_food_bot'):
            logger.info(f"  {name}: {module.__file__}")