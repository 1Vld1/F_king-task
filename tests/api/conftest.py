import pytest
from aiohttp.web_urldispatcher import DynamicResource

from store.api.__main__ import parser
from store.api.app import create_app


@pytest.fixture
def arguments(aiomisc_unused_port, tmp_url):
    """
    Аргументы для запуска приложения.
    """
    return parser.parse_args(
        [
            '--log-level=debug',
            '--api-address=127.0.0.1',
            f'--api-port={aiomisc_unused_port}',
            f'--pg-url={tmp_url}'
        ]
    )


@pytest.fixture
async def api_client(aiohttp_client, arguments):
    app = create_app(arguments)
    client = await aiohttp_client(app, server_kwargs={
        'port': arguments.api_port
    })

    try:
        yield client
    finally:
        await client.close()


@pytest.fixture(scope='session')
def url_for():
    def _url_for(path: str, **kwargs) -> str:
        """
        Генерирует URL для динамического aiohttp маршрута с параметрами.
        """
        kwargs = {
            key: str(value)
            # Все значения должны быть str (для DynamicResource)
            for key, value in kwargs.items()
        }

        return str(DynamicResource(path).url_for(**kwargs))

    return _url_for
