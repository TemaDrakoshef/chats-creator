import asyncio
import logging
import os
import shutil
from pathlib import Path
from uuid import uuid4

from src.opentele.api import UseCurrentSession
from src.opentele.td import TDesktop

logger = logging.getLogger(__name__)


async def load_tdata():
    sem = asyncio.Semaphore(60)
    ftemp = Path(".tdtemp")
    if not ftemp.exists():
        ftemp.mkdir()
    else:
        shutil.rmtree(ftemp, ignore_errors=True)
    tdata_paths = [
        f for f in os.listdir("feed_tdata") if Path("feed_tdata", f).is_dir()
    ]
    logger.info("Найдено %d TDATA. Подгружаю...", len(tdata_paths))

    converting_tasks = [load_tdata_account(path, sem) for path in tdata_paths]
    new_accs = await asyncio.gather(*converting_tasks)
    logger.info("Подгружено %d аккаунтов", len(new_accs))


async def load_tdata_account(path: Path, sem: asyncio.Semaphore):
    async with sem:
        real_path = Path("feed_tdata", path)
        client = None

        try:
            tdesk = TDesktop(str(real_path), keyFile="data")
            new_session_path = Path(".tdtemp", uuid4().hex + ".session")
            client = await tdesk.ToTelethon(
                session=str(new_session_path),
                flag=UseCurrentSession,
            )
            await asyncio.wait_for(client.connect(), timeout=10)
            me = await client.get_me()
            if me is None:
                raise asyncio.TimeoutError()
            await client.disconnect()
            await asyncio.sleep(1)
            shutil.move(
                str(new_session_path),
                new_session_path.parent.parent
                / "sessions"
                / (me.phone + ".session"),
            )
        except asyncio.TimeoutError:
            logger.error(
                "Не удалось подключиться к аккаунту %s", str(real_path)
            )
            return None
        else:
            logger.info(
                "Удалось подгрузить аккаунт %s ('%s')",
                me.phone,
                str(real_path),
            )
            return me.phone
        finally:
            try:
                if client:
                    if client.is_connected():
                        await client.disconnect()
                await asyncio.sleep(0.5)
                if new_session_path.exists():
                    try:
                        os.remove(new_session_path)
                    except PermissionError:
                        pass
                shutil.rmtree(real_path, ignore_errors=True)
            except Exception as cleanup_err:
                logger.debug("Cleanup error: %s", cleanup_err)
