import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from clickhouse import init_clickhouse
from config import settings
from extractors import KafkaExtractor
from loaders import ClickhouseLoader
from logger import setup_logger
from transformers import event_transformer

from models import Event

logger = logging.getLogger("etl")


async def main():
    try:
        logger.info("starting etl process")
        init_clickhouse(settings.ch)
        batch: list[Event] = []
        loader = ClickhouseLoader(settings.ch)
        transformer = event_transformer
        extractor = KafkaExtractor(settings.kafka)
        # TODO: pipeline
        async with extractor:
            async for item in extractor.extract():
                batch.append(transformer(item))
                if len(batch) == settings.batch_size:
                    loader.load_batch(batch)
                    batch = []
            loader.load_batch(batch)
        logger.info("etl proccess complete")
    except Exception:
        logger.exception("unhandled exception")
        raise


if __name__ == "__main__":
    setup_logger() 
    if settings.run_once:
        asyncio.run(main())
    else:
        scheduler = AsyncIOScheduler()
        scheduler.add_job(main, "interval", seconds=settings.run_interval_seconds)
        logger.info("starting_scheduler")
        scheduler.start()

        # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
        try:
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
