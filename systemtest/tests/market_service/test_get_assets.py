from assertpy import assert_that
from requests import post

from tests.utils.services import assets_url


class TestGetBaseAssets:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        pass

    def test_when_get_assets_then_sucess(self):
        ### GIVEN

        ### WHEN
        response = post(assets_url)

        ### THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()['status']).is_equal_to('success')
        assets = response.json().get('message')
        assert_that(assets).is_type_of(list)
        assert_that(assets).is_length(3)

        asset = assets[0]
        assert_that(asset['short_name']).is_equal_to('BTC')
        assert_that(asset['long_name']).is_equal_to('Bitcoin')
        assert_that(asset['asset_id']).is_equal_to(1)

        asset = assets[1]
        assert_that(asset['short_name']).is_equal_to('DOGE')
        assert_that(asset['long_name']).is_equal_to('Dogecoin')
        assert_that(asset['asset_id']).is_equal_to(2)

        asset = assets[2]
        assert_that(asset['short_name']).is_equal_to('MLN')
        assert_that(asset['long_name']).is_equal_to('Melonhead Protocol')
        assert_that(asset['asset_id']).is_equal_to(3)