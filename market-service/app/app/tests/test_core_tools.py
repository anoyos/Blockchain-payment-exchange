from app.core import tools


class TestCoreTools:

    def test_get_asset_by_net_code(self):
        data = tools.get_asset_by_net_code('USDT')
        assert isinstance(data, dict)
